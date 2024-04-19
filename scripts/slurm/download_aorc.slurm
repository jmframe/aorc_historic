#!/bin/bash
#SBATCH --job-name=aorc_download         # Job name
#SBATCH --partition=normal               # Partition (queue) name
#SBATCH --nodes=1                       # Number of nodes
#SBATCH --ntasks=1                      # Number of tasks (processes)
#SBATCH --time=01:00:00                 # Time limit hrs:min:sec
#SBATCH --output=aorc_download_%j.log   # Standard output and error log

module load Anaconda3                    # Load Anaconda module if required
source activate /home/jmframe/aorc_historic/environment/.conda/envs/aorc_env

# Run the download script
python /home/jmframe/aorc_historic/scripts/download_AORC_by_year_and_month.py
