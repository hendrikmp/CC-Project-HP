from typing import List, Optional
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

    def create_trip(self, trip: Trip) -> str:
        """Create a new trip and store it in the database.
        
        Returns:
            The trip_id of the created trip.
        """
        trip.validate()  # Re-validate before insertion
        trip_dict = trip.model_dump()

        if self.db_collection is not None:
            # Let MongoDB generate the `_id`
            trip_dict.pop("trip_id", None)
            result = self.db_collection.insert_one(trip_dict)
            trip.trip_id = str(result.inserted_id)
        else:
            trip.trip_id = str(uuid4())
        
        return trip.trip_id

    def get_all_trips(self) -> List[Trip]:
        """Retrieve all trips."""
        if self.db_collection is None:
            return []
        
        all_trips_data = self.db_collection.find()
        # Convert BSON _id to string trip_id
        return [
            Trip(trip_id=str(t.pop("_id")), **t) for t in all_trips_data
        ]

    def get_trip_by_id(self, trip_id: str) -> Optional[Trip]:
        """Find a single trip by its ID."""
        # This is a placeholder. A real implementation would query the DB.
        # e.g., from bson import ObjectId; self.db_collection.find_one({"_id": ObjectId(trip_id)})
        return None

    def add_passenger_to_trip(self, trip_id: str, passenger_id: str) -> bool:
        """Add a passenger to a trip in the database."""
        # Placeholder for DB update logic
        # e.g., self.db_collection.update_one({"_id": ...}, {"$addToSet": {"passengers": ...}})
        return False
