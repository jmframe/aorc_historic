#!/bin/bash
#SBATCH --job-name=unzip         # Job name
#SBATCH --partition=normal               # Partition (queue) name
#SBATCH --nodes=1                       # Number of nodes
#SBATCH --ntasks=1                      # Number of tasks (processes)
#SBATCH --time=01:00:00                 # Time limit hrs:min:sec
#SBATCH --output=unzip_%j.log   # Standard output and error log

# Run the unzip script
sh /home/jmframe/aorc_historic/scripts/unzip_downloads.sh