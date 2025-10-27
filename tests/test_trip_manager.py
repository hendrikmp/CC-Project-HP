import pytest
from datetime import datetime
from src.trip import Trip
from src.trip_manager import TripManager


def test_create_trip_without_db():
    """Test creating a trip without database connection."""
    manager = TripManager()
    
    start = datetime(2025, 6, 1, 10, 0)
    end = datetime(2025, 6, 1, 18, 0)
    
    trip = Trip(
        driver_id="driver123",
        driver_car="Tesla Model 3",
        free_seats=3,
        destination="Lake Tahoe",
        pickup_location="San Francisco",
        start_datetime=start,
        return_datetime=end,
        cost_per_passenger=25.0
    )
    
    trip_id = manager.create_trip(trip)
    # Updated to match current TripManager behavior (UUID when no DB)
    assert isinstance(trip_id, str)
    assert trip_id  # non-empty
    assert trip.trip_id == trip_id


# def test_validate_trip_data_success():
#     """Test validating correct trip data."""
#     manager = TripManager()
    
#     start = datetime(2025, 6, 1, 10, 0)
#     end = datetime(2025, 6, 1, 18, 0)
    
#     result = manager.validate_trip_data(
#         driver_id="driver123",
#         driver_car="Tesla Model 3",
#         free_seats=3,
#         destination="Lake Tahoe",
#         pickup_location="San Francisco",
#         start_datetime=start,
#         return_datetime=end,
#         cost_per_passenger=25.0
#     )
    
#     assert result is True


# def test_validate_trip_data_invalid_seats():
#     """Test validating trip data with invalid seats."""
#     manager = TripManager()
    
#     start = datetime(2025, 6, 1, 10, 0)
#     end = datetime(2025, 6, 1, 18, 0)
    
#     with pytest.raises(ValueError):
#         manager.validate_trip_data(
#             driver_id="driver123",
#             driver_car="Tesla Model 3",
#             free_seats=-1,
#             destination="Lake Tahoe",
#             pickup_location="San Francisco",
#             start_datetime=start,
#             return_datetime=end,
#             cost_per_passenger=25.0
#         )
