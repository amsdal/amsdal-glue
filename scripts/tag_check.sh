#!/bin/bash

OWNER="amsdal"
REPO="amsdal-glue"


declare -A folder_tags

folder_tags["./libs/amsdal-glue/src/amsdal_glue"]="glue"
folder_tags["./libs/api-server/src/amsdal_glue_api_server"]="api-server"
folder_tags["./libs/connections/src/amsdal_glue_connections"]="connections"
folder_tags["./libs/core/src/amsdal_glue_core"]="core"
folder_tags["./libs/sql-parser/src/amsdal_glue_sql_parser"]="sql-parser"


file_name="__about__.py"

version_regex="^__version__ = ['\"](.*)['\"]"

CHECK_TAGS=()
REPO_TAGS=()

extract_info() {
    local folder=$1
    local tag=$2
    local file_path="$folder/$file_name"
    local version=""

    if [[ -f "$file_path" ]]; then
        while IFS= read -r line; do
            if [[ $line =~ $version_regex ]]; then
                version="${BASH_REMATCH[1]}"
                break
            fi
        done < "$file_path"

        if [[ -n $version ]]; then
            echo "Folder: $folder, Version: $version, Tag: $tag"
            CHECK_TAGS+=("$tag/v$version")
        else
            echo "Folder: $folder, Version not found"
        fi
    else
        echo "File $file_path does not exist"
    fi
}

fetch_repo_tags() {
    local page=1
    local per_page=100
    local tags

    while :; do
        tags=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
                "https://api.github.com/repos/$OWNER/$REPO/tags?page=$page&per_page=$per_page" | jq -r '.[].name')

        if [[ -z $tags ]]; then
            break
        fi

        REPO_TAGS+=($tags)
        ((page++))
    done
}

for folder in "${!folder_tags[@]}"; do
    extract_info "$folder" "${folder_tags[$folder]}"
done

fetch_repo_tags


for TAG in "${CHECK_TAGS[@]}"; do
  if [[ " ${REPO_TAGS[@]} " =~ " $TAG " ]]; then
    echo "Tag $TAG exists in the repository."
  else
    echo "Tag $TAG does not exist in the repository."
    git tag $TAG
    git push origin $TAG
  fi
done

