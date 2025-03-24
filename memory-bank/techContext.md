# Technical Context: Home Assistant Sensor Data Export

## Technologies Used

### Core Technologies

1. **Python 3.9+**
   - Primary programming language
   - Chosen for its simplicity, readability, and extensive library ecosystem
   - Type hints used throughout for better code quality

2. **Home Assistant REST API**
   - Used to retrieve historical sensor data
   - Authenticated using Long-Lived Access Tokens
   - Documentation: https://developers.home-assistant.io/docs/api/rest/

3. **Virtual Environment (venv)**
   - Isolates project dependencies
   - Ensures consistent execution environment
   - Simplifies dependency management

### Key Libraries

1. **requests (>= 2.28.0)**
   - Handles HTTP communication with the Home Assistant API
   - Provides robust error handling and timeout management
   - Simplifies authentication header management

2. **pandas (>= 1.5.0)**
   - Used for data manipulation and export
   - Provides built-in support for CSV, JSON, and Excel formats
   - Simplifies timestamp handling and data transformation

3. **openpyxl (>= 3.0.10)**
   - Optional dependency for Excel file support
   - Used by pandas for Excel file export

4. **argparse (standard library)**
   - Handles command-line argument parsing
   - Provides automatic help generation
   - Simplifies input validation

5. **pathlib (standard library)**
   - Modern path manipulation
   - Cross-platform compatibility
   - Directory creation and validation

## Development Setup

### Environment Setup

1. **Python Installation**
   - Python 3.9 or higher required
   - Virtual environment recommended

2. **Virtual Environment**
   - Created using `python -m venv venv`
   - Activated with `source venv/bin/activate` (Unix) or `venv\Scripts\activate` (Windows)

3. **Dependencies**
   - Installed via `pip install -r requirements.txt`
   - Pinned versions for stability

### Project Structure

```
ha-export/
├── docs/
│   └── api_key_setup.md       # Documentation for API key generation
├── memory-bank/               # Project documentation and context
├── venv/                      # Virtual environment (not in version control)
├── .gitignore                 # Git ignore configuration
├── ha_export.py               # Main script
├── README.md                  # Project overview and usage instructions
├── requirements.txt           # Python dependencies
├── secrets.py                 # User-specific configuration (not in version control)
└── secrets_template.py        # Template for secrets.py
```

## Technical Constraints

1. **Home Assistant API Limitations**
   - Rate limiting may apply depending on Home Assistant instance
   - Historical data availability depends on Home Assistant configuration
   - Some sensors may not store historical data

2. **Authentication Requirements**
   - Requires a Long-Lived Access Token from Home Assistant
   - Token must have appropriate permissions to access sensor data

3. **Network Connectivity**
   - Requires network access to the Home Assistant instance
   - May need special configuration for remote access

4. **Data Volume Considerations**
   - Large time ranges may result in significant data volume
   - Memory usage increases with data size
   - Processing time scales with data volume

## Dependencies

### Direct Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| requests   | >=2.28.0 | HTTP communication with Home Assistant API |
| pandas     | >=1.5.0  | Data manipulation and export |
| openpyxl   | >=3.0.10 | Excel file support (optional) |

### Indirect Dependencies

| Dependency | Purpose |
|------------|---------|
| numpy      | Required by pandas for numerical operations |
| python-dateutil | Date parsing and manipulation |
| pytz       | Timezone support |
| six        | Python 2/3 compatibility utilities |
| charset-normalizer | Character encoding detection |
| idna       | Internationalized domain name support |
| urllib3    | HTTP client for requests |
| certifi    | SSL certificate verification |
| et-xmlfile | Excel XML file parsing |

## Compatibility

- **Operating Systems**: Cross-platform (Windows, macOS, Linux)
- **Python Versions**: 3.9 or higher recommended
- **Home Assistant Versions**: Compatible with recent Home Assistant releases (2022.x and newer)
