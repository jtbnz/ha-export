# Home Assistant Sensor Data Export

A Python utility to export sensor data from Home Assistant for analysis and visualization.

## Features

- Connect to Home Assistant via the REST API
- Extract historical sensor data for a specified time range
- Save data to various file formats (CSV, JSON)
- Configurable time range in hours
- Secure storage of API credentials
- Fallback implementation for environments without pandas
- Debug mode for detailed logging during troubleshooting

## Prerequisites

- Python 3.9+
- Home Assistant instance with API access
- Long-Lived Access Token (see [API Key Setup](docs/api_key_setup.md))

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/jtbnz/ha-export.git
   cd ha-export
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your credentials:
   ```
   cp secrets_template.py secrets.py
   ```
   Edit `secrets.py` with your Home Assistant URL and API token.

## Configuration

The `secrets.py` file contains the following configuration options:

- `HA_URL`: The URL of your Home Assistant instance
- `HA_TOKEN`: Your Home Assistant Long-Lived Access Token
- `DEBUG`: Set to `True` to enable detailed logging for troubleshooting, or `False` for minimal output during normal operation

## Usage

```
python ha_export.py [sensor_entity_id] [time_range_hours] [output_file]
```

### Arguments

- `sensor_entity_id`: The entity ID of the sensor to export (e.g., `sensor.fabic_care_025_energy_power`)
- `time_range_hours`: Number of hours of historical data to retrieve (e.g., `24`)
- `output_file`: Path to save the exported data (e.g., `power_data.csv`)

### Examples

Export 24 hours of power consumption data to CSV:
```
python ha_export.py sensor.fabic_care_025_energy_power 24 power_data.csv
```

Export 48 hours of temperature data to JSON:
```
python ha_export.py sensor.living_room_temperature 48 temperature_data.json
```

## Output Formats

The script automatically determines the output format based on the file extension:

- `.csv`: Comma-separated values
- `.json`: JSON format
- Other extensions default to CSV format

## Documentation

- [API Key Setup](docs/api_key_setup.md): Instructions for creating a Home Assistant API token

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
