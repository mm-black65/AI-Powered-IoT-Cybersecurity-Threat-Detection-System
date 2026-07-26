from fastapi import FastAPI
from backend.routes import router
from backend.database import (
    create_table,
    create_prediction_table
)

app = FastAPI(
    title="AI IoT Cybersecurity System",
    description="Backend API for IoT Threat Detection",
    version="1.0"
)

# Create database table
create_table()
create_prediction_table()
# Register routes
app.include_router(router)

@app.get("/")
def home():
    return {
        "status": "Running",
        "message": "Welcome to AI IoT Cybersecurity Backend"
    }