# AORC Data Download and Processing Scripts

This repository contains scripts for downloading and processing temperature and precipitation data from the NOAA AORC (Advanced Hydrologic Prediction Service Operational Remote Sensing Center) historical archive. The script is designed to fetch data for specified regions and time periods, organizing the downloads into a structured directory format.

## Project Structure

- `/aorc-historic/` - Main directory for downloaded data.
- `download_AORC_by_year_and_month.py` - Python script to automate the downloading of data.

## Environment Setup

The script runs within a Conda environment to ensure that all dependencies are managed correctly.

### Creating the Environment

To create the environment, ensure you have Anaconda installed, then run:

```bash
conda env create -f environment.yml  
```

This will set up the environment as per the configurations specified in `environment.yml`.

Environment Path

The Conda environment is created in a specific directory to avoid confusion with user directories, ensuring clarity that it is meant for the environment:
`/home/jmframe/aorc_historic/environment/.conda/envs/aorc_env`

## Usage
To run the script, navigate to the aorc-historic directory and activate the environment:

```bash
cd /home/jmframe/aorc_historic
conda activate ./environment/.conda/envs/aorc_env
```

Then execute the script by specifying the year and month for which you want to download data:

```bash
./download_AORC_by_year_and_month.py
```

### Configuring the Script

Edit the year and month variables in the script to fetch data for different periods as required.

### Data Handling

The downloaded ZIP files are automatically placed in the aorc-historic directory under corresponding regional subdirectories to mimic the structure from the NOAA AORC server.


## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
