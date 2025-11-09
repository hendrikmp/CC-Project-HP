from datetime import datetime
from pydantic import ValidationError
import pytest
from pymongo import MongoClient
import os

from src.trip import Trip
from src.trip_manager import TripManager


@pytest.fixture
def valid_trip_data():
    """Fixture for valid trip data dictionary."""
    return {
        "driver_id": "driver123",
        "driver_car": "Tesla Model 3",
        "capacity": 3,
        "destination": "Lake Tahoe",
        "pickup_location": "San Francisco",
        "start_datetime": datetime(2025, 6, 1, 10, 0),
        "return_datetime": datetime(2025, 6, 1, 18, 0),
        "cost_per_passenger": 25.0,
    }


def test_create_trip_without_db(valid_trip_data):
    """Test creating a trip without a database connection. A UUID is assigned."""
    manager = TripManager()
    trip = Trip(**valid_trip_data)
    
    trip_id = manager.create_trip(trip)
    
    assert isinstance(trip_id, str)
    assert trip.trip_id == trip_id


def test_create_trip_with_db(valid_trip_data, mocker):
    """Test creating a trip with a mocked database connection."""
    mock_collection = mocker.MagicMock()
    
    manager = TripManager(db_collection=mock_collection)
    trip = Trip(**valid_trip_data)
    
    trip_id = manager.create_trip(trip)
    
    # Verify an insert occurred
    mock_collection.insert_one.assert_called_once()
    # Check that trip_id was removed before insertion and custom _id was set by app
    inserted_dict = mock_collection.insert_one.call_args[0][0]
    assert "trip_id" not in inserted_dict
    assert inserted_dict["_id"] == trip_id


def test_create_invalid_trip_raises_error(valid_trip_data):
    """Test that creating an invalid trip raises a Pydantic ValidationError."""
    manager = TripManager()
    invalid_data = valid_trip_data.copy()
    invalid_data["capacity"] = -1  # Invalid data
    
    with pytest.raises(ValidationError):
        Trip(**invalid_data)


def test_get_all_trips_with_db(mocker):
    """Test retrieving all trips from a mocked database."""
    mock_collection = mocker.MagicMock()
    mock_collection.find.return_value = [
        {
            "_id": "trip1",
            "driver_id": "d1",
            "driver_car": "Car A",
            "capacity": 2,
            "destination": "Dest A",
            "pickup_location": "Pick A",
            "start_datetime": datetime(2025, 7, 1, 10, 0),
            "return_datetime": datetime(2025, 7, 1, 18, 0),
            "cost_per_passenger": 20.0,
            "passengers": [],
        }
    ]
    
    manager = TripManager(db_collection=mock_collection)
    trips = manager.get_all_trips()
    
    assert len(trips) == 1
    assert isinstance(trips[0], Trip)
    assert trips[0].trip_id == "trip1"
    assert trips[0].driver_id == "d1"


def test_get_all_trips_no_db():
    """Test retrieving trips when no database is configured."""
    manager = TripManager()
    trips = manager.get_all_trips()
    assert trips == []


def test_get_trip_by_id_placeholder():
    """Test the placeholder for get_trip_by_id returns None."""
    manager = TripManager()
    assert manager.get_trip_by_id("some_id") is None


def test_add_passenger_to_trip_placeholder():
    """Test the placeholder for add_passenger_to_trip returns False."""
    manager = TripManager()
    assert manager.add_passenger_to_trip("trip_id", "passenger_id") is False


# Test MongoDB integration

def test_trip_manager_with_real_mongo(valid_trip_data):
    """Test TripManager with a real MongoDB instance."""
    mongo_uri = os.getenv("MONGO_URI", "mongodb://admin:1234@localhost:27017/test_trips_db?authSource=admin")
    client = MongoClient(mongo_uri)
    db_collection = client.get_database().get_collection("trips")

    # Clear the collection before testing
    db_collection.delete_many({})

    manager = TripManager(db_collection=db_collection)
    trip = Trip(**valid_trip_data)

    trip_id = manager.create_trip(trip)
    assert isinstance(trip_id, str)

    # Verify the trip was inserted
    inserted_trip = db_collection.find_one({"_id": trip_id})
    assert inserted_trip is not None
    assert inserted_trip["driver_id"] == valid_trip_data["driver_id"]

    # Clean up after test
    db_collection.delete_many({})
