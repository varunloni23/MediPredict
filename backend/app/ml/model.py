import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
from datetime import datetime
from typing import List, Tuple, Optional, Any, Dict

class DeviceHealthPredictor:
    def __init__(self):
        self.model: Optional[RandomForestClassifier] = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_names = ['usage_hours', 'temperature', 'pressure', 'vibration', 'error_count']
        
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
    
    def predict_with_explanation(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Predict device health status with detailed explanations
        Returns: list of predictions with explanations including feature importance
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
            
            # Get feature importance from the model
            feature_importance = self.model.feature_importances_
            
            # Get the actual classes the model was trained on
            model_classes = self.model.classes_
        else:
            raise Exception("Model is not available for prediction")
        
        # Convert numeric predictions back to labels
        label_mapping = {0: 'healthy', 1: 'at_risk', 2: 'needs_maintenance'}
        
        results = []
        for idx, pred in enumerate(predictions):
            prediction_label = label_mapping.get(pred, 'unknown')
            confidence_score = float(np.max(probabilities[idx]))
            
            # Get probability distribution across all classes (only those in the model)
            class_probabilities = {}
            for class_idx, class_label in enumerate(model_classes):
                class_name = label_mapping.get(class_label, f'class_{class_label}')
                if class_idx < len(probabilities[idx]):
                    class_probabilities[class_name] = float(probabilities[idx][class_idx])
                else:
                    class_probabilities[class_name] = 0.0
            
            # Ensure all three classes are in the output (even if model wasn't trained on them)
            for class_name in ['healthy', 'at_risk', 'needs_maintenance']:
                if class_name not in class_probabilities:
                    class_probabilities[class_name] = 0.0
            
            # Calculate feature contributions for this prediction
            feature_values = df.iloc[idx][self.feature_names].to_dict()
            
            # Create feature importance dictionary
            feature_contributions = {}
            for feature_name, importance in zip(self.feature_names, feature_importance):
                feature_contributions[feature_name] = {
                    'importance': float(importance),
                    'value': float(feature_values[feature_name])
                }
            
            # Sort features by importance
            sorted_features = sorted(
                feature_contributions.items(),
                key=lambda x: x[1]['importance'],
                reverse=True
            )
            
            # Generate detailed recommendation
            recommendation = self._generate_detailed_recommendation(
                prediction_label,
                sorted_features,
                confidence_score
            )
            
            # Create explanation text
            explanation = self._create_explanation(
                prediction_label,
                sorted_features,
                confidence_score
            )
            
            result = {
                'prediction': prediction_label,
                'confidence': confidence_score,
                'class_probabilities': class_probabilities,
                'feature_contributions': dict(sorted_features),
                'recommendation': recommendation,
                'explanation': explanation,
                'top_factors': [f[0] for f in sorted_features[:3]]  # Top 3 most important features
            }
            
            results.append(result)
        
        return results
    
    def _generate_detailed_recommendation(self, prediction: str, sorted_features: List, confidence: float) -> str:
        """Generate a detailed recommendation based on prediction and feature analysis"""
        recommendations = []
        
        if prediction == 'healthy':
            recommendations.append("✓ Device is operating within normal parameters.")
            if confidence < 0.7:
                recommendations.append("⚠ However, confidence is moderate. Monitor closely.")
        elif prediction == 'at_risk':
            recommendations.append("⚠ Device showing early warning signs.")
            recommendations.append("→ Schedule preventive inspection within 2-4 weeks.")
        else:  # needs_maintenance
            recommendations.append("🔴 Critical: Device requires immediate attention.")
            recommendations.append("→ Schedule maintenance within 24-48 hours.")
        
        # Add specific feature-based recommendations
        for feature_name, data in sorted_features[:2]:  # Top 2 features
            importance = data['importance']
            value = data['value']
            
            if importance > 0.15:  # Significant contributor
                if feature_name == 'error_count' and value > 5:
                    recommendations.append(f"→ High error count ({int(value)}) detected - investigate error logs.")
                elif feature_name == 'temperature' and value > 40:
                    recommendations.append(f"→ Elevated temperature ({value:.1f}°C) - check cooling system.")
                elif feature_name == 'vibration' and value > 1.0:
                    recommendations.append(f"→ Abnormal vibration ({value:.2f} Hz) - check mechanical components.")
                elif feature_name == 'pressure' and (value < 80 or value > 140):
                    recommendations.append(f"→ Pressure outside normal range ({value:.1f} PSI) - inspect pressure system.")
                elif feature_name == 'usage_hours' and value > 5000:
                    recommendations.append(f"→ High usage hours ({int(value)}) - consider scheduled maintenance.")
        
        return "\n".join(recommendations)
    
    def _create_explanation(self, prediction: str, sorted_features: List, confidence: float) -> str:
        """Create a human-readable explanation of the prediction"""
        explanation_parts = []
        
        explanation_parts.append(
            f"The model predicts this device is '{prediction}' with {confidence*100:.1f}% confidence."
        )
        
        # Explain top contributing factors
        top_features = sorted_features[:3]
        if top_features:
            explanation_parts.append("\nKey factors influencing this prediction:")
            for idx, (feature_name, data) in enumerate(top_features, 1):
                importance_pct = data['importance'] * 100
                value = data['value']
                
                feature_display = {
                    'usage_hours': f'Usage Hours ({int(value)} hrs)',
                    'temperature': f'Temperature ({value:.1f}°C)',
                    'pressure': f'Pressure ({value:.1f} PSI)',
                    'vibration': f'Vibration ({value:.2f} Hz)',
                    'error_count': f'Error Count ({int(value)})'
                }
                
                explanation_parts.append(
                    f"{idx}. {feature_display.get(feature_name, feature_name)} - "
                    f"{importance_pct:.1f}% contribution to prediction"
                )
        
        return "\n".join(explanation_parts)
    
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