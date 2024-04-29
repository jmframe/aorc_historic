#!/bin/bash

# Directory containing the .zip files
SOURCE_DIR="/home/jmframe/data/AORC/downloads"

# Target directory for .nc4 files
TARGET_DIR="/home/jmframe/data/AORC/netcdf"

# Create the target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Export TARGET_DIR so it is available in subshells
export TARGET_DIR

# Find all zip files and unzip them into the target directory
find "$SOURCE_DIR" -type f -name "*.zip" -exec sh -c '
  zip_file="$1"
  echo "Processing $zip_file..."
  # Unzip files directly into the target directory
  unzip -oj "$zip_file" "*.nc4" -d "$TARGET_DIR"
' _ {} \;

echo "Unzipping complete."

