#!/home/jmframe/aorc_historic/environment/.conda/envs/aorc_env/bin/python3
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
    precip_directory = join(region_directory, "ABRFC_precip_partition")
    precip_url = join(base_url, f"AORC_{region_code.upper()}_4km/ABRFC_precip_partition/AORC_APCP_4KM_{region_code.upper()}_{formatted_month}.zip")
    download_file(precip_url, precip_directory)

base_url = 'https://hydrology.nws.noaa.gov/aorc-historic/'
regions = ['AORC_ABRFC_4km', 'AORC_CBRFC_4km', 'AORC_CNRFC_4km', 'AORC_LMRFC_4km',
           'AORC_MARFC_4km', 'AORC_MBRFC_4km', 'AORC_NCRFC_4km', 'AORC_NERFC_4km',
           'AORC_NWRFC_4km', 'AORC_OHRFC_4km', 'AORC_SERFC_4km', 'AORC_WGRFC_4km']

base_directory = '/home/jmframe/aorc_historic/data/downloads'

year = 2020  # Change as needed
month = 5    # Change as needed

for region in regions:
    region_code = region.split('_')[1]
    download_region_data(base_url, region_code, year, month, base_directory)
    break
