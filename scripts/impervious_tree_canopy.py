from pathlib import Path
import rasterio
import pandas as pd
import numpy as np
from rasterio.warp import transform
from rasterio.mask import mask
from shapely.geometry import Point, mapping

df = pd.read_csv("coordinates.csv")

folder = Path(__file__).resolve().parent / "data_sources"

lake_placid_f = folder / "lake_placid_nlcd_tcc_conus_wgs84_v2025-6_20250101_20251231_5bf23954-a327-45a0-8b94-34e1277c6240.tiff"
nyc_f = folder / "nyc_nlcd_tcc_conus_wgs84_v2025-6_20250101_20251231_49bca7e9-5509-422b-a5b7-b80ddb84c406.tiff"
syracuse_f = folder / "syracuse_nlcd_tcc_conus_wgs84_v2025-6_20250101_20251231_66113322-a82a-455f-914c-6f60801f837a.tiff"
troy_f = folder / "troy_nlcd_tcc_conus_wgs84_v2025-6_20250101_20251231_11f06316-9e48-49cc-b572-42b623d08664.tiff"

lake_placid_impervious_f = folder / "lake_placid_Annual_NLCD_FctImp_2025_CU_C1V2_c233c6ac-15fa-4382-9a02-9b1fa7a912c9.tiff"
nyc_impervious_f = folder / "nyc_Annual_NLCD_FctImp_2025_CU_C1V2_f5aab22f-552b-4d07-84a0-54b112ffd60d.tiff"
syracuse_impervious_f = folder / "syracuse_Annual_NLCD_FctImp_2025_CU_C1V2_8e4afcc9-ceb7-44bd-8b41-90d8c9233e25.tiff"
troy_impervious_f = folder / "troy_Annual_NLCD_FctImp_2025_CU_C1V2_4bd7d48b-de16-4123-bf01-b21e9c12db5b.tiff"


tree_files = {
    "Troy": troy_f,
    "NYC": nyc_f,
    "Syracuse": syracuse_f,
    "Lake Placid": lake_placid_f
}

impervious_files = {
    "Troy": troy_impervious_f,
    "NYC": nyc_impervious_f,
    "Syracuse": syracuse_impervious_f,
    "Lake Placid": lake_placid_impervious_f
}

# calculate average percentage within a 500-meter radius of coordinate
def calculate_average(src, lat, lon):
    # convert lat/lon to Alber coordinates (meters), since the tiff files are not in degrees
    xs, ys = transform("EPSG:4326", src.crs, [lon], [lat])

    # create 500-meter radius
    buffer = Point(xs[0], ys[0]).buffer(500)

    # extract raster pixels and remove NoData pixels
    data, _ = mask(src, [mapping(buffer)], crop=True, filled=False)
    valid = data[0].compressed()
    valid = valid[(valid >= 0) & (valid <= 100)]

    avg = float(np.mean(valid)) if len(valid) > 0 else None

    return avg


results = []


for _, row in df.iterrows():
    lat = row["Lat"]
    lon = row["Long"]
    area = row["Area"]

    # calculate impervious percentage
    with rasterio.open(impervious_files[area]) as src:
        avg_impervious = calculate_average(src, lat, lon)

        # get Albers coordinates
        xs, ys = transform("EPSG:4326", src.crs, [lon], [lat])

    # calculate tree canopy percentage from each tree canopy file
    with rasterio.open(tree_files[area]) as tree_src:
        avg_tree = calculate_average(tree_src, lat, lon)

    results.append({
        "Area": area,
        "Sample": row["Sample"],
        "Lat": lat,
        "Long": lon,
        "Albers_x": xs[0],
        "Albers_y": ys[0],
        "Impervious_Percent": avg_impervious,
        "Tree_Canopy_Percent": avg_tree
    })

result_df = pd.DataFrame(results)
result_df.to_csv("impervious_and_tree_canopy.csv", index=False)