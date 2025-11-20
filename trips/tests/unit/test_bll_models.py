import pytest
from pydantic import ValidationError
from datetime import datetime, timedelta, timezone
from src.bll_models import Trip, TripRequest, TripRequestStatus


def test_create_valid_trip():
    """Test creating a trip with valid data."""
    start = datetime(2025, 6, 1, 10, 0)
    end = datetime(2025, 6, 1, 18, 0)
    
    trip = Trip(
        driver_id="driver123",
        driver_car="Tesla Model 3",
        capacity=3,
        destination="Lake Tahoe",
        pickup_location="San Francisco Downtown",
        start_datetime=start,
        return_datetime=end,
        cost_per_passenger=25.50
    )
    
    assert trip.driver_id == "driver123"
    assert trip.driver_car == "Tesla Model 3"
    assert trip.capacity == 3
    assert trip.destination == "Lake Tahoe"
    assert trip.pickup_location == "San Francisco Downtown"
    assert trip.cost_per_passenger == 25.50
    assert trip.passengers == []


def test_trip_negative_seats_raises_error():
    """Test that negative capacity raises ValueError."""
    start = datetime(2025, 6, 1, 10, 0)
    end = datetime(2025, 6, 1, 18, 0)
    
    with pytest.raises(ValidationError, match="capacity must be positive"):
        Trip(
            driver_id="driver123",
            driver_car="Tesla Model 3",
            capacity=-1,
            destination="Lake Tahoe",
            pickup_location="San Francisco",
            start_datetime=start,
            return_datetime=end,
            cost_per_passenger=25.0
        )


def test_trip_zero_seats_raises_error():
    """Test that zero capacity raises ValueError."""
    start = datetime(2025, 6, 1, 10, 0)
    end = datetime(2025, 6, 1, 18, 0)
    
    with pytest.raises(ValidationError, match="capacity must be positive"):
        Trip(
            driver_id="driver123",
            driver_car="Tesla Model 3",
            capacity=0,
            destination="Lake Tahoe",
            pickup_location="San Francisco",
            start_datetime=start,
            return_datetime=end,
            cost_per_passenger=25.0
        )


def test_trip_passengers_exceed_seats_raises_error():
    """Test that passengers list exceeding capacity raises ValueError."""
    start = datetime(2025, 6, 1, 10, 0)
    end = datetime(2025, 6, 1, 18, 0)
    
    with pytest.raises(ValidationError, match="exceeds capacity"):
        Trip(
            driver_id="driver123",
            driver_car="Tesla Model 3",
            capacity=2,
            destination="Lake Tahoe",
            pickup_location="San Francisco",
            start_datetime=start,
            return_datetime=end,
            cost_per_passenger=25.0,
            passengers=["pass1", "pass2", "pass3"]
        )


def test_trip_invalid_datetime_raises_error():
    """Test that return_datetime before start_datetime raises ValueError."""
    start = datetime(2025, 6, 1, 18, 0)
    end = datetime(2025, 6, 1, 10, 0)
    
    with pytest.raises(ValidationError, match="return_datetime must be after start_datetime"):
        Trip(
            driver_id="driver123",
            driver_car="Tesla Model 3",
            capacity=3,
            destination="Lake Tahoe",
            pickup_location="San Francisco",
            start_datetime=start,
            return_datetime=end,
            cost_per_passenger=25.0
        )


def test_trip_negative_cost_raises_error():
    """Test that negative cost_per_passenger raises ValueError."""
    start = datetime(2025, 6, 1, 10, 0)
    end = datetime(2025, 6, 1, 18, 0)
    
    with pytest.raises(ValidationError, match="cost_per_passenger cannot be negative"):
        Trip(
            driver_id="driver123",
            driver_car="Tesla Model 3",
            capacity=3,
            destination="Lake Tahoe",
            pickup_location="San Francisco",
            start_datetime=start,
            return_datetime=end,
            cost_per_passenger=-10.0
        )


def test_add_passenger_success():
    """Test successfully adding a passenger."""
    start = datetime(2025, 6, 1, 10, 0)
    end = datetime(2025, 6, 1, 18, 0)
    
    trip = Trip(
        driver_id="driver123",
        driver_car="Tesla Model 3",
        capacity=3,
        destination="Lake Tahoe",
        pickup_location="San Francisco",
        start_datetime=start,
        return_datetime=end,
        cost_per_passenger=25.0
    )
    
    result = trip.add_passenger("passenger1")
    assert result is True
    assert "passenger1" in trip.passengers
    assert len(trip.passengers) == 1


def test_add_passenger_when_full():
    """Test adding passenger when trip is full."""
    start = datetime(2025, 6, 1, 10, 0)
    end = datetime(2025, 6, 1, 18, 0)
    
    trip = Trip(
        driver_id="driver123",
        driver_car="Tesla Model 3",
        capacity=1,
        destination="Lake Tahoe",
        pickup_location="San Francisco",
        start_datetime=start,
        return_datetime=end,
        cost_per_passenger=25.0,
        passengers=["passenger1"]
    )
    
    result = trip.add_passenger("passenger2")
    assert result is False
    assert len(trip.passengers) == 1


def test_add_duplicate_passenger_raises_error():
    """Test adding same passenger twice raises ValueError."""
    start = datetime(2025, 6, 1, 10, 0)
    end = datetime(2025, 6, 1, 18, 0)
    
    trip = Trip(
        driver_id="driver123",
        driver_car="Tesla Model 3",
        capacity=3,
        destination="Lake Tahoe",
        pickup_location="San Francisco",
        start_datetime=start,
        return_datetime=end,
        cost_per_passenger=25.0
    )
    
    trip.add_passenger("passenger1")
    
    with pytest.raises(ValueError, match="already in this trip"):
        trip.add_passenger("passenger1")


def test_trip_to_dict():
    """Test converting trip to dictionary format."""
    start = datetime(2025, 6, 1, 10, 0)
    end = datetime(2025, 6, 1, 18, 0)
    
    trip = Trip(
        driver_id="driver123",
        driver_car="Tesla Model 3",
        capacity=3,
        destination="Lake Tahoe",
        pickup_location="San Francisco",
        start_datetime=start,
        return_datetime=end,
        cost_per_passenger=25.0,
        trip_id="trip456"
    )
    
    trip_dict = trip.to_dict()
    
    assert trip_dict["trip_id"] == "trip456"
    assert trip_dict["driver_id"] == "driver123"
    assert trip_dict["capacity"] == 3
    assert trip_dict["passengers"] == []


def test_create_valid_trip_request():
    """Test creating a trip request with valid data."""
    now = datetime.now(timezone.utc)
    trip_request = TripRequest(
        passenger_id="pass123",
        destination="Disneyland",
        earliest_start_date=now + timedelta(days=1),
        latest_start_date=now + timedelta(days=2),
    )
    assert trip_request.passenger_id == "pass123"
    assert trip_request.destination == "Disneyland"
    assert trip_request.status == TripRequestStatus.PENDING
    assert trip_request.trip_id is None


def test_trip_request_invalid_dates_raises_error():
    """Test that latest_start_date before earliest_start_date raises an error."""
    now = datetime.now(timezone.utc)
    with pytest.raises(ValidationError, match="latest_start_date must be after earliest_start_date"):
        TripRequest(
            passenger_id="pass123",
            destination="Disneyland",
            earliest_start_date=now + timedelta(days=2),
            latest_start_date=now + timedelta(days=1),
        )


def test_trip_request_same_dates_raises_error():
    """Test that latest_start_date same as earliest_start_date raises an error."""
    now = datetime.now(timezone.utc)
    with pytest.raises(ValidationError, match="latest_start_date must be after earliest_start_date"):
        TripRequest(
            passenger_id="pass123",
            destination="Disneyland",
            earliest_start_date=now,
            latest_start_date=now,
        )


def test_trip_request_to_dict():
    """Test converting a trip request to a dictionary."""
    now = datetime.now(timezone.utc)
    trip_request = TripRequest(
        request_id="req123",
        passenger_id="pass123",
        destination="Disneyland",
        earliest_start_date=now + timedelta(days=1),
        latest_start_date=now + timedelta(days=2),
        status=TripRequestStatus.ACCEPTED,
        trip_id="trip456"
    )
    
    request_dict = trip_request.to_dict()
    
    assert request_dict["request_id"] == "req123"
    assert request_dict["passenger_id"] == "pass123"
    assert request_dict["destination"] == "Disneyland"
    assert request_dict["status"] == "accepted"
    assert request_dict["trip_id"] == "trip456"
    assert isinstance(request_dict["created_at"], datetime)
    assert isinstance(request_dict["updated_at"], datetime)
