from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import users, devices, predictions, auth, ml, reports
from app.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MediPredict API",
    description="Predictive Maintenance System for Healthcare Devices",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(devices.router, prefix="/api/devices", tags=["devices"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["predictions"])
app.include_router(ml.router, prefix="/api/ml", tags=["ml"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])

@app.get("/")
async def root():
    return {"message": "Welcome to MediPredict API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}