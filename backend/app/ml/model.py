import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
from datetime import datetime
from typing import List, Tuple, Optional, Any

class DeviceHealthPredictor:
    def __init__(self):
        self.model: Optional[RandomForestClassifier] = None
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def preprocess_data(self, df: pd.DataFrame) -> Any:
        """
        Preprocess the device data for training or prediction
        """
        # Handle missing values
        df = df.fillna(0)
        
        # Select features for prediction
        feature_columns = ['usage_hours', 'temperature', 'pressure', 'vibration', 'error_count']
        
        # Ensure all feature columns exist
        for col in feature_columns:
            if col not in df.columns:
                df[col] = 0
        
        X = df[feature_columns]
        
        # Scale features
        if not self.is_trained:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = self.scaler.transform(X)
            
        return X_scaled
    
    def train(self, df: pd.DataFrame, target_column: str = 'health_status'):
        """
        Train the model with provided data
        Expected target values: 'healthy', 'at_risk', 'needs_maintenance'
        """
        # Preprocess data
        X = self.preprocess_data(df)
        
        # Prepare target variable
        y = df[target_column]
        
        # Convert string labels to numeric
        def map_labels(label):
            label_mapping = {'healthy': 0, 'at_risk': 1, 'needs_maintenance': 2}
            return label_mapping.get(label, 0)
        
        y_numeric = y.apply(map_labels)
        
        # Train model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, y_numeric)
        
        self.is_trained = True
        
        # Save model
        self.save_model()
        
        return self.model
    
    def predict(self, df: pd.DataFrame) -> List[Tuple[str, float, str]]:
        """
        Predict device health status
        Returns: list of predictions with confidence scores
        """
        if not self.is_trained or self.model is None:
            # Try to load a pre-trained model
            if not self.load_model():
                raise Exception("Model not trained and no saved model found")
        
        # Preprocess data
        X = self.preprocess_data(df)
        
        # Make predictions
        if self.model is not None:
            predictions = self.model.predict(X)
            probabilities = self.model.predict_proba(X)
        else:
            raise Exception("Model is not available for prediction")
        
        # Convert numeric predictions back to labels
        label_mapping = {0: 'healthy', 1: 'at_risk', 2: 'needs_maintenance'}
        predictions_labels = [label_mapping[pred] for pred in predictions]
        
        # Get confidence scores (max probability)
        confidence_scores = np.max(probabilities, axis=1)
        
        # Generate recommendations based on predictions
        recommendations = []
        for pred in predictions_labels:
            if pred == 'healthy':
                recommendations.append("Device is operating normally. No action required.")
            elif pred == 'at_risk':
                recommendations.append("Device showing signs of potential issues. Schedule inspection.")
            else:  # needs_maintenance
                recommendations.append("Device requires immediate maintenance. Schedule service.")
        
        return list(zip(predictions_labels, confidence_scores, recommendations))
    
    def save_model(self, filepath: str = "models/device_health_model.pkl"):
        """
        Save the trained model to disk
        """
        # Create models directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'is_trained': self.is_trained
        }
        joblib.dump(model_data, filepath)
    
    def load_model(self, filepath: str = "models/device_health_model.pkl") -> bool:
        """
        Load a trained model from disk
        """
        try:
            if os.path.exists(filepath):
                model_data = joblib.load(filepath)
                self.model = model_data['model']
                self.scaler = model_data['scaler']
                self.is_trained = model_data['is_trained']
                return True
            return False
        except Exception as e:
            print(f"Error loading model: {e}")
            return False

# Initialize global predictor instance
predictor = DeviceHealthPredictor()