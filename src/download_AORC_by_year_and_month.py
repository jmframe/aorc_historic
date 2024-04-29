#!/home/jmframe/aorc_historic/environment/.conda/envs/aorc_env/bin/python3
import argparse
import yaml
import os
import requests
from os.path import join, exists
from os import makedirs

def download_file(url, directory):
    if not exists(directory):
        makedirs(directory)

    local_filename = join(directory, url.split('/')[-1])
    # Check if file exists
    head_response = requests.head(url, verify=False)  # Still using verify=False for the example
    if head_response.status_code == 200:
        response = requests.get(url, stream=True, verify=False)
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {local_filename}")
    else:
        print(f"Failed to download {local_filename}. Status code: {head_response.status_code}. File URL: {url}")

def download_region_data(base_url, region_code, year, month, base_directory):
    formatted_month = f"{year}{month:02d}"
    region_directory = join(base_directory, f"AORC_{region_code.upper()}_4km")

    # Temperature data
    temp_url = join(base_url, f"AORC_{region_code.upper()}_4km/AORC_TMPR_4KM_{region_code.upper()}_{formatted_month}.zip")
    download_file(temp_url, region_directory)

    # Precipitation data
    precip_directory = join(region_directory, f"{region_code.upper()}_precip_partition")
    precip_url = join(base_url, f"AORC_{region_code.upper()}_4km/{region_code.upper()}_precip_partition/AORC_APCP_4KM_{region_code.upper()}_{formatted_month}.zip")
    download_file(precip_url, precip_directory)

def main():
    parser = argparse.ArgumentParser(description="Download AORC data based on configurations from a YAML file.")
    parser.add_argument('-c', '--config', type=str, required=True, help='Path to the configuration file.')
    args = parser.parse_args()

    with open(args.config, 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    base_url = cfg['base_url']
    base_directory = cfg['base_directory']
    year = cfg['year']
    month = cfg['month']
    
    regions = ['AORC_ABRFC_4km', 'AORC_CBRFC_4km', 'AORC_CNRFC_4km', 'AORC_LMRFC_4km',
               'AORC_MARFC_4km', 'AORC_MBRFC_4km', 'AORC_NCRFC_4km', 'AORC_NERFC_4km',
               'AORC_NWRFC_4km', 'AORC_OHRFC_4km', 'AORC_SERFC_4km', 'AORC_WGRFC_4km']

    for region in regions:
        region_code = region.split('_')[1]
        download_region_data(base_url, region_code, year, month, base_directory)

if __name__ == "__main__":
    main()
