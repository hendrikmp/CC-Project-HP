from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from .bll_models import TripRequestStatus


# --- Trip Models ---

class TripBody(BaseModel):
    """Request body for creating a new trip.
    Excludes fields that are auto-generated or set by the server.
    """
    driver_id: str
    driver_car: str
    capacity: int = Field(..., gt=0, description="Maximum number of passengers, must be positive.")
    destination: str
    pickup_location: str
    start_datetime: datetime
    return_datetime: datetime
    cost_per_passenger: float = Field(..., ge=0, description="Cost per passenger, cannot be negative.")

class TripResponse(TripBody):
    """Response model for a single trip, including TripBody + server-set fields."""
    trip_id: str
    passengers: List[str]

class TripIdPath(BaseModel):
    """Path parameter model for identifying a trip."""
    trip_id: str = Field(..., description="The unique identifier of the trip.")

class TripSearchQuery(BaseModel):
    """Query parameters for searching trips."""
    pickup: Optional[str] = Field(None, description="Filter by pickup location.")
    destination: Optional[str] = Field(None, description="Filter by destination.")
    date: Optional[datetime] = Field(None, description="Filter by trip date.")

# --- Trip Request Models ---

class TripRequestBody(BaseModel):
    """Request body for creating a new trip request."""
    passenger_id: str
    destination: str
    earliest_start_date: datetime
    latest_start_date: datetime

class TripRequestResponse(BaseModel):
    """Response model for a single trip request."""
    request_id: str
    passenger_id: str
    destination: str
    earliest_start_date: datetime
    latest_start_date: datetime
    status: TripRequestStatus
    trip_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class TripRequestUpdateBody(BaseModel):
    """Request body for updating a trip request (e.g., accepting it)."""
    trip_id: str
    status: TripRequestStatus

class RequestIdPath(BaseModel):
    """Path parameter model for identifying a trip request."""
    request_id: str = Field(..., description="The unique identifier of the trip request.")

class TripRequestSearchQuery(BaseModel):
    """Query parameters for searching trip requests."""
    destination: Optional[str] = Field(None, description="Filter by destination.")


# --- Generic Models ---

class JoinTripBody(BaseModel):
    """Request body for joining a trip as a passenger."""
    passenger_id: str = Field(..., description="The ID of the passenger joining the trip.")

class ErrorResponse(BaseModel):
    """Generic error response model."""
    code: int
    message: str