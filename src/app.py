from flask_openapi3 import OpenAPI
from src.routes import api as trip_api
from flask import request

import os
from pymongo import MongoClient
from src.trip_manager import TripManager
from shared.logging_config import setup_logger, register_logging_handlers


# Initialize a logger for the trips service
app_logger = setup_logger('trips-ms')


# Initialize Flask app with OpenAPI
app = OpenAPI(__name__)

# Register shared logging and error handlers
register_logging_handlers(app, app_logger)

# Register the blueprint from routes.py
app.register_api(trip_api)

# Initialize MongoDB client and inject into TripManager
mongo_uri = os.getenv("MONGO_URI", "mongodb://trips-db:27017/trips_db")
mongo_client = MongoClient(mongo_uri)
db_collection = mongo_client.get_database().get_collection("trips")

trip_manager = TripManager(db_collection=db_collection)
app.config["trip_manager"] = trip_manager

# Define a basic health check route
@app.get("/health", summary="Health Check")
def health_check():
    """Returns a 200 OK status to indicate the service is running."""
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(debug=True, port=5001)
