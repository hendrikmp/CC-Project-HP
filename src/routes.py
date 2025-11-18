from flask_openapi3 import APIBlueprint, Tag
from flask import current_app
from typing import List

from src.api_models import (
    TripBody, TripResponse, TripIdPath, TripSearchQuery,
    ErrorResponse, JoinTripBody, TripRequestBody, TripRequestResponse, 
    TripRequestUpdateBody, RequestIdPath, TripRequestSearchQuery
)
from src.bll_models import Trip, TripRequest
from src.trip_manager import TripManager
from src.trip_request_manager import TripRequestManager

# Define an API blueprint for trip-related routes
api = APIBlueprint(
    'trips',
    __name__,
    url_prefix='/trips',
    abp_tags=[Tag(name='Trips', description='Operations related to trips'), Tag(name='Trip Requests', description='Operations related to trip requests')],
    abp_responses={400: ErrorResponse, 404: ErrorResponse}
)


@api.post('/', summary="Create a new trip")
def create_trip(body: TripBody) -> dict:
    """
    Creates a new trip based on the provided details.
    The server assigns a unique `trip_id`.
    """
    manager: TripManager = current_app.config["trip_manager"]
    trip_id = manager.create_trip(Trip(**body.model_dump()))
    return {"trip_id": trip_id}


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
    return [TripResponse(**trip.model_dump()).model_dump() for trip in all_trips]


@api.get('/<trip_id>', summary="Get a trip by ID")
def get_trip_by_id(path: TripIdPath) -> dict:
    """
    Returns the details of a specific trip by its ID.
    """
    manager: TripManager = current_app.config["trip_manager"]
    trip = manager.get_trip_by_id(path.trip_id)
    if trip:
        return TripResponse(**trip.model_dump()).model_dump()
    return {"message": "Trip not found"}, 404


@api.post('/<trip_id>/join', summary="Join a trip as a passenger")
def join_trip(path: TripIdPath, body: JoinTripBody) -> dict:
    """
    Allows a passenger to join an existing trip.
    """
    manager: TripManager = current_app.config["trip_manager"]
    updated_trip = manager.add_passenger_to_trip(path.trip_id, body.passenger_id)
    if updated_trip:
        return {"message": "Passenger added successfully"}
    return {"message": "Trip not found or could not be updated"}, 404


@api.delete('/<trip_id>', summary="Delete a trip")
def delete_trip(path: TripIdPath) -> dict:
    """
    Deletes a trip by its ID.
    """
    manager: TripManager = current_app.config["trip_manager"]
    if manager.delete_trip(path.trip_id):
        return {"message": "Trip deleted successfully"}
    return {"message": "Trip not found"}, 404


@api.post('/requests', summary="Create a new trip request")
def create_trip_request(body: TripRequestBody) -> dict:
    """
    Creates a new trip request.
    """
    manager: TripRequestManager = current_app.config["trip_request_manager"]
    trip_request_id = manager.create_trip_request(TripRequest(**body.model_dump()))
    return {"request_id": trip_request_id}


@api.get('/requests', summary="List all trip requests")
def get_all_trip_requests(query: TripRequestSearchQuery) -> List[dict]:
    """
    Returns a list of all trip requests.
    Supports optional filtering by destination.
    """
    manager: TripRequestManager = current_app.config["trip_request_manager"]
    all_requests = manager.get_all_trip_requests(destination=query.destination)
    return [TripRequestResponse(**req.model_dump()).model_dump() for req in all_requests]


@api.get('/requests/<request_id>', summary="Get a trip request by ID")
def get_trip_request_by_id(path: RequestIdPath) -> dict:
    """
    Returns the details of a specific trip request by its ID.
    """
    manager: TripRequestManager = current_app.config["trip_request_manager"]
    trip_request = manager.get_trip_request_by_id(path.request_id)
    if trip_request:
        return TripRequestResponse(**trip_request.model_dump()).model_dump()
    return {"message": "Trip request not found"}, 404


@api.put('/requests/<request_id>', summary="Update a trip request")
def update_trip_request(path: RequestIdPath, body: TripRequestUpdateBody) -> dict:
    """
    Updates a trip request's status.
    """
    manager: TripRequestManager = current_app.config["trip_request_manager"]
    success = manager.update_trip_request(path.request_id, body.trip_id, body.status)
    if success:
        return {"message": "Trip request updated successfully"}
    return {"message": "Trip request not found or could not be updated"}, 404