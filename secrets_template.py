# Home Assistant API Configuration
# --------------------------------
# This file contains configuration for connecting to your Home Assistant instance.
# Copy this file to 'secrets.py' and fill in your specific details.
# Note: 'secrets.py' is included in .gitignore to prevent sensitive information from being committed.

# The URL of your Home Assistant instance
# Examples:
#   - Local instance: "http://homeassistant.local:8123"
#   - Local IP: "http://192.168.1.100:8123"
#   - Remote access: "https://your-instance.duckdns.org"
HA_URL = "http://your-home-assistant-url:8123"

# Your Home Assistant Long-Lived Access Token
# See the documentation for instructions on how to create this token
HA_TOKEN = "your_long_lived_access_token_here"

# Debug Mode
# Set to True to enable detailed logging for troubleshooting
# Set to False for minimal output during normal operation
DEBUG = False
