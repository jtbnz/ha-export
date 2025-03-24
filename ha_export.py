#!/usr/bin/env python3
"""
Home Assistant Sensor Data Export

This script connects to a Home Assistant instance and exports historical
sensor data for a specified time range.

Usage:
    python ha_export.py [sensor_entity_id] [time_range_hours] [output_file]

Example:
    python ha_export.py sensor.fabic_care_025_energy_power 24 power_data.csv
"""

import argparse
import datetime
import json
import os
import sys
import time
import csv
from pathlib import Path
from typing import Dict, List, Optional, Union

import requests

# Try to import pandas, but provide fallback if not available
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("Warning: pandas not available, using fallback CSV implementation.")

# Import configuration from secrets.py
try:
    from secrets import HA_URL, HA_TOKEN
except ImportError:
    print("Error: secrets.py file not found or incomplete.")
    print("Please copy secrets_template.py to secrets.py and fill in your Home Assistant details.")
    sys.exit(1)


class HomeAssistantAPI:
    """Class to interact with the Home Assistant REST API."""

    def __init__(self, base_url: str, token: str):
        """
        Initialize the Home Assistant API client.

        Args:
            base_url: The base URL of the Home Assistant instance
            token: The long-lived access token for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def get_sensor_history(
        self, entity_id: str, hours: int
    ) -> List[Dict[str, Union[str, float]]]:
        """
        Retrieve historical data for a specific sensor.

        Args:
            entity_id: The entity ID of the sensor
            hours: Number of hours of history to retrieve

        Returns:
            List of sensor readings with timestamp and state
        """
        # Calculate start time (now - hours)
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(hours=hours)

        # Format timestamps for the API
        start_time_str = start_time.isoformat()
        end_time_str = end_time.isoformat()

        # Build the API URL
        url = f"{self.base_url}/api/history/period/{start_time_str}"
        params = {
            "filter_entity_id": entity_id,
            "end_time": end_time_str,
            "minimal_response": "true",
        }

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            # The API returns a list of lists, where each inner list contains
            # the history for one entity. Since we're filtering for a specific
            # entity, we can take the first list.
            data = response.json()
            
            if not data or not data[0]:
                print(f"No data found for entity {entity_id} in the specified time range.")
                return []
                
            # Print the first entry for debugging
            if data and data[0]:
                print(f"Sample data entry: {json.dumps(data[0][0], indent=2, default=str)}")
            
            # Extract the relevant data
            history_data = []
            for entry in data[0]:
                try:
                    # Check if 'last_updated' exists in the entry
                    if 'last_updated' not in entry:
                        print(f"Warning: 'last_updated' field missing in entry: {json.dumps(entry, indent=2, default=str)}")
                        # Try to use 'last_changed' as fallback if available
                        if 'last_changed' in entry:
                            print(f"Using 'last_changed' as fallback for timestamp")
                            timestamp_str = entry['last_changed']
                        else:
                            print(f"No timestamp field found, skipping entry")
                            continue
                    else:
                        timestamp_str = entry['last_updated']
                    
                    # Convert the timestamp to a datetime object
                    # Handle different timestamp formats
                    if 'Z' in timestamp_str:
                        # ISO format with Z (UTC)
                        timestamp = datetime.datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    elif '+' in timestamp_str or '-' in timestamp_str and 'T' in timestamp_str:
                        # ISO format with timezone offset
                        timestamp = datetime.datetime.fromisoformat(timestamp_str)
                    else:
                        # ISO format without timezone (assume local)
                        timestamp = datetime.datetime.fromisoformat(timestamp_str)
                    
                    # Try to convert state to float if it's numeric
                    try:
                        state = float(entry['state'])
                    except (ValueError, TypeError):
                        state = entry['state']
                        
                    history_data.append({
                        'timestamp': timestamp,
                        'state': state,
                        'attributes': entry.get('attributes', {})
                    })
                except Exception as e:
                    print(f"Error processing entry: {e}")
                    print(f"Problematic entry: {json.dumps(entry, indent=2, default=str)}")
                
            return history_data
            
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Home Assistant: {e}")
            sys.exit(1)
        except (ValueError, KeyError) as e:
            print(f"Error processing response from Home Assistant: {e}")
            print(f"Response data: {json.dumps(data, indent=2, default=str) if 'data' in locals() else 'No data received'}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            print(f"Response data: {json.dumps(data, indent=2, default=str) if 'data' in locals() else 'No data received'}")
            sys.exit(1)

    def check_connection(self) -> bool:
        """
        Check if the connection to Home Assistant is working.

        Returns:
            True if connection is successful, False otherwise
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/", headers=self.headers, timeout=10
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False


def save_data(
    data: List[Dict[str, Union[str, float]]], output_file: str
) -> None:
    """
    Save sensor data to the specified output file.

    Args:
        data: List of sensor readings
        output_file: Path to the output file
    """
    if not data:
        print("No data to save.")
        return

    # Determine the output format based on the file extension
    file_ext = os.path.splitext(output_file)[1].lower()
    
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
    """Main function to parse arguments and execute the data export."""
    parser = argparse.ArgumentParser(
        description="Export sensor data from Home Assistant."
    )
    parser.add_argument(
        "entity_id", help="Entity ID of the sensor (e.g., sensor.fabic_care_025_energy_power)"
    )
    parser.add_argument(
        "hours", type=int, help="Number of hours of history to retrieve"
    )
    parser.add_argument(
        "output_file", help="Path to save the exported data"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.hours <= 0:
        print("Error: Hours must be a positive number.")
        sys.exit(1)
        
    # Create output directory if it doesn't exist
    output_path = Path(args.output_file)
    output_dir = output_path.parent
    if output_dir and not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize the Home Assistant API client
    ha_api = HomeAssistantAPI(HA_URL, HA_TOKEN)
    
    # Check connection to Home Assistant
    print("Checking connection to Home Assistant...")
    if not ha_api.check_connection():
        print("Error: Could not connect to Home Assistant.")
        print("Please check your URL and token in secrets.py.")
        sys.exit(1)
    
    print(f"Connected to Home Assistant at {HA_URL}")
    
    # Retrieve sensor history
    print(f"Retrieving {args.hours} hours of history for {args.entity_id}...")
    start_time = time.time()
    history_data = ha_api.get_sensor_history(args.entity_id, args.hours)
    elapsed_time = time.time() - start_time
    
    # Print summary
    if history_data:
        print(f"Retrieved {len(history_data)} data points in {elapsed_time:.2f} seconds.")
        
        # Save the data
        save_data(history_data, args.output_file)
    else:
        print("No data retrieved. Please check if the sensor exists and has historical data.")


if __name__ == "__main__":
    main()
