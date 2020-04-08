#!/bin/bash

#
# Run the colombia_covid_19_pipe.py Python script
#

echo "Running Colombia Covid 19 Pipeline ..."
# Load Python environment
source .venv/bin/activate
# Go to source code
cd ./src
# Run Python script
python colombia_covid_19_pipe.py
# Go back to main directory
cd ../
# Finish
echo "Finished !"
echo "The Pipeline output is generated within ./output directory."
