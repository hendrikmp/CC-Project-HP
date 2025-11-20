import pytest
from datetime import datetime, timedelta, UTC
from src.bll_models import TripRequest, TripRequestStatus
from src.trip_request_manager import TripRequestManager

@pytest.fixture
def valid_trip_request_data():
    """Fixture for valid trip request data dictionary."""
    now = datetime.now(UTC)
    return {
        "passenger_id": "pass123",
        "destination": "Disneyland",
        "earliest_start_date": now + timedelta(days=1),
        "latest_start_date": now + timedelta(days=2),
    }

@pytest.fixture
def mock_db_collection(mocker):
    """Fixture for a mocked MongoDB collection."""
    return mocker.MagicMock()

@pytest.fixture
def trip_request_manager(mock_db_collection):
    """Fixture for a TripRequestManager with a mocked DB collection."""
    return TripRequestManager(db_collection=mock_db_collection)

def test_create_and_get_trip_request(trip_request_manager, mock_db_collection, valid_trip_request_data):
    """Test creating a trip request and then retrieving it."""
    trip_request = TripRequest(**valid_trip_request_data)
    request_id = trip_request_manager.create_trip_request(trip_request)

    # Configure the mock to return the inserted data
    request_data_with_id = valid_trip_request_data.copy()
    request_data_with_id["request_id"] = request_id
    mock_db_collection.find_one.return_value = request_data_with_id

    retrieved_request = trip_request_manager.get_trip_request_by_id(request_id)

    mock_db_collection.insert_one.assert_called_once()
    mock_db_collection.find_one.assert_called_with({"request_id": request_id})
    
    assert retrieved_request is not None
    assert retrieved_request.request_id == request_id
    assert retrieved_request.destination == "Disneyland"

def test_get_all_trip_requests(trip_request_manager, mock_db_collection, valid_trip_request_data):
    """Test retrieving all trip requests."""
    request_data_with_id = valid_trip_request_data.copy()
    request_data_with_id["request_id"] = "req1"
    mock_db_collection.find.return_value = [request_data_with_id]

    requests = trip_request_manager.get_all_trip_requests()

    assert len(requests) == 1
    assert requests[0].request_id == "req1"
    mock_db_collection.find.assert_called_with({})

def test_get_all_trip_requests_with_filter(trip_request_manager, mock_db_collection):
    """Test retrieving trip requests with a destination filter."""
    trip_request_manager.get_all_trip_requests(destination="Disney")
    mock_db_collection.find.assert_called_with({"destination": {"$regex": "Disney", "$options": "i"}})

def test_update_trip_request(trip_request_manager, mock_db_collection):
    """Test updating a trip request."""
    request_id = "req1"
    trip_id = "trip123"
    status = TripRequestStatus.ACCEPTED

    # Simulate successful update
    mock_db_collection.update_one.return_value.modified_count = 1
    
    success = trip_request_manager.update_trip_request(request_id, trip_id, status)
    
    assert success is True
    mock_db_collection.update_one.assert_called_once()
    call_args = mock_db_collection.update_one.call_args[0]
    assert call_args[0] == {"request_id": request_id}
    assert call_args[1]["$set"]["status"] == status
    assert call_args[1]["$set"]["trip_id"] == trip_id

def test_get_trip_request_not_found(trip_request_manager, mock_db_collection):
    """Test that get_trip_request_by_id returns None if not found."""
    mock_db_collection.find_one.return_value = None
    trip_request = trip_request_manager.get_trip_request_by_id("nonexistent")
    assert trip_request is None

def test_update_trip_request_not_found(trip_request_manager, mock_db_collection):
    """Test that updating a nonexistent trip request fails."""
    mock_db_collection.update_one.return_value.modified_count = 0
    result = trip_request_manager.update_trip_request("nonexistent", "trip1", TripRequestStatus.ACCEPTED)
    assert result is False
