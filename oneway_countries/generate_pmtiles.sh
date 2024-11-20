#!/bin/bash

set -e

function cleanup {
    exit $?
}

trap "cleanup" EXIT

DIR="$(cd "$(dirname "$0")" && pwd)"

for country_file in $DIR/*.geojson; do
    if [ -f "${country_file}.pmtiles" ]; then
        echo "${country_file}.pmtiles already exists, continue"
        continue
    fi

    echo "Convert ${country_file} to PMTiles..."
    tippecanoe --projection=EPSG:4326 -o "${country_file}.pmtiles" -l oneway --minimum-zoom=2 --maximum-zoom=18 --drop-densest-as-needed $country_file
done
