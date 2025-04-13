# MCP Radiation

A Python package for retrieving solar radiation data using NASA's POWER API.

## Features

- Retrieve hourly solar radiation data for any location
- Support for total, direct, and diffuse irradiance
- Temperature and wind speed data included
- Automatic date validation and adjustment
- Retry mechanism for API requests
- Export data to CSV format

## Installation

```bash
pip install -e .
```

## Usage

```python
from mcp_radiation import RadiationMCP

# Initialize with location coordinates
mcp = RadiationMCP(latitude=39.9042, longitude=116.4074)

# Get data for a specific date range
data = mcp.fetch_data('2023-01-01', '2023-12-31')

# Get five years of hourly data
df, stats = mcp.get_five_years_hourly_data('data')
```

## Data Format

The package retrieves the following parameters:
- Total irradiance (W/m²)
- Direct irradiance (W/m²)
- Diffuse irradiance (W/m²)
- Temperature (°C)
- Wind speed (m/s)

## License

MIT License

## Author

俞海 (yuhai_8203@126.com) 