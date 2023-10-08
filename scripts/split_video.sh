#!/bin/bash

# Get the filename without the extension
filename=$(basename -- "$1")
filename_noext="${filename%.*}"

# Remove whitespaces and special characters from the filename
sanitized_filename=$(echo "$filename_noext" | sed 's/[^a-zA-Z0-9]//g')

# Generate a timestamp
timestamp=$(date +"%Y%m%d%H%M%S")

# Create a subdirectory in ./output with the sanitized original filename and a timestamp
mkdir -p "./output/${sanitized_filename}_${timestamp}"

# Run ffmpeg to split the video into frames
ffmpeg -i "$1" -vf fps=1 "./output/${sanitized_filename}_${timestamp}/frame_%04d.png"

# Logging
echo "Input File: $1"
echo "Original File Name: $filename_noext"
echo "Sanitized File Name: $sanitized_filename"
echo "Timestamp: $timestamp"
echo "Subfolder: ${sanitized_filename}_${timestamp}"
