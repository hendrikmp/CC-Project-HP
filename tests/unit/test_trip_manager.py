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


def test_create_invalid_trip_raises_error(valid_trip_data):
    """Test that creating an invalid trip raises a Pydantic ValidationError."""
    invalid_data = valid_trip_data.copy()
    invalid_data["capacity"] = -1  # Invalid data
    
    with pytest.raises(ValidationError):
        Trip(**invalid_data)


def test_get_all_trips_no_db():
    """Test retrieving trips when no database is configured."""
    manager = TripManager()
    trips = manager.get_all_trips()
    assert trips == []


def test_add_passenger_to_trip_no_db():
    """Test adding a passenger returns False if no DB is configured."""
    manager = TripManager()
    assert manager.add_passenger_to_trip("trip1", "p1") is False


def test_delete_trip_no_db():
    """Test that deleting a trip returns False if no DB is configured."""
    manager = TripManager()
    assert manager.delete_trip("trip1") is False


def test_get_all_trips_no_db():
    """Test retrieving trips when no database is configured."""
    manager = TripManager()
    trips = manager.get_all_trips()
    assert trips == []


def test_add_passenger_to_trip_no_db():
    """Test adding a passenger returns False if no DB is configured."""
    manager = TripManager()
    assert manager.add_passenger_to_trip("trip1", "p1") is False


def test_delete_trip_no_db():
    """Test that deleting a trip returns False if no DB is configured."""
    manager = TripManager()
    assert manager.delete_trip("trip1") is False

