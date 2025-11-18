from typing import List, Optional
from datetime import datetime
from uuid import uuid4
from pymongo.collection import Collection
from pymongo import MongoClient
from src.bll_models import TripRequest


class TripRequestManager:
    """Manages trip request creation and storage operations."""

    def __init__(self, db_collection: Collection):
        """Initialize TripRequestManager."""
        self.trip_requests_collection = db_collection
        self.trip_requests_collection.create_index("request_id", unique=True)

    def create_trip_request(self, trip_request: TripRequest) -> str:
        """Create a new trip request and store it in the database."""
        trip_request_dict = trip_request.model_dump()
        
        request_id = trip_request_dict.get("request_id") or str(uuid4())
        trip_request_dict["request_id"] = request_id
        self.trip_requests_collection.insert_one(trip_request_dict)
        trip_request.request_id = request_id
            
        return trip_request.request_id

    def get_trip_request_by_id(self, request_id: str) -> Optional[TripRequest]:
        """Find a single trip request by its `request_id`."""
        data = self.trip_requests_collection.find_one({"request_id": request_id})
        if not data:
            return None
        return TripRequest(**data)

    def get_all_trip_requests(self, destination: Optional[str] = None) -> List[TripRequest]:
        """Retrieve all trip requests, optionally filtered by destination."""
        query: dict = {}
        if destination:
            query["destination"] = {"$regex": destination, "$options": "i"}

        all_requests_data = self.trip_requests_collection.find(query)
        return [TripRequest(**r) for r in all_requests_data]

    def update_trip_request(self, request_id: str, trip_id: str, status: str) -> bool:
        """Update a trip request's status and assign a trip_id."""
        result = self.trip_requests_collection.update_one(
            {"request_id": request_id},
            {"$set": {"status": status, "trip_id": trip_id, "updated_at": datetime.utcnow()}}
        )
        return result.modified_count > 0
