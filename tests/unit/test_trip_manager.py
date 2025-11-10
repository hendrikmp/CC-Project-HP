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


def test_create_trip_with_db(valid_trip_data, mocker):
    """Test creating a trip with a mocked database connection."""
    mock_collection = mocker.MagicMock()
    
    manager = TripManager(db_collection=mock_collection)
    trip = Trip(**valid_trip_data)
    
    trip_id = manager.create_trip(trip)
    
    # Verify an insert occurred
    mock_collection.insert_one.assert_called_once()
    
    # Check that trip_id was set on the trip object and returned
    assert trip.trip_id is not None
    assert trip_id == trip.trip_id
    
    # Check that the dictionary passed to insert_one has the trip_id
    inserted_dict = mock_collection.insert_one.call_args[0][0]
    assert inserted_dict["trip_id"] == trip_id


def test_create_invalid_trip_raises_error(valid_trip_data):
    """Test that creating an invalid trip raises a Pydantic ValidationError."""
    invalid_data = valid_trip_data.copy()
    invalid_data["capacity"] = -1  # Invalid data
    
    with pytest.raises(ValidationError):
        Trip(**invalid_data)


def test_get_all_trips_with_db(mocker, valid_trip_data):
    """Test retrieving all trips from a mocked database."""
    mock_collection = mocker.MagicMock()
    trip_data = valid_trip_data.copy()
    trip_data["trip_id"] = "trip1"
    mock_collection.find.return_value = [trip_data]
    
    manager = TripManager(db_collection=mock_collection)
    trips = manager.get_all_trips()
    
    assert len(trips) == 1
    assert isinstance(trips[0], Trip)
    assert trips[0].trip_id == "trip1"
    assert trips[0].driver_id == valid_trip_data["driver_id"]


def test_get_all_trips_no_db():
    """Test retrieving trips when no database is configured."""
    manager = TripManager()
    trips = manager.get_all_trips()
    assert trips == []


def test_get_all_trips_with_filters(mocker, valid_trip_data):
    """Test retrieving trips with various filters."""
    mock_collection = mocker.MagicMock()
    manager = TripManager(db_collection=mock_collection)

    # Test with pickup filter
    manager.get_all_trips(pickup="San")
    mock_collection.find.assert_called_with({"pickup_location": {"$regex": "San", "$options": "i"}})

    # Test with destination filter
    manager.get_all_trips(destination="Tahoe")
    mock_collection.find.assert_called_with({"destination": {"$regex": "Tahoe", "$options": "i"}})

    # Test with date filter
    trip_date = datetime(2025, 6, 1)
    day_start = datetime(2025, 6, 1, 0, 0, 0)
    day_end = day_start.replace(hour=23, minute=59, second=59, microsecond=999999)
    manager.get_all_trips(trip_date=trip_date)
    mock_collection.find.assert_called_with({"start_datetime": {"$gte": day_start, "$lte": day_end}})

    # Test with all filters combined
    manager.get_all_trips(pickup="SF", destination="LA", trip_date=trip_date)
    mock_collection.find.assert_called_with({
        "pickup_location": {"$regex": "SF", "$options": "i"},
        "destination": {"$regex": "LA", "$options": "i"},
        "start_datetime": {"$gte": day_start, "$lte": day_end},
    })


def test_get_trip_by_id(mocker, valid_trip_data):
    """Test retrieving a single trip by its ID."""
    mock_collection = mocker.MagicMock()
    trip_data = valid_trip_data.copy()
    trip_data["trip_id"] = "trip123"
    mock_collection.find_one.return_value = trip_data
    
    manager = TripManager(db_collection=mock_collection)
    trip = manager.get_trip_by_id("trip123")
    
    assert trip is not None
    assert trip.trip_id == "trip123"
    mock_collection.find_one.assert_called_with({"trip_id": "trip123"})


def test_get_trip_by_id_not_found(mocker):
    """Test that get_trip_by_id returns None if the trip is not found."""
    mock_collection = mocker.MagicMock()
    mock_collection.find_one.return_value = None
    
    manager = TripManager(db_collection=mock_collection)
    trip = manager.get_trip_by_id("nonexistent")
    
    assert trip is None


def test_add_passenger_to_trip(mocker):
    """Test adding a passenger to a trip successfully."""
    mock_collection = mocker.MagicMock()
    mock_collection.update_one.return_value.modified_count = 1
    
    manager = TripManager(db_collection=mock_collection)
    result = manager.add_passenger_to_trip("trip1", "passenger1")
    
    assert result is True
    mock_collection.update_one.assert_called_once()


def test_add_passenger_to_trip_full_or_duplicate(mocker):
    """Test adding a passenger fails if the trip is full or the passenger is a duplicate."""
    mock_collection = mocker.MagicMock()
    mock_collection.update_one.return_value.modified_count = 0
    
    manager = TripManager(db_collection=mock_collection)
    result = manager.add_passenger_to_trip("trip1", "passenger1")
    
    assert result is False


def test_add_passenger_to_trip_no_db():
    """Test adding a passenger returns False if no DB is configured."""
    manager = TripManager()
    assert manager.add_passenger_to_trip("trip1", "p1") is False


def test_delete_trip(mocker):
    """Test deleting a trip successfully."""
    mock_collection = mocker.MagicMock()
    mock_collection.delete_one.return_value.deleted_count = 1
    
    manager = TripManager(db_collection=mock_collection)
    result = manager.delete_trip("trip1")
    
    assert result is True
    mock_collection.delete_one.assert_called_with({"trip_id": "trip1"})


def test_delete_trip_not_found(mocker):
    """Test deleting a trip that does not exist."""
    mock_collection = mocker.MagicMock()
    mock_collection.delete_one.return_value.deleted_count = 0
    
    manager = TripManager(db_collection=mock_collection)
    result = manager.delete_trip("nonexistent")
    
    assert result is False


def test_delete_trip_no_db():
    """Test that deleting a trip returns False if no DB is configured."""
    manager = TripManager()
    assert manager.delete_trip("trip1") is False

