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

