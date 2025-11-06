from datetime import datetime
from pydantic import ValidationError
import pytest

from src.trip import Trip
from src.trip_manager import TripManager


@pytest.fixture
def valid_trip_data():
    """Fixture for valid trip data dictionary."""
    return {
        "driver_id": "driver123",
        "driver_car": "Tesla Model 3",
        "free_seats": 3,
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
    mock_collection.insert_one.return_value.inserted_id = "mock_trip_id"
    
    manager = TripManager(db_collection=mock_collection)
    trip = Trip(**valid_trip_data)
    
    trip_id = manager.create_trip(trip)
    
    assert trip_id == "mock_trip_id"
    # Verify that model_dump() was called and the dict was inserted
    mock_collection.insert_one.assert_called_once()
    # Check that trip_id was removed before insertion, as Mongo creates it
    inserted_dict = mock_collection.insert_one.call_args[0][0]
    assert "trip_id" not in inserted_dict


def test_create_invalid_trip_raises_error(valid_trip_data):
    """Test that creating an invalid trip raises a Pydantic ValidationError."""
    manager = TripManager()
    invalid_data = valid_trip_data.copy()
    invalid_data["free_seats"] = -1  # Invalid data
    
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
            "free_seats": 2,
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
