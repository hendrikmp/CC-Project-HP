from flask_openapi3 import OpenAPI
from flask_cors import CORS
from src.routes import api as trip_api
from flask import request

import os
from pymongo import MongoClient
from src.trip_manager import TripManager
from src.trip_request_manager import TripRequestManager
from shared.logging_config import setup_logger, register_logging_handlers


# Initialize a logger for the trips service
app_logger = setup_logger('trips-ms')


# Initialize Flask app with OpenAPI
app = OpenAPI(__name__)
CORS(app)

# Register shared logging and error handlers
register_logging_handlers(app, app_logger)

# Register the blueprint from routes.py
app.register_api(trip_api)

# Initialize MongoDB client and inject into TripManager
mongo_uri = os.getenv("MONGO_URI", "mongodb://trips-db:27017/trips_db")
mongo_client = MongoClient(mongo_uri)
db = mongo_client.get_database()

trips_collection = db.get_collection("trips")
trip_requests_collection = db.get_collection("trip_requests")

trip_manager = TripManager(db_collection=trips_collection)
trip_request_manager = TripRequestManager(db_collection=trip_requests_collection)

app.config["trip_manager"] = trip_manager
app.config["trip_request_manager"] = trip_request_manager

# Define a basic health check route
@app.get("/health", summary="Health Check")
def health_check():
    """Returns a 200 OK status to indicate the service is running."""
    return {"status": "ok"}, 200


if __name__ == "__main__":
    # Get PORT from Render (default to 5001 if local)
    port = int(os.environ.get("PORT", 5001))
    
    # Get DEBUG mode (False in production for security)
    debug = os.environ.get("FLASK_ENV") != "production"

    # host='0.0.0.0' allows external access
    app.run(host='0.0.0.0', port=port, debug=debug)
