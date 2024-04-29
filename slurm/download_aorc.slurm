#!/bin/bash
#SBATCH --job-name=aorc_download         # Job name
#SBATCH --partition=normal               # Partition (queue) name
#SBATCH --nodes=1                       # Number of nodes
#SBATCH --ntasks=1                      # Number of tasks (processes)
#SBATCH --time=01:00:00                 # Time limit hrs:min:sec
#SBATCH --output=aorc_download_%j.log   # Standard output and error log

module load Anaconda3                    # Load Anaconda module if required
MAIN_DIR="/home/jmframe/aorc_historic/"
source activate "${MAIN_DIR}environment/.conda/envs/aorc_env"

# Run the download script
python "${MAIN_DIR}src/download_AORC_by_year_and_month.py" --config "${MAIN_DIR}config_files/download_2020_05_config.yml"