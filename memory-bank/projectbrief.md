# Project Brief: Home Assistant Sensor Data Export

## Overview
A Python utility that connects to a Home Assistant instance via its REST API to extract historical sensor data. The tool allows users to specify a sensor entity, time range, and output file format.

## Core Requirements

1. **Authentication**
   - Connect to Home Assistant using a Long-Lived Access Token
   - Store credentials securely in a separate secrets file
   - Provide documentation on generating API tokens

2. **Data Extraction**
   - Extract historical data for a specified sensor
   - Allow configurable time range in hours
   - Support various sensor types (power, temperature, etc.)

3. **Output Options**
   - Save data to various file formats (CSV, JSON)
   - Automatically determine format based on file extension
   - Create output directories if they don't exist

4. **Command Line Interface**
   - Accept three parameters: sensor entity ID, time range in hours, output file
   - Provide clear error messages and usage instructions
   - Display progress information during execution

5. **Project Structure**
   - Use Python virtual environment for dependency management
   - Include proper .gitignore to exclude sensitive information
   - Provide comprehensive documentation

## Success Criteria

- Successfully connect to Home Assistant and authenticate
- Correctly retrieve historical data for the specified sensor and time range
- Properly format and save data to the specified output file
- Handle errors gracefully with informative messages
- Provide clear documentation for setup and usage

## Test Case

- Sensor: `sensor.fabic_care_025_energy_power`
- Time Range: 24 hours
- Output File: CSV format
