# MediPredict

A Predictive Maintenance System for Healthcare Devices

## Overview

MediPredict is a web-based AI dashboard that helps hospital technicians and administrators upload device data, automatically predict health status, and visualize maintenance risk. The system uses machine learning to classify devices as Healthy, At Risk, or Needs Maintenance.

## Features

### Core Features
- **Data Upload Portal**: Technicians can upload device CSV/Excel files with usage, errors, and service history
- **Data Preprocessing Pipeline**: Backend cleans and normalizes uploaded data
- **Device Health Prediction**: AI model classifies devices as Healthy, At Risk, or Needs Maintenance
- **Interactive Dashboard**: Displays device performance metrics, alerts, and predicted status with color-coded charts
- **Role-Based Access**:
  - Technicians: Upload data, view alerts
  - Administrators: Monitor global statistics and performance trends
- **Report Export**: Downloadable CSV or PDF summary of predictions and equipment performance

### Technical Features
- **Frontend**: React + TailwindCSS + Recharts
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **ML/AI Layer**: Scikit-learn for model training & inference

## Project Structure

```
MediPredict/
├── backend/          # FastAPI backend
│   ├── app/          # Main application
│   ├── tests/        # Unit tests
│   ├── requirements.txt
│   └── README.md
├── frontend/         # React frontend
│   ├── src/          # Source code
│   ├── package.json
│   └── README.md
└── README.md         # This file
```

## Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables in `.env` file

5. Run the application:
   ```bash
   python run.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

### Docker Setup (Recommended)

You can also run the entire application using Docker:

1. Make sure Docker and Docker Compose are installed
2. Run the application:
   ```bash
   docker-compose up --build
   ```

This will start:
- PostgreSQL database on port 5432
- Backend API on port 8000
- Frontend on port 3000

## User Flow

1. User logs in → sees dashboard view based on role
2. Technician uploads a CSV or Excel dataset
3. Backend preprocesses data and stores it in PostgreSQL
4. ML model runs prediction on each device entry
5. Results are displayed as a color-coded device list & graphs
6. User can download summary or view historical predictions

## Data Format

To upload device data, use a CSV file with the following columns:
- `deviceId`: Unique identifier for the device
- `timestamp`: Date/time of the reading
- `usage_hours`: Total hours of device usage
- `temperature`: Device temperature in Celsius
- `pressure`: Device pressure reading
- `vibration`: Vibration level
- `error_count`: Number of errors recorded
- `error_codes`: Error codes (comma-separated)
- `maintenance_notes`: Any maintenance notes

A sample template is available in `sample_device_data_template.csv`.

## API Documentation

Once the backend server is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

- Frontend runs on http://localhost:3000
- Backend runs on http://localhost:8000
- API requests from frontend are proxied to backend