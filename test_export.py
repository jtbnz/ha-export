#!/usr/bin/env python3
"""
Test script for Home Assistant Sensor Data Export

This script tests the basic functionality of the ha_export.py script
without actually connecting to a Home Assistant instance.
"""

import datetime
import json
import os
import sys
import csv
from pathlib import Path

# Try to import pandas, but provide fallback if not available
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("Warning: pandas not available, using fallback CSV implementation.")

# Try to import DEBUG from secrets.py, default to False if not available
try:
    from secrets import DEBUG
except ImportError:
    DEBUG = False

def debug_log(message):
    """Print debug messages only when DEBUG is enabled."""
    if DEBUG:
        print(f"[DEBUG] {message}")

def generate_test_data(hours=24, interval_minutes=5):
    """
    Generate test sensor data for a specified time range.
    
    Args:
        hours: Number of hours of data to generate
        interval_minutes: Interval between data points in minutes
        
    Returns:
        List of sensor readings with timestamp and state
    """
    debug_log(f"Generating test data for {hours} hours with {interval_minutes} minute intervals")
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(hours=hours)
    debug_log(f"Time range: {start_time} to {end_time}")
    
    # Generate data points at regular intervals
    data = []
    current_time = start_time
    while current_time <= end_time:
        # Simulate a power sensor with some random-like values
        # In a real scenario, this would come from Home Assistant
        power_value = 100 + (current_time.hour * 10) + (current_time.minute / 6)
        
        data.append({
            'timestamp': current_time,
            'state': power_value,
            'attributes': {
                'unit_of_measurement': 'W',
                'friendly_name': 'Test Power Sensor'
            }
        })
        
        current_time += datetime.timedelta(minutes=interval_minutes)
    
    return data

def save_data(data, output_file):
    """
    Save sensor data to the specified output file.
    
    Args:
        data: List of sensor readings
        output_file: Path to the output file
    """
    debug_log(f"Saving {len(data)} data points to {output_file}")
    
    if not data:
        print("No data to save.")
        return

    # Determine the output format based on the file extension
    file_ext = os.path.splitext(output_file)[1].lower()
    debug_log(f"Detected file extension: {file_ext}")
    
    try:
        if PANDAS_AVAILABLE:
            # Use pandas if available
            df = pd.DataFrame([
                {'timestamp': entry['timestamp'], 'value': entry['state']}
                for entry in data
            ])
            
            if file_ext == '.csv':
                df.to_csv(output_file, index=False)
            elif file_ext == '.json':
                # For JSON, we'll include more details including attributes
                full_data = [
                    {
                        'timestamp': entry['timestamp'].isoformat(),
                        'value': entry['state'],
                        'attributes': entry['attributes']
                    }
                    for entry in data
                ]
                with open(output_file, 'w') as f:
                    json.dump(full_data, f, indent=2)
            elif file_ext == '.xlsx':
                df.to_excel(output_file, index=False)
            else:
                # Default to CSV for unknown extensions
                print(f"Unknown file extension '{file_ext}', defaulting to CSV format.")
                df.to_csv(output_file, index=False)
        else:
            # Fallback implementation without pandas
            if file_ext == '.json':
                # For JSON, we'll include more details including attributes
                full_data = [
                    {
                        'timestamp': entry['timestamp'].isoformat(),
                        'value': entry['state'],
                        'attributes': entry['attributes']
                    }
                    for entry in data
                ]
                with open(output_file, 'w') as f:
                    json.dump(full_data, f, indent=2)
            else:
                # Default to CSV for all other formats when pandas is not available
                if file_ext != '.csv':
                    print(f"Extension '{file_ext}' requires pandas. Using CSV format instead.")
                
                with open(output_file, 'w', newline='') as csvfile:
                    fieldnames = ['timestamp', 'value']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for entry in data:
                        writer.writerow({
                            'timestamp': entry['timestamp'].isoformat(),
                            'value': entry['state']
                        })
            
        print(f"Data successfully saved to {output_file}")
        
    except Exception as e:
        print(f"Error saving data to {output_file}: {e}")
        sys.exit(1)

def main():
    """Main function to execute the test."""
    # Parse command line arguments
    if len(sys.argv) != 3:
        print("Usage: python test_export.py [hours] [output_file]")
        sys.exit(1)
        
    try:
        hours = int(sys.argv[1])
    except ValueError:
        print("Error: Hours must be a number.")
        sys.exit(1)
        
    if hours <= 0:
        print("Error: Hours must be a positive number.")
        sys.exit(1)
        
    output_file = sys.argv[2]
    
    # Create output directory if it doesn't exist
    output_path = Path(output_file)
    output_dir = output_path.parent
    if output_dir and not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate test data
    print(f"Generating {hours} hours of test data...")
    data = generate_test_data(hours=hours)
    
    # Print summary
    print(f"Generated {len(data)} data points.")
    
    # Save the data
    save_data(data, output_file)

if __name__ == "__main__":
    main()
