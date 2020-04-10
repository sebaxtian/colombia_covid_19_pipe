#!/bin/bash

#
# Create new release tag
#

# Run Colombia Covid 19 Pipeline
./run.sh
# Check any error
if [ $? -eq 0 ]; then
    echo "Running Colombia Covid 19 Pipeline Release ..."
    # Check the last version tag
    LAST_VERSION=$(hub release | head -n 1)
    echo "Lastest release $LAST_VERSION"
    # Get the last patch
    N=$(echo $LAST_VERSION | tr "." "\n" | tail -n -1)
    N=$(($N + 1))
    # Create version tag
    VERSION="$(($(date +%m))).$(date +%d).$N"
    # Create new release
    echo "Creating new release $VERSION ..."
    git config --global user.email 'sebaxtianrioss@gmail.com'
    git config --global user.name 'Sebastian Rios Sabogal'
    git tag -a $VERSION -m "$VERSION" master
    git push --tags
    # Check any error
    if [ $? -eq 0 ]; then
        # Create covid19.zip file for assets release
        zip -r ./output/covid19.zip output/
        # Create GitHub release
        hub release create -a ./output/covid19.zip -m "v$VERSION" $VERSION
        # Finish without error
        echo "Finished !"
        echo "Release $VERSION was created."
        # Success
        exit 0
    else
        # Finish with error
        echo "Finish with errors ! FAIL"
        # Fail
        exit -1
    fi
else
    # Finish with error
    echo "Finish with errors ! FAIL"
    # Fail
    exit -1
fi
