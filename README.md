Oneway map using OSM data
=========================

Source: OSM via Overpass


## Webserver starten

```
python -m RangeHTTPServer 8000
```

### Create Tiles for Basemap

Follow guide: https://docs.protomaps.com/guide/getting-started


1. Download Windows x86_64 release of pmtiles https://github.com/protomaps/go-pmtiles/releases

2. Check planet file

```
pmtiles show https://build.protomaps.com/20241111.pmtiles
```

3. Create bounding box for europe with http://bboxfinder.com/

-24.785156,36.315125,36.914063,71.300793

4. Extract euroep

```
pmtiles extract https://build.protomaps.com/20241111.pmtiles my_area.pmtiles --bbox=-24.785156,36.315125,36.914063,71.300793 --maxzoom=14
```

Download ca. 20GB PMTiles