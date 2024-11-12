#!/bin/bash

set -e

function cleanup {
    exit $?
}

trap "cleanup" EXIT

DIR="$(cd "$(dirname "$0")" && pwd)"

for country_file in $DIR/*.geojson; do
    echo "Convert ${country_file} to PMTiles..."
    tippecanoe --projection=EPSG:4326 -o "${country_file}.pmtiles" -l oneway --minimum-zoom=5 --maximum-zoom=17 $country_file
done

echo "Merge all PMTiles..."
tile-join --overzoom -z 17 -Z 5 -o $DIR/merged.pmtiles $DIR/*.pmtiles
mv $DIR/merged.pmtiles $DIR/output