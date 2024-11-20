echo "Merge all PMTiles..."
rm -f $DIR/merged.pmtiles
tile-join --overzoom -z 17 -Z 5  -o $DIR/merged.pmtiles $DIR/*.pmtiles
