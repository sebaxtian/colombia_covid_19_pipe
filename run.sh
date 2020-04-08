#!/bin/bash

#
# Run the colombia_covid_19_pipe.py Python script
#

# Create and Load Python environment
echo "Setup Python environment ..."
python3 -m venv .venv
source .venv/bin/activate
# Install Python requirements
echo "Install Python requirements ..."
pip3 install -r requirements.txt
# Go to source code
cd ./src
# Run Python script
echo "Running Colombia Covid 19 Pipeline ..."
python3 colombia_covid_19_pipe.py
# Go back to main directory
cd ../
# Finish
echo "Finished !"
echo "The Pipeline output is generated within ./output directory."
