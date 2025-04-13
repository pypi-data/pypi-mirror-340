# Solar Radiation Analysis

A Python package for analyzing solar radiation and wind speed data from NASA POWER API.

## Installation

```bash
pip install solar-radiation-analysis
```

## Usage

```python
from solar_radiation_analysis import SolarRadiationAnalysis

# Initialize the analysis with location coordinates
analysis = SolarRadiationAnalysis(latitude=39.9042, longitude=116.4074)

# Get analysis results
results = analysis.get_analysis()

# Print the results
print(results)
```

## Features

- Retrieves solar radiation and wind speed data from NASA POWER API
- Calculates five-year averages
- Analyzes yearly and monthly trends
- Identifies daily peaks and extreme values
- Provides comprehensive statistical analysis

## Dependencies

- requests
- pandas
- numpy

## License

MIT License

## Author

Yu Hai (yuhai_8203@126.com) 