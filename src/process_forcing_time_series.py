#!/home/jmframe/aorc_historic/environment/.conda/envs/aorc_env/bin/python3
import geopandas as gpd
import xarray as xr
import os
import pandas as pd
import yaml
import argparse

def load_config(path):
    with open(path, 'r') as file:
        return yaml.safe_load(file)

def process_netcdf(file_path, var_name):
    with xr.open_dataset(file_path) as ds:
        return ds[var_name].squeeze()

def main(config_path):
    config = load_config(config_path)

    # Load GeoPackage
    gdf = gpd.read_file(config['geopackage_path'])
    if gdf.crs is None:
        gdf.set_crs("EPSG:5070", inplace=True)

    nc_dir = config['netcdf_directory']
    nc_files = [f for f in os.listdir(nc_dir) if f.endswith('.nc4')]

    # Regions known to intersect
    intersecting_regions = set()

    # Attempted regions to avoid re-checking non-intersecting
    attempted_regions = set()

    # All possible regions
    regions = ['ABRFC', 'CBRFC', 'CNRFC', 'LMRFC', 
               'MARFC', 'MBRFC', 'NCRFC', 'NERFC', 
               'NWRFC', 'OHRFC', 'SERFC', 'WGRFC']

    data_frames = []
    for file in nc_files:
        file_path = os.path.join(nc_dir, file)
        file_region = next((r for r in regions if r in file), None)

        if file_region in attempted_regions and file_region not in intersecting_regions:
            print(f"Skipping processing for {file} as its region {file_region} is known not to intersect.")
            continue

        print(f"Processing file: {file_path}")
        var_name = file.split('_')[1]
        if var_name == "TMP":
            var_name = "TMP_2maboveground"
        elif var_name == "APCP":
            var_name = "APCP_surface"
        date_str = file.split('_')[-1].split('.')[0]
        date = pd.to_datetime(date_str, format='%Y%m%d%H')
        
        data_array = process_netcdf(file_path, var_name)
        temp_df = data_array.to_dataframe(name=var_name).reset_index()
        temp_gdf = gpd.GeoDataFrame(temp_df, geometry=gpd.points_from_xy(temp_df.longitude, temp_df.latitude))
        temp_gdf.set_crs("EPSG:4326", inplace=True)  # Assuming NetCDF data in WGS84
        temp_gdf.to_crs(gdf.crs, inplace=True)  # Reproject to match GeoPackage CRS
        
        joined_gdf = gpd.sjoin(temp_gdf, gdf, how="inner", predicate='intersects')
        if not joined_gdf.empty:
            joined_gdf['time'] = date
            data_frames.append(joined_gdf)
            intersecting_regions.add(file_region)
        else:
            print(f"No intersecting data found for region {file_region}.")
        
        attempted_regions.add(file_region)

    if data_frames:
        final_df = pd.concat(data_frames, ignore_index=True)
        time_series_data = final_df.groupby(['id', 'time'])[var_name].mean().unstack(level=0)
        time_series_data.to_csv(config['output_csv'])
    else:
        print("No valid data to process.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process NetCDF files over GeoPackage data.")
    parser.add_argument('config_path', type=str, help='Path to the configuration YAML file')
    args = parser.parse_args()
    main(args.config_path)