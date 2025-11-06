from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

# --- Trip Models ---

class TripBody(BaseModel):
    """Request body for creating a new trip.
    Excludes fields that are auto-generated or set by the server.
    """
    driver_id: str
    driver_car: str
    free_seats: int = Field(..., gt=0, description="Number of available seats, must be positive.")
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
    user_id: str
    destination: str
    earliest_start: datetime
    latest_return: datetime

class TripRequestResponse(TripRequestBody):
    """Response model for a trip request, including TripRequestBody + ID."""
    request_id: str

# --- Generic Models ---

class SuccessResponse(BaseModel):
    """Generic success response model."""
    message: str

class ErrorResponse(BaseModel):
    """Generic error response model."""
    code: int
    message: str
