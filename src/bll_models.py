from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class Trip(BaseModel):
    """Pydantic-based Trip model with business validations and helpers.

    This preserves the previous public methods (`validate`, `to_dict`,
    `add_passenger`) so existing code and tests continue to work with
    minimal changes.
    """

    trip_id: Optional[str] = Field(default=None)
    driver_id: str
    driver_car: str
    capacity: int
    destination: str
    pickup_location: str
    start_datetime: datetime
    return_datetime: datetime
    cost_per_passenger: float
    passengers: List[str] = Field(default_factory=list)

    @field_validator("capacity")
    def capacity_must_be_positive(cls, v):
        """Validate that capacity is a positive integer."""
        if v <= 0:
            raise ValueError("capacity must be positive")
        return v

    @field_validator("cost_per_passenger")
    def cost_cannot_be_negative(cls, v):
        if v < 0:
            raise ValueError("cost_per_passenger cannot be negative")
        return v

    @model_validator(mode="after")
    def check_dates_and_passengers(self):
        if self.return_datetime <= self.start_datetime:
            raise ValueError("return_datetime must be after start_datetime")

        if len(self.passengers) > self.capacity:
            raise ValueError(
                f"Number of passengers ({len(self.passengers)}) exceeds capacity ({self.capacity})"
            )

        return self

    def add_passenger(self, passenger_id: str) -> bool:
        """Add a passenger to the trip.

        Raises ValueError if passenger already exists. Returns False if trip is full.
        """
        if passenger_id in self.passengers:
            raise ValueError(f"Passenger {passenger_id} is already in this trip")

        if len(self.passengers) >= self.capacity:
            return False

        self.passengers.append(passenger_id)
        return True

    def to_dict(self) -> dict:
        """Return a dictionary representation suitable for storage.

        Dates are left as datetime objects; persistence layer may convert them.
        """
        return {
            "trip_id": self.trip_id,
            "driver_id": self.driver_id,
            "driver_car": self.driver_car,
            "capacity": self.capacity,
            "destination": self.destination,
            "pickup_location": self.pickup_location,
            "start_datetime": self.start_datetime,
            "return_datetime": self.return_datetime,
            "cost_per_passenger": self.cost_per_passenger,
            "passengers": list(self.passengers),
        }

    def validate(self) -> None:
        """Re-run validation by rebuilding model (will raise on invalid state)."""
        # Pydantic v2: re-validate current state
        self.__class__.model_validate(self.model_dump())


class TripRequestStatus(str, Enum):
    """Enum for the status of a trip request."""

    PENDING = "pending"
    ACCEPTED = "accepted"


class TripRequest(BaseModel):
    """Pydantic-based TripRequest model."""

    request_id: Optional[str] = Field(default=None)
    passenger_id: str
    destination: str
    earliest_start_date: datetime
    latest_start_date: datetime
    status: TripRequestStatus = Field(default=TripRequestStatus.PENDING)
    trip_id: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @model_validator(mode="after")
    def check_dates(self):
        if self.latest_start_date <= self.earliest_start_date:
            raise ValueError("latest_start_date must be after earliest_start_date")
        return self

    def to_dict(self) -> dict:
        """Return a dictionary representation suitable for storage."""
        data = self.model_dump()
        # Convert enum to string for storage
        data["status"] = self.status.value
        return data
