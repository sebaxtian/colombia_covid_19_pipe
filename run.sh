#!/bin/bash

#
# Run the colombia_covid_19_pipe.py Python script
#

echo "Running Colombia Covid 19 Pipeline ..."
source .venv/bin/activate
cd ./src
python colombia_covid_19_pipe.py
cd ../
echo "Finished !"
echo "The Pipeline output is generated within ./output directory."
