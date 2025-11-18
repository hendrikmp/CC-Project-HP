from datetime import datetime
from pydantic import ValidationError
import pytest

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


def test_create_invalid_trip_raises_error(valid_trip_data):
    """Test that creating an invalid trip raises a Pydantic ValidationError."""
    invalid_data = valid_trip_data.copy()
    invalid_data["capacity"] = -1  # Invalid data
    
    with pytest.raises(ValidationError):
        Trip(**invalid_data)

