from typing import List, Optional
from datetime import datetime, date
from uuid import uuid4
from pymongo.collection import Collection
from pymongo import MongoClient
from src.trip import Trip


class TripManager:
    """Manages trip creation and storage operations."""

    def __init__(self, db_collection: Optional[Collection] = None, mongo_uri: str = None):
        """Initialize TripManager.
        
        Args:
            db_collection: MongoDB collection for storing trips (optional).
            mongo_uri: URI for connecting to MongoDB (optional).
        """
        if db_collection is not None:
            self.db_collection = db_collection
        elif mongo_uri:
            client = MongoClient(mongo_uri)
            self.db_collection = client.get_database().get_collection("trips")
        else:
            self.db_collection = None

        # Ensure an index on trip_id for efficient queries
        if self.db_collection is not None:
            self.db_collection.create_index("trip_id", unique=True)

    def create_trip(self, trip: Trip) -> Trip:
        """Create a new trip and store it in the database.
        
        Returns:
            The created Trip object.
        """
        trip.validate()  # Re-validate before insertion
        trip_dict = trip.model_dump()

        if self.db_collection is not None:
            trip_id = trip_dict.get("trip_id") or str(uuid4())
            trip_dict["trip_id"] = trip_id  # Use trip_id as the application-level identifier
            self.db_collection.insert_one(trip_dict)
            trip.trip_id = trip_id
        else:
            trip.trip_id = str(uuid4())
        
        return trip

    def get_all_trips(
        self,
        pickup: Optional[str] = None,
        destination: Optional[str] = None,
        trip_date: Optional[datetime] = None,
    ) -> List[Trip]:
        """Retrieve all trips, optionally filtered by pickup, destination, and date.

        Args:
            pickup: Optional pickup location substring (case-insensitive contains).
            destination: Optional destination substring (case-insensitive contains).
            trip_date: Optional datetime; matches trips that start on the same calendar day.
        """
        if self.db_collection is None:
            return []

        query: dict = {}
        if pickup:
            query["pickup_location"] = {"$regex": pickup, "$options": "i"}
        if destination:
            query["destination"] = {"$regex": destination, "$options": "i"}
        if trip_date:
            # Match start_datetime within the day [00:00, 23:59:59]
            if isinstance(trip_date, datetime):
                day_start = datetime(trip_date.year, trip_date.month, trip_date.day, 0, 0, 0)
            else:
                # if a date is ever passed, normalize
                day_start = datetime(trip_date.year, trip_date.month, trip_date.day, 0, 0, 0)  # type: ignore[attr-defined]
            day_end = day_start.replace(hour=23, minute=59, second=59, microsecond=999999)
            query["start_datetime"] = {"$gte": day_start, "$lte": day_end}

        all_trips_data = self.db_collection.find(query)
        return [Trip(**t) for t in all_trips_data]

    def get_trip_by_id(self, trip_id: str) -> Optional[Trip]:
        """Find a single trip by its `trip_id`. Returns None if not found."""
        if self.db_collection is None:
            return None
        data = self.db_collection.find_one({"trip_id": trip_id})
        if not data:
            return None
        return Trip(**data)

    def add_passenger_to_trip(self, trip_id: str, passenger_id: str) -> bool:
        """Add a passenger to a trip in the database.

        Returns True if the passenger was added; False if the trip is full or passenger already present.
        """
        if self.db_collection is None:
            return False

        # Ensure capacity before adding and avoid duplicates atomically
        result = self.db_collection.update_one(
            {
                "trip_id": trip_id,
                "$expr": {"$lt": [{"$size": "$passengers"}, "$capacity"]},
                "passengers": {"$ne": passenger_id},
            },
            {"$addToSet": {"passengers": passenger_id}},
        )
        return result.modified_count == 1

    def delete_trip(self, trip_id: str) -> bool:
        """Delete a trip by id. Returns True if a document was deleted."""
        if self.db_collection is None:
            return False
        result = self.db_collection.delete_one({"trip_id": trip_id})
        return result.deleted_count == 1
