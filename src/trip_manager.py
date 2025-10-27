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
    
    def validate_trip_data(
        self,
        driver_id: str,
        driver_car: str,
        free_seats: int,
        destination: str,
        pickup_location: str,
        start_datetime,
        return_datetime,
        cost_per_passenger: float
    ) -> bool:
        """Validate trip data before creation.
        
        Returns:
            True if all validation passes
            
        Raises:
            ValueError: If any validation fails
        """
        trip = Trip(
            driver_id=driver_id,
            driver_car=driver_car,
            free_seats=free_seats,
            destination=destination,
            pickup_location=pickup_location,
            start_datetime=start_datetime,
            return_datetime=return_datetime,
            cost_per_passenger=cost_per_passenger
        )
        return True
