import pytest
import requests
from datetime import datetime, timedelta, UTC

@pytest.fixture
def valid_trip_request_data():
    """Fixture for valid trip request data dictionary."""
    now = datetime.now(UTC)
    return {
        "passenger_id": "pass123",
        "destination": "Disneyland",
        "earliest_start_date": (now + timedelta(days=1)).isoformat(),
        "latest_start_date": (now + timedelta(days=2)).isoformat(),
    }

def test_create_and_get_trip_request(api_service, trip_requests_collection, valid_trip_request_data):
    """Test creating a trip request and then retrieving it."""
    # Create a trip request
    create_url = f"{api_service}/trips/requests"
    create_response = requests.post(create_url, json=valid_trip_request_data)
    assert create_response.status_code == 200
    request_id = create_response.json()["request_id"]

    # Get the trip request
    get_url = f"{api_service}/trips/requests/{request_id}"
    get_response = requests.get(get_url)
    assert get_response.status_code == 200
    retrieved_request = get_response.json()

    assert retrieved_request["request_id"] == request_id
    assert retrieved_request["destination"] == "Disneyland"
    assert retrieved_request["status"] == "pending"

def test_get_all_trip_requests(api_service, trip_requests_collection, valid_trip_request_data):
    """Test retrieving all trip requests."""
    # Create a trip request
    create_url = f"{api_service}/trips/requests"
    requests.post(create_url, json=valid_trip_request_data)

    # Get all trip requests
    get_url = f"{api_service}/trips/requests"
    get_response = requests.get(get_url)
    assert get_response.status_code == 200
    all_requests = get_response.json()

    assert len(all_requests) >= 1

def test_update_trip_request(api_service, trip_requests_collection, valid_trip_request_data):
    """Test updating a trip request."""
    # Create a trip request
    create_url = f"{api_service}/trips/requests"
    create_response = requests.post(create_url, json=valid_trip_request_data)
    request_id = create_response.json()["request_id"]

    # Update the trip request
    update_url = f"{api_service}/trips/requests/{request_id}"
    update_data = {"trip_id": "trip123", "status": "accepted"}
    update_response = requests.put(update_url, json=update_data)
    assert update_response.status_code == 200

    # Get the trip request to verify the update
    get_url = f"{api_service}/trips/requests/{request_id}"
    get_response = requests.get(get_url)
    retrieved_request = get_response.json()

    assert retrieved_request["status"] == "accepted"
    assert retrieved_request["trip_id"] == "trip123"
