from src.trip import Trip
import uuid


class TripManager:
    """Manages trip creation and storage operations."""
    
    def __init__(self, db_collection=None):
        """Initialize TripManager.
        
        Args:
            db_collection: MongoDB collection for storing trips (optional)
        """
        self.db_collection = db_collection
    
    def create_trip(self, trip: Trip) -> str:
        """Create a new trip and store it in the database.
        
        Args:
            trip: Trip object to create
            
        Returns:
            The trip_id of the created trip
            
        Raises:
            ValueError: If the provided trip is invalid.
        """
        # Ensure trip is valid (Trip validates on init; this re-validates in case of mutations)
        trip.validate()

        trip_dict = trip.to_dict()
        
        if self.db_collection is not None:
            result = self.db_collection.insert_one(trip_dict)
            trip.trip_id = str(result.inserted_id)
        else:
            # Generate a unique ID when no database is available
            trip.trip_id = str(uuid.uuid4())
        
        return trip.trip_id
