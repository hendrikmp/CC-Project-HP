from flask_openapi3 import OpenAPI
from flask_cors import CORS
from src.routes import api as trip_api
from flask import request

import os
import sentry_sdk
from pymongo import MongoClient
from src.trip_manager import TripManager
from src.trip_request_manager import TripRequestManager
from shared.logging_config import setup_logger, register_logging_handlers

# Initialize Sentry for error tracking and performance monitoring
sentry_sdk.init(
    dsn="https://20baf1054278cb308fa5d05f65d527a2@o4510682372964352.ingest.de.sentry.io/4510682377420880",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    # Enable sending logs to Sentry
    enable_logs=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
)


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
db = mongo_client.get_database("trips_db")

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

@app.route('/debug-sentry')
def trigger_error():
    1 / 0
    return "This will never run"


if __name__ == "__main__":
    # Get PORT from Render (default to 5001 if local)
    port = int(os.environ.get("PORT", 5001))
    
    # Get DEBUG mode (False in production for security)
    debug = os.environ.get("FLASK_ENV") != "production"

    # host='0.0.0.0' allows external access
    app.run(host='0.0.0.0', port=port, debug=debug)
