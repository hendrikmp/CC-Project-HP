import requests
from datetime import datetime, timedelta

def test_health_check(api_service):
    """Test that the health check endpoint is working."""
    response = requests.get(f"{api_service}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_and_get_trip(api_service, db_collection):
    """Test creating a trip and then retrieving it via the API."""
    start_time = datetime.now()
    trip_data = {
        "trip_id": "trip1",
        "driver_id": "api_driver",
        "driver_car": "DeLorean",
        "capacity": 2,
        "destination": "The Future",
        "pickup_location": "Hill Valley",
        "start_datetime": start_time.isoformat(),
        "return_datetime": (start_time + timedelta(days=1)).isoformat(),
        "cost_per_passenger": 100.0,
    }

    # 1. Create a trip
    create_response = requests.post(f"{api_service}/trips/", json=trip_data)

    assert create_response.status_code == 200
    trip_id = create_response.json()["trip_id"]
    assert isinstance(trip_id, str)

    # 2. Retrieve the trip to verify it was created
    get_response = requests.get(f"{api_service}/trips/{trip_id}")
    assert get_response.status_code == 200
    retrieved_trip = get_response.json()
    
    assert retrieved_trip["trip_id"] == trip_id
    assert retrieved_trip["destination"] == "The Future"
    assert retrieved_trip["driver_id"] == "api_driver"

    # 3. Verify it's in the database directly
    db_trip = db_collection.find_one({"trip_id": trip_id})
    assert db_trip is not None
    assert db_trip["destination"] == "The Future"

def test_get_all_trips(api_service, db_collection):
    """Test listing all trips."""
    # Insert two trips directly into the DB for this test
    start_time = datetime.now()
    trip1 = {
        "trip_id": "trip1",
        "driver_id": "api_driver",
        "driver_car": "DeLorean",
        "capacity": 2,
        "destination": "The Future",
        "pickup_location": "Hill Valley",
        "start_datetime": start_time,
        "return_datetime": (start_time + timedelta(days=1)),
        "cost_per_passenger": 100.0,
        "passengers": []
    }
    trip2 = {
        "trip_id": "trip2",
        "driver_id": "api_driver2",
        "driver_car": "DeLorean",
        "capacity": 2,
        "destination": "The Future",
        "pickup_location": "Hill Valley",
        "start_datetime": start_time,
        "return_datetime": (start_time + timedelta(days=1)),
        "cost_per_passenger": 100.0,
        "passengers": []
    }
    db_collection.insert_many([trip1, trip2])

    # Get all trips via the API
    response = requests.get(f"{api_service}/trips/")

    print(response.status_code)
    print(response.text)


    assert response.status_code == 200
    trips = response.json()

    assert len(trips) == 2
    trip_ids = {t["trip_id"] for t in trips}
    assert trip_ids == {"trip1", "trip2"}

def test_join_trip(api_service, db_collection):
    """Test joining a trip."""
    # Insert a trip to join
    start_time = datetime.now()
    trip_id = "joinable_trip"
    trip = {
        "trip_id": trip_id, "driver_id": "d1", "destination": "Dest1",
        "pickup_location": "Pick1", "capacity": 1, "passengers": [],
        "start_datetime": start_time, "return_datetime": (start_time + timedelta(days=1)),
        "cost_per_passenger": 10.0, "driver_car": "Golf",
    }
    db_collection.insert_one(trip)

    # Join the trip
    join_response = requests.post(f"{api_service}/trips/{trip_id}/join", json={"passenger_id": "pass1"})
    assert join_response.status_code == 200

    # Verify passenger was added in the DB
    db_trip = db_collection.find_one({"trip_id": trip_id})
    assert "pass1" in db_trip["passengers"]

def test_delete_trip(api_service, db_collection):
    """Test deleting a trip."""
    # Insert a trip to delete
    start_time = datetime.now()
    trip_id = "deletable_trip"
    trip = {
        "trip_id": trip_id, "driver_id": "d1", "destination": "Dest1",
        "pickup_location": "Pick1", "capacity": 1, "passengers": [],
        "start_datetime": start_time, "return_datetime": (start_time + timedelta(days=1)),
        "cost_per_passenger": 10.0, "driver_car": "Golf",
    }
    db_collection.insert_one(trip)

    # Delete the trip
    delete_response = requests.delete(f"{api_service}/trips/{trip_id}")
    assert delete_response.status_code == 200

    # Verify it's gone from the DB
    db_trip = db_collection.find_one({"trip_id": trip_id})
    assert db_trip is None
