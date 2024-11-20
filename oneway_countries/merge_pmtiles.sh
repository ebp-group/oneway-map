#!/bin/bash

set -e

function cleanup {
    exit $?
}

trap "cleanup" EXIT

DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Merge all PMTiles..."
rm -f $DIR/merged.pmtiles
tile-join --overzoom -z 17 -Z 5  -o $DIR/merged.pmtiles $DIR/*.pmtiles
