#!/bin/bash

#
# Run covid19co_pipe.py Python script
#

# Go to source code
cd ./src
# Run Python script
echo "Running Colombia Covid19 Pipeline ..."
python3 covid19co_pipe.py
# Check any error
if [ $? -eq 0 ]; then
    # Run Python script
    echo "Running Colombia Covid19 Time Line ..."
    python3 covid19co_timeline.py
    # Go back to main directory
    cd ../
    # Finish without error
    echo "Pipeline output is generated within ./output directory."
    echo "Finished !"
    echo ""
    # Success
    exit 0
else
    # Go back to main directory
    cd ../
    # Finish with error
    echo "Finish with errors ! FAIL"
    echo ""
    # Fail
    exit -1
fi
