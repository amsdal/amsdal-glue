#!/bin/bash

# To run the script, execute the command `bash release.sh` and pass the arguments:
#
# 1. Release date in the format "01-01-24".
# 2. List of libraries in the format "library_name/release_version", separated by spaces.
#
# Example command:
#
#       bash release.sh 01-01-24 api-server/0.1.0 amsdal-glue/0.2.0

# The script will perform the following actions:
# 1. Enter each specified library.
# 2. Update the changelog.
# 3. Commit the changes and create a tag.
# 4. After processing all the specified libraries, push the changes and tags, triggering the necessary CI/CD processes for the releases.




if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <release_date> [lib1/release_version] [lib2/release_version] [lib3/release_version] [lib4/release_version] [lib5/release_version]"
  exit 1
fi


RELEASE_DATE=$1
shift

LIBRARIES=("$@")

git checkout -b "release/$RELEASE_DATE"

process_library() {
  local LIB_WITH_VERSION=$1
  IFS='/' read -r LIB_NAME RELEASE_VERSION <<< "$LIB_WITH_VERSION"

  if [ -d ./libs/"$LIB_NAME" ]; then
    echo "Processing library: $LIB_NAME with release version: $RELEASE_VERSION"
    cd ./libs/"$LIB_NAME" || { echo "Failed to change directory to $LIB_NAME"; exit 1; }

    hatch run release $RELEASE_VERSION

    cd ../.. || exit 1
  else
    echo "Library $LIB_NAME does not exist."
  fi
}

for LIB in "${LIBRARIES[@]}"; do
  process_library "$LIB"
done

git push origin "release/$RELEASE_DATE"
git push origin --tags

echo "Branch release/$RELEASE_DATE created and pushed. Libraries processed."
