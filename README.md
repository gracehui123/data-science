# Environmental Data Analysis

Python scripts and datasets for exploring tree canopy, impervious surfaces, and weather at sample locations in NYC, Troy, Syracuse, and Lake Placid, New York.

- `original_data/`: source NLCD raster files and weather data.
- `modified_data/`: sample coordinates, calculated land-cover percentages, and a merged dataset.
- `scripts/impervious_tree_canopy.py`: calculates average canopy and impervious cover within 500 meters of each location.
- `scripts/weather.py`: retrieves daily weather from Open-Meteo for September 24–October 11, 2025, and calculates heating and cooling degree days.

## Running the scripts

Install the Python dependencies:

```sh
pip install pandas numpy rasterio shapely requests geopandas
```
