from flask_openapi3 import OpenAPI
from src.trip_manager import TripManager

# Initialize Flask app with OpenAPI
app = OpenAPI(__name__)

# In a real app, you'd inject this dependency, e.g., using a factory
# or a dedicated dependency injection library. For now, we instantiate it directly.
trip_manager = TripManager()

# Define a basic health check route
@app.get("/health", summary="Health Check")
def health_check():
    """Returns a 200 OK status to indicate the service is running."""
    return {"status": "ok"}, 200

# The following is for local development and will be executed when
# you run `python src/app.py`. In production, a WSGI server like Gunicorn
# would run the 'app' object.
if __name__ == "__main__":
    app.run(debug=True, port=5001)
