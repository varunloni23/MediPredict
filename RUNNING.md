# How to Run MediPredict

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- PostgreSQL database
- Docker (optional, for containerized deployment)

## Quick Start with Docker (Recommended)

1. Make sure Docker and Docker Compose are installed
2. Run the application:
   ```bash
   docker-compose up --build
   ```

This will start all services:
- PostgreSQL database on port 5432
- Backend API on port 8000
- Frontend on port 3000

Visit http://localhost:3000 to access the application.

## Manual Setup

### Backend

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

4. Set up environment variables in `.env` file:
   ```bash
   # Database configuration
   DATABASE_URL=postgresql://user:password@localhost/mediapredict
   
   # Security
   SECRET_KEY=your-super-secret-jwt-key-here-change-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. Initialize the database:
   ```bash
   python init_db.py
   ```

6. (Optional) Generate sample data:
   ```bash
   python generate_sample_data.py
   ```

7. (Optional) Train the model:
   ```bash
   python train_model.py
   ```

8. Run the application:
   ```bash
   python run.py
   ```

The backend will be available at http://localhost:8000

### Frontend

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

The frontend will be available at http://localhost:3000

## Running Tests

### Backend Tests

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Run tests:
   ```bash
   pytest
   ```

## API Documentation

Once the backend server is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Demo Script

To run the demo workflow:
```bash
python demo.py
```

This will show the complete workflow of the system without needing to start the web servers.