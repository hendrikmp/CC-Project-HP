import pytest
from datetime import datetime
from src.bll_models import Trip
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

@pytest.fixture
def mock_db_collection(mocker):
    """Fixture for a mocked MongoDB collection."""
    return mocker.MagicMock()

@pytest.fixture
def trip_manager(mock_db_collection):
    """Fixture for a TripManager with a mocked DB collection."""
    return TripManager(db_collection=mock_db_collection)

def test_create_and_get_trip(trip_manager, mock_db_collection, valid_trip_data):
    """Test creating a trip and then retrieving it from the mocked DB."""
    trip = Trip(**valid_trip_data)
    trip_id = trip_manager.create_trip(trip)

    # Configure the mock to return the inserted data
    trip_data_with_id = valid_trip_data.copy()
    trip_data_with_id["trip_id"] = trip_id
    mock_db_collection.find_one.return_value = trip_data_with_id

    retrieved_trip = trip_manager.get_trip_by_id(trip_id)

    mock_db_collection.insert_one.assert_called_once()
    mock_db_collection.find_one.assert_called_with({"trip_id": trip_id})
    
    assert retrieved_trip is not None
    assert retrieved_trip.trip_id == trip_id
    assert retrieved_trip.destination == "Lake Tahoe"

def test_add_passenger_integration(trip_manager, mock_db_collection):
    """Test adding a passenger via the trip manager."""
    trip_id = "trip1"
    passenger_id = "pass1"

    # Simulate successful update
    mock_db_collection.update_one.return_value.modified_count = 1
    
    success = trip_manager.add_passenger_to_trip(trip_id, passenger_id)
    
    assert success is True
    mock_db_collection.update_one.assert_called_once()

def test_delete_trip_integration(trip_manager, mock_db_collection):
    """Test deleting a trip via the trip manager."""
    trip_id = "trip1"

    # Simulate successful deletion
    mock_db_collection.delete_one.return_value.deleted_count = 1

    success = trip_manager.delete_trip(trip_id)

    assert success is True
    mock_db_collection.delete_one.assert_called_with({"trip_id": trip_id})


def test_get_all_trips(trip_manager, mock_db_collection, valid_trip_data):
    """Test retrieving all trips from the mocked DB."""
    trip_data_with_id = valid_trip_data.copy()
    trip_data_with_id["trip_id"] = "trip1"
    mock_db_collection.find.return_value = [trip_data_with_id]

    trips = trip_manager.get_all_trips()

    assert len(trips) == 1
    assert trips[0].trip_id == "trip1"
    mock_db_collection.find.assert_called_with({})


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


def test_get_trip_by_id_not_found(trip_manager, mock_db_collection):
    """Test that get_trip_by_id returns None if the trip is not found."""
    mock_db_collection.find_one.return_value = None
    trip = trip_manager.get_trip_by_id("nonexistent")
    assert trip is None


def test_add_passenger_full_or_duplicate(trip_manager, mock_db_collection):
    """Test adding a passenger fails if the trip is full or the passenger is a duplicate."""
    mock_db_collection.update_one.return_value.modified_count = 0
    result = trip_manager.add_passenger_to_trip("trip1", "passenger1")
    assert result is False


def test_delete_trip_not_found(trip_manager, mock_db_collection):
    """Test deleting a trip that does not exist."""
    mock_db_collection.delete_one.return_value.deleted_count = 0
    result = trip_manager.delete_trip("nonexistent")
    assert result is False
