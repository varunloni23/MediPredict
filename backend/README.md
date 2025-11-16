# MediPredict Backend

This is the backend API for the MediPredict system, built with FastAPI.

## Features

- User authentication (JWT)
- Device management
- Device data upload (CSV/Excel)
- Predictive maintenance model integration
- Role-based access control

## Tech Stack

- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **ML Library**: Scikit-learn
- **Authentication**: JWT

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables in `.env` file

4. Run the application:
   ```bash
   python run.py
   ```

## API Documentation

Once the server is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── api/          # API routes
│   ├── crud/         # Database operations
│   ├── database/     # Database configuration
│   ├── ml/           # Machine learning models
│   ├── models/       # Database models
│   ├── schemas/      # Pydantic schemas
│   ├── auth.py       # Authentication utilities
│   └── main.py       # Main application
├── tests/            # Unit tests
├── requirements.txt  # Dependencies
├── run.py            # Application entry point
└── .env              # Environment variables
```