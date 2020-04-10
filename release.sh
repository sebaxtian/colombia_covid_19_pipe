#!/bin/bash

#
# Create new release tag
#

# Run Colombia Covid 19 Pipeline
#./run.sh
echo ""
# Check any error
if [ $? -eq 0 ]; then
    # Check the last version tag
    LAST_VERSION=$(hub release | head -n 1)
    echo "Last release $LAST_VERSION"
    # Get the last patch
    N=$(hub release | head -n 1 | tail -c 2)
    N=$(($N + 1))
    #echo "N: $N"
    # Create version tag
    VERSION="$(date +%m).$(date +%d).$N"
    VERSION=$(echo $VERSION | cut -c2-)
    # Create new release
    echo "Creating new release $VERSION ..."
    git tag -a $VERSION -m "$VERSION" master
    git push --tags
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
