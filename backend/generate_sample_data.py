import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_sample_data(num_devices=5, records_per_device=100):
    """
    Generate sample device data for testing
    """
    data = []
    
    # Device types and manufacturers
    device_types = ['MRI Scanner', 'Ultrasound Machine', 'Infusion Pump', 'Ventilator', 'ECG Machine']
    manufacturers = ['MedTech Inc.', 'HealthCorp', 'CareSystems', 'LifeCare', 'BioMed']
    
    for device_id in range(1, num_devices + 1):
        # Device info
        device_type = random.choice(device_types)
        manufacturer = random.choice(manufacturers)
        
        # Generate records for this device
        for record_id in range(records_per_device):
            # Generate timestamp
            timestamp = datetime.now() - timedelta(days=random.randint(0, 365))
            
            # Generate realistic device data
            usage_hours = random.uniform(50, 500)
            temperature = random.uniform(20, 50)
            pressure = random.uniform(80, 160)
            vibration = random.uniform(0, 1)
            error_count = random.randint(0, 10)
            
            # Randomly generate error codes
            error_codes = None
            if error_count > 0 and random.random() > 0.7:
                error_codes = f"ERR{random.randint(100, 999)}"
            
            data.append({
                'device_id': f'DEV-{device_id:05d}',
                'timestamp': timestamp,
                'usage_hours': usage_hours,
                'temperature': temperature,
                'pressure': pressure,
                'vibration': vibration,
                'error_count': error_count,
                'error_codes': error_codes
            })
    
    return pd.DataFrame(data)

def save_sample_data_to_csv(filename='sample_device_data.csv'):
    """
    Generate and save sample data to CSV
    """
    df = generate_sample_data()
    df.to_csv(filename, index=False)
    print(f"Sample data saved to {filename}")
    print(f"Generated {len(df)} records for {df['device_id'].nunique()} devices")
    return df

if __name__ == "__main__":
    df = save_sample_data_to_csv()
    print("\nFirst few rows of generated data:")
    print(df.head())