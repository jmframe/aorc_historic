#!/home/jmframe/aorc_historic/environment/.conda/envs/aorc_env/bin/python3
import geopandas as gpd
import xarray as xr
import os
import pandas as pd
import yaml
import argparse
import logging
import multiprocessing

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(path):
    with open(path, 'r') as file:
        config = yaml.safe_load(file)
    logging.info(f"Configuration loaded from {path}")
    return config

def process_netcdf(file_path, var_name):
    logging.info(f"Opening NetCDF file: {file_path}")
    with xr.open_dataset(file_path) as ds:
        data_array = ds[var_name].squeeze()
        if isinstance(data_array, xr.DataArray):
            temp_df = data_array.to_dataframe(name=var_name).reset_index()
            temp_df['variable'] = var_name  # Add a 'variable' column
            return temp_df
        else:
            logging.error("Expected data_array to be an xarray DataArray.")
            return None

def process_file(file_info):
    file, config, gdf, regions, attempted_regions, intersecting_regions = file_info
    logging.info(f"Processing file: {file}")
    file_path = os.path.join(config['netcdf_directory'], file)
    file_region = next((r for r in regions if r in file), None)

    if file_region in attempted_regions and file_region not in intersecting_regions:
        logging.info(f"Skipping processing for {file} as its region {file_region} is known not to intersect.")
        return None, None

    logging.info(f"Processing file: {file_path}")

    var_name = file.split('_')[1]
    if var_name == "TMP":
        var_name = "TMP_2maboveground"
    elif var_name == "APCP":
        var_name = "APCP_surface"
    date_str = file.split('_')[-1].split('.')[0]
    date = pd.to_datetime(date_str, format='%Y%m%d%H')
    
    temp_df = process_netcdf(file_path, var_name)
    if temp_df is None:
        logging.error(f"Failed to process NetCDF data from {file_path}")
        return None, None

    temp_gdf = gpd.GeoDataFrame(temp_df, geometry=gpd.points_from_xy(temp_df.longitude, temp_df.latitude))
    temp_gdf.set_crs("EPSG:4326", inplace=True)
    temp_gdf.to_crs(gdf.crs, inplace=True)
    
    joined_gdf = gpd.sjoin(temp_gdf, gdf, how="inner", predicate='intersects')
    if not joined_gdf.empty:
        joined_gdf['time'] = date
        intersecting_regions.add(file_region)  # Mark this region as intersecting
        attempted_regions.add(file_region)     # Mark this region as attempted
        return joined_gdf, var_name
    else:
        logging.info(f"No intersecting data found for file: {file}")
        attempted_regions.add(file_region)     # Mark this region as attempted
        return None, None

def main(config_path):
    config = load_config(config_path)
    gdf = gpd.read_file(config['geopackage_path'])
    if gdf.crs is None:
        gdf.set_crs("EPSG:5070", inplace=True)

    regions = ['ABRFC', 'CBRFC', 'CNRFC', 'LMRFC', 
               'MARFC', 'MBRFC', 'NCRFC', 'NERFC', 
               'NWRFC', 'OHRFC', 'SERFC', 'WGRFC']
    nc_files = [f for f in os.listdir(config['netcdf_directory']) if f.endswith('.nc4')]

    # Initialize the sets and counters
    attempted_regions = set()
    intersecting_regions = set()

    # Initialize data_frames and var_names as empty lists and sets
    data_frames = []  # This will store the results from each file processed
    var_names = set()  # This will store the variable names extracted from the files
    success_count = 0  # This will count the number of successful processes
    debug_limit = config.get('debug_limit', None)  # Get debug_limit from config

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        for result in pool.imap(process_file, [(file, config, gdf, regions, attempted_regions, intersecting_regions) for file in nc_files]):
            if result[0] is not None:
                data_frames.append(result[0])
                var_names.add(result[1])
                success_count += 1
                if debug_limit and success_count >= debug_limit:
                    logging.info(f"Debug limit reached: {debug_limit} files processed successfully.")
                    break

    if data_frames:
        final_df = pd.concat(data_frames, ignore_index=True)
        if 'variable' in final_df.columns:
            for var_name in final_df['variable'].unique():
                filtered_df = final_df[final_df['variable'] == var_name]
                time_series_data = filtered_df.groupby(['id', 'time'])[var_name].mean().unstack(level=0)
                output_filename = f"{var_name}_{pd.Timestamp.now().strftime('%Y_%m')}.csv"
                time_series_data.to_csv(os.path.join(config['output_dir'], output_filename))
                logging.info(f"Output saved for {var_name} to {output_filename}")
        else:
            logging.error("No 'variable' column found in the DataFrame.")   
    else:
        logging.info("No valid data to process. No output file created.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process NetCDF files over GeoPackage data.")
    parser.add_argument('config_path', type=str, help='Path to the configuration YAML file')
    args = parser.parse_args()
    main(args.config_path)