# MediPredict Data Schema

## Database Schema

### Users
- `id`: Integer (Primary Key)
- `username`: String (Unique)
- `email`: String (Unique)
- `hashed_password`: String
- `role`: Enum (admin, technician)
- `created_at`: DateTime

### Devices
- `id`: Integer (Primary Key)
- `device_id`: String (Unique)
- `name`: String
- `type`: String
- `manufacturer`: String
- `model`: String
- `serial_number`: String (Unique)
- `installation_date`: DateTime
- `last_maintenance_date`: DateTime (Nullable)
- `status`: String (active, inactive, maintenance)
- `created_at`: DateTime
- `updated_at`: DateTime

### DeviceData
- `id`: Integer (Primary Key)
- `device_id`: String (Foreign Key to Devices)
- `timestamp`: DateTime
- `usage_hours`: Float (Nullable)
- `temperature`: Float (Nullable)
- `pressure`: Float (Nullable)
- `vibration`: Float (Nullable)
- `error_count`: Integer (Default: 0)
- `error_codes`: Text (JSON string, Nullable)
- `maintenance_notes`: Text (Nullable)
- `created_at`: DateTime

### Predictions
- `id`: Integer (Primary Key)
- `device_id`: String (Foreign Key to Devices)
- `prediction_timestamp`: DateTime
- `predicted_status`: String (healthy, at_risk, needs_maintenance)
- `confidence_score`: Float
- `features_used`: String (JSON string of features)
- `recommendation`: String (Nullable)
- `created_at`: DateTime

## CSV/Excel Upload Format

The system expects CSV or Excel files with the following columns:

- `timestamp`: Date/Time of the data point
- `usage_hours`: Number of hours the device has been used
- `temperature`: Current temperature of the device (in Celsius)
- `pressure`: Current pressure reading
- `vibration`: Vibration level
- `error_count`: Number of errors recorded
- `error_codes`: Error codes (comma-separated if multiple)
- `maintenance_notes`: Any maintenance notes

Example:
```csv
timestamp,usage_hours,temperature,pressure,vibration,error_count,error_codes,maintenance_notes
2023-06-01 08:00:00,120.5,32.1,105.2,0.15,0,,Normal operation
2023-06-01 12:00:00,124.2,33.5,107.8,0.18,1,ERR201,Minor error detected
```

## API Endpoints

### Authentication
- `POST /api/auth/token` - Login and get access token
- `POST /api/auth/register` - Register new user

### Users
- `POST /api/users/` - Create user
- `GET /api/users/{user_id}` - Get user by ID
- `GET /api/users/` - Get all users
- `PUT /api/users/{user_id}` - Update user
- `DELETE /api/users/{user_id}` - Delete user

### Devices
- `POST /api/devices/` - Create device
- `GET /api/devices/{device_id}` - Get device by ID
- `GET /api/devices/` - Get all devices
- `PUT /api/devices/{device_id}` - Update device
- `DELETE /api/devices/{device_id}` - Delete device
- `POST /api/devices/{device_id}/upload-data` - Upload device data from file

### Predictions
- `POST /api/predictions/` - Create prediction
- `GET /api/predictions/{prediction_id}` - Get prediction by ID
- `GET /api/predictions/device/{device_id}` - Get predictions for a device
- `GET /api/predictions/` - Get all predictions
- `PUT /api/predictions/{prediction_id}` - Update prediction
- `DELETE /api/predictions/{prediction_id}` - Delete prediction
- `POST /api/predictions/predict-for-device/{device_id}` - Generate prediction for a device
- `POST /api/predictions/bulk-predict` - Generate predictions for multiple devices

### ML
- `POST /api/ml/train-model` - Train the predictive model