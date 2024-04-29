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

# Setup argument parser
parser = argparse.ArgumentParser(description="Process NetCDF files over GeoPackage data.")
parser.add_argument('config_path', type=str, help='Path to the configuration YAML file')
args = parser.parse_args()

# Load configuration
config = load_config(args.config_path)

def process_netcdf(file_path, var_name):
    with xr.open_dataset(file_path) as ds:
        return ds[var_name].squeeze()

# Load GeoPackage containing sub-catchment geometries
gdf = gpd.read_file(config['geopackage_path'])

# Directory containing the NetCDF files
nc_dir = config['netcdf_directory']

# List all NetCDF files
nc_files = [f for f in os.listdir(nc_dir) if f.endswith('.nc4')]

data_frames = []
for file in nc_files:
    file_path = os.path.join(nc_dir, file)
    var_name = file.split('_')[1]
    if var_name == "TMP":
        var_name = "TMP_2maboveground"
    elif var_name == "APCP":
        var_name = "APCP_surface"
    date_str = file.split('_')[-1].split('.')[0]
    date = pd.to_datetime(date_str, format='%Y%m%d%H')
    print(file_path)
    data_array = process_netcdf(file_path, var_name)
    temp_df = data_array.to_dataframe(name=var_name).reset_index()
    temp_gdf = gpd.GeoDataFrame(temp_df, geometry=gpd.points_from_xy(temp_df.longitude, temp_df.latitude))

    joined_gdf = gpd.sjoin(temp_gdf, gdf, how="inner", op='intersects')
    joined_gdf['time'] = date
    
    data_frames.append(joined_gdf)

final_df = pd.concat(data_frames)
time_series_data = final_df.groupby(['id', 'time'])[var_name].mean().unstack(level=0)

# Save the time series data
time_series_data.to_csv(config['output_csv'])