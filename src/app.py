from flask_openapi3 import OpenAPI
from src.routes import api as trip_api

# Initialize Flask app with OpenAPI
app = OpenAPI(__name__)

# Register the blueprint from routes.py
app.register_api(trip_api)

# Define a basic health check route
@app.get("/health", summary="Health Check")
def health_check():
    """Returns a 200 OK status to indicate the service is running."""
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(debug=True, port=5001)
