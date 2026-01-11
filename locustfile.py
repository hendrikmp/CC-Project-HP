from locust import HttpUser, task, between
from uuid import uuid4

class ViewerUser(HttpUser):
    # Wait between 1 and 3 seconds between tasks (simulates real human behavior)
    wait_time = between(1, 3)

    @task(1)
    def view_trips(self):
        """Simulates a user loading the main page (GET request)"""
        self.client.get("/trips")
        self.client.get("/trips/requests")

class CreatorUser(HttpUser):
    wait_time = between(5, 10)
    
    @task(2)
    def create_trip(self):
        """Simulates a user creating a trip (POST request)"""
        # Sending random data to avoid "duplicate" errors if your backend checks
        payload = {
            "capacity": 1,
            "cost_per_passenger": 0,
            "destination": "test",
            "driver_car": "test",
            "driver_id": str(uuid4()),
            "pickup_location": "test",
            "return_datetime": "2026-01-11T16:00:21.335Z",
            "start_datetime": "2026-01-10T16:00:21.335Z"
            }
        
        # Note: We assume your backend route is /trips/requests based on previous chats
        # Adjust the URL string if your route is different
        self.client.post("/trips", json=payload)

    @task(1)
    def create_trip_request(self):
        """Simulates a user creating a trip (POST request)"""
        # Sending random data to avoid "duplicate" errors if your backend checks
        payload = {
            "destination": "test",
            "earliest_start_date": "2026-01-10T16:31:20.768Z",
            "latest_start_date": "2026-01-11T16:31:20.768Z",
            "passenger_id": str(uuid4())
        }
        
        # Note: We assume your backend route is /trips/requests based on previous chats
        # Adjust the URL string if your route is different
        self.client.post("/trips/requests", json=payload)