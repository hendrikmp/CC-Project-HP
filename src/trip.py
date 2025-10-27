from datetime import datetime
from typing import List, Optional


class Trip:
    """Represents a trip posted by a driver."""
    
    def __init__(
        self,
        driver_id: str,
        driver_car: str,
        free_seats: int,
        destination: str,
        pickup_location: str,
        start_datetime: datetime,
        return_datetime: datetime,
        cost_per_passenger: float,
        trip_id: Optional[str] = None,
        passengers: Optional[List[str]] = None
    ):
        """Initialize a new Trip.
        
        Args:
            driver_id: Unique identifier for the driver
            driver_car: Description of the driver's car
            free_seats: Number of available seats (must be positive)
            destination: Destination location
            pickup_location: Pick-up/drop-off location
            start_datetime: Trip start date and time
            return_datetime: Trip return date and time
            cost_per_passenger: Cost per passenger
            trip_id: Unique identifier for the trip (optional, for DB)
            passengers: List of passenger IDs (optional, defaults to empty)
        """
        self.trip_id = trip_id
        self.driver_id = driver_id
        self.driver_car = driver_car
        self.free_seats = free_seats
        self.destination = destination
        self.pickup_location = pickup_location
        self.start_datetime = start_datetime
        self.return_datetime = return_datetime
        self.cost_per_passenger = cost_per_passenger
        self.passengers = passengers if passengers is not None else []
        
        self._validate()
    
    def _validate(self):
        """Validate trip data according to business rules."""
        if self.free_seats <= 0:
            raise ValueError("free_seats must be positive")
        
        if len(self.passengers) > self.free_seats:
            raise ValueError(
                f"Number of passengers ({len(self.passengers)}) exceeds "
                f"free seats ({self.free_seats})"
            )
        
        if self.return_datetime <= self.start_datetime:
            raise ValueError("return_datetime must be after start_datetime")
        
        if self.cost_per_passenger < 0:
            raise ValueError("cost_per_passenger cannot be negative")
        
        if not self.driver_id or not self.driver_car:
            raise ValueError("driver_id and driver_car are required")
        
        if not self.destination or not self.pickup_location:
            raise ValueError("destination and pickup_location are required")
    
    def add_passenger(self, passenger_id: str) -> bool:
        """Add a passenger to the trip.
        
        Args:
            passenger_id: Unique identifier for the passenger
            
        Returns:
            True if passenger was added, False if trip is full
            
        Raises:
            ValueError: If passenger is already in the trip
        """
        if passenger_id in self.passengers:
            raise ValueError(f"Passenger {passenger_id} is already in this trip")
        
        if len(self.passengers) >= self.free_seats:
            return False
        
        self.passengers.append(passenger_id)
        return True
    
    def to_dict(self):
        """Convert trip to dictionary format suitable for MongoDB."""
        return {
            "trip_id": self.trip_id,
            "driver_id": self.driver_id,
            "driver_car": self.driver_car,
            "free_seats": self.free_seats,
            "destination": self.destination,
            "pickup_location": self.pickup_location,
            "start_datetime": self.start_datetime,
            "return_datetime": self.return_datetime,
            "cost_per_passenger": self.cost_per_passenger,
            "passengers": self.passengers
        }

    def validate(self) -> None:
        """Re-run validation on current fields. Raises ValueError if invalid."""
        self._validate()
