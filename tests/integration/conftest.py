import pytest
import subprocess
import time
import requests
from requests.exceptions import ConnectionError
import os
from pymongo import MongoClient

@pytest.fixture(scope="session")
def api_service():
    """
    Fixture to start and stop the Docker Compose services for the API.
    Waits for the API to be healthy before yielding the base URL.
    """
    # Use the directory of the current file to find docker-compose.yml
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    docker_compose_path = os.path.join(project_root, 'docker-compose.yml')
    
    api_url = "http://localhost:5001"
    
    try:
        # Start services
        subprocess.run(
            ["docker", "compose", "-f", docker_compose_path, "up", "-d"],
            check=True,
            capture_output=True
        )
        
        # Wait for the API to be healthy
        health_url = f"{api_url}/health"
        retries = 15
        delay = 2  # seconds
        for i in range(retries):
            try:
                response = requests.get(health_url)
                if response.status_code == 200:
                    print("API is healthy.")
                    break
            except ConnectionError:
                print(f"Waiting for API to be healthy... (attempt {i+1}/{retries})")
                time.sleep(delay)
        else:
            pytest.fail("API did not become healthy in time.")
            
        yield api_url
        
    finally:
        subprocess.run(
            ["docker", "compose", "-f", docker_compose_path, "down"],
            capture_output=True,
            check=False
        )

@pytest.fixture(scope="function")
def db_collection(api_service):
    """
    Fixture to get a MongoDB collection and clean it before each test.
    Depends on the api_service to ensure containers are running.
    """
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/trips_db")
    client = MongoClient(mongo_uri)
    db = client.get_database()
    collection = db.get_collection("trips")
    
    # Clean the collection before the test
    collection.delete_many({})
    
    yield collection
    
    # The database will be torn down with the container, but if we wanted
    # to clean up after each test, we could do it here.
    # collection.delete_many({})

@pytest.fixture(scope="function")
def trip_requests_collection(api_service):
    """
    Fixture to get a MongoDB collection for trip requests and clean it before each test.
    """
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/trips_db")
    client = MongoClient(mongo_uri)
    db = client.get_database()
    collection = db.get_collection("trip_requests")
    
    # Clean the collection before the test
    collection.delete_many({})
    
    yield collection
