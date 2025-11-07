from flask_openapi3 import APIBlueprint, Tag
from typing import List

from src.api_models import (
    TripBody, TripResponse, TripIdPath, TripSearchQuery,
    SuccessResponse, ErrorResponse
)
from src.trip import Trip
from src.trip_manager import TripManager

# In a real app, this would be injected, not a global
trip_manager = TripManager()

# Define an API blueprint for trip-related routes
api = APIBlueprint(
    'trips',
    __name__,
    url_prefix='/trips',
    abp_tags=[Tag(name='Trips', description='Operations related to trips')],
    abp_responses={400: ErrorResponse, 404: ErrorResponse}
)

@api.post('/', summary="Create a new trip")
def create_trip(body: TripBody) -> TripResponse:
    """
    Creates a new trip based on the provided details.
    The server assigns a unique `trip_id`.
    """
    new_trip = Trip(**body.model_dump())
    trip_id = trip_manager.create_trip(new_trip)
    
    # Return the full trip details, including the new ID
    return TripResponse(trip_id=trip_id, **new_trip.model_dump())

@api.get('/', summary="List all available trips")
def get_all_trips(query: TripSearchQuery) -> List[TripResponse]:
    """
    Returns a list of all available trips.
    Supports optional filtering by pickup location, destination, and date.
    
    *Note: Filtering logic is not yet implemented.*
    """
    # Placeholder: a real implementation would pass filters to the manager
    all_trips = trip_manager.get_all_trips()
    
    # Convert Trip models to TripResponse models
    return [TripResponse(**trip.model_dump()) for trip in all_trips]

@api.get('/<string:trip_id>', summary="Get a specific trip by ID")
def get_trip_by_id(path: TripIdPath) -> TripResponse:
    """
    Returns the details of a single trip identified by its `trip_id`.
    
    *Note: This is a placeholder and will return a 404.*
    """
    # Placeholder: a real implementation would fetch from the DB
    trip = trip_manager.get_trip_by_id(path.trip_id)
    if trip:
        return TripResponse(**trip.model_dump())
    # In a real app, you'd return a proper 404 error response
    return {"code": 404, "message": "Trip not found"}, 404

@api.post('/<string:trip_id>/join', summary="Join a trip as a passenger")
def join_trip(path: TripIdPath) -> SuccessResponse:
    """
    Allows a user to join a specific trip.
    
    *Note: This is a placeholder and will not modify the trip.*
    """
    # Placeholder: a real implementation would require a passenger ID
    # and update the trip in the database.
    return {"message": f"Successfully joined trip {path.trip_id} (placeholder)."}

@api.delete('/<string:trip_id>', summary="Delete a trip")
def delete_trip(path: TripIdPath) -> SuccessResponse:
    """
    Deletes a trip by its ID.
    
    *Note: This is a placeholder and will not delete the trip.*
    """
    return {"message": f"Trip {path.trip_id} deleted successfully (placeholder)."}
