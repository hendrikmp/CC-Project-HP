from flask_openapi3 import APIBlueprint, Tag
from flask import current_app
from typing import List

from src.api_models import (
    TripBody, TripResponse, TripIdPath, TripSearchQuery,
    ErrorResponse, JoinTripBody
)
from src.trip import Trip
from src.trip_manager import TripManager

# Define an API blueprint for trip-related routes
api = APIBlueprint(
    'trips',
    __name__,
    url_prefix='/trips',
    abp_tags=[Tag(name='Trips', description='Operations related to trips')],
    abp_responses={400: ErrorResponse, 404: ErrorResponse}
)


@api.post('/', summary="Create a new trip")
def create_trip(body: TripBody) -> str:
    """
    Creates a new trip based on the provided details.
    The server assigns a unique `trip_id`.
    """
    manager: TripManager = current_app.config["trip_manager"]
    trip_id = manager.create_trip(Trip(**body.model_dump()))
    
    # Return the full trip details, including the new ID
    return trip_id


@api.get('/', summary="List all available trips")
def get_all_trips(query: TripSearchQuery) -> List[dict]:
    """
    Returns a list of all available trips.
    Supports optional filtering by pickup location, destination, and date.
    
    """
    manager: TripManager = current_app.config["trip_manager"]
    all_trips = manager.get_all_trips(
        pickup=query.pickup,
        destination=query.destination,
        trip_date=query.date,
    )
    
    # Convert Trip models to TripResponse models
    return [TripResponse(**trip.model_dump()).model_dump() for trip in all_trips]


@api.get('/<string:trip_id>', summary="Get a specific trip by ID")
def get_trip_by_id(path: TripIdPath) -> dict:
    """
    Returns the details of a single trip identified by its `trip_id`.
    """
    manager: TripManager = current_app.config["trip_manager"]
    trip = manager.get_trip_by_id(path.trip_id)
    if trip:
        return TripResponse(**trip.model_dump()).model_dump()
    # In a real app, you'd return a proper 404 error response
    return ErrorResponse(message="Trip not found", code=404)


@api.post('/<string:trip_id>/join', summary="Join a trip as a passenger")
def join_trip(path: TripIdPath, body: JoinTripBody) -> str:
    """
    Allows a user to join a specific trip.
    
    Returns a success message on success, or an error message with appropriate status code.
    """
    manager: TripManager = current_app.config["trip_manager"]
    trip = manager.get_trip_by_id(path.trip_id)
    if not trip:
        return "Trip not found", 404
    added = manager.add_passenger_to_trip(path.trip_id, body.passenger_id)
    if not added:
        return "Trip is full or passenger already joined", 400
    return f"Successfully joined trip {path.trip_id}"


@api.delete('/<string:trip_id>', summary="Delete a trip")
def delete_trip(path: TripIdPath) -> str:
    """
    Deletes a trip by its ID.
    
    Returns a success message on success, or an error message with appropriate status code.
    """
    manager: TripManager = current_app.config["trip_manager"]
    deleted = manager.delete_trip(path.trip_id)
    if not deleted:
        return "Trip not found", 404
    return f"Trip {path.trip_id} deleted successfully."