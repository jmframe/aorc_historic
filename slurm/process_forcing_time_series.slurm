#!/bin/bash
#SBATCH --job-name=process_2020_05_9513780       # Job name
#SBATCH --partition=normal               # Partition (queue) name
#SBATCH --nodes=1                       # Number of nodes
#SBATCH --ntasks=10                      # Number of tasks (processes)
#SBATCH --time=01:00:00                 # Time limit hrs:min:sec
#SBATCH --output=process_2020_05_9513780_%j.log       # Standard output and error log

MAIN_DIR="/home/jmframe/aorc_historic/"

# Source the Conda configuration
source /apps/Anaconda3/2023.09/etc/profile.d/conda.sh

# Activate the environment
conda activate ${MAIN_DIR}environment/.conda/envs/aorc_env

# Path to the YAML configuration file
CONFIG_PATH="${MAIN_DIR}/config_files/process_2020_05_9513780.yml"

# Run the Python script with the configuration file
python3 -u "${MAIN_DIR}src/process_forcing_time_series.py" $CONFIG_PATH
