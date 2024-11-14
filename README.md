Oneway map using OSM data
=========================

Source: OSM via Overpass


## Start webserver starten

For local testing, start a webserver that supports range-requests (needed for PMTiles):

```
python -m RangeHTTPServer 8000
```

## Installation

Install Python, create venv and install dependencies:

```
python3 -m venv pyenv
pyenv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Install system dependencies and [tippecanoe](https://github.com/felt/tippecanoe):

```
sudo apt-get install gcc g++ make libsqlite3-dev zlib1g-dev
git clone https://github.com/felt/tippecanoe.git
cd tippecanoe
make -j
sudo make install
```

## Usage

To extract the oneway GeoJSONs from the countries of Europe run:

```
python export_oneway_by_country.py
```

Generate PMTiles from GeoJSONs:

```
bash oneway_countries/generate_pmtiles.sh
mv oneway_countries/merged.pmtiles output/
```

### Create Tiles for Basemap

Follow guide: https://docs.protomaps.com/guide/getting-started

1. Download Windows x86_64 release of pmtiles https://github.com/protomaps/go-pmtiles/releases

2. Check planet file

```
pmtiles show https://build.protomaps.com/20241111.pmtiles
```

3. Create bounding box for europe with http://bboxfinder.com/

=> -24.785156,36.315125,36.914063,71.300793

4. Extract europe

```
pmtiles extract https://build.protomaps.com/20241111.pmtiles europe.pmtiles --bbox=-24.785156,36.315125,36.914063,71.300793
mv europe.pmtiles output/
```

Download ca. 40GB PMTiles, use `--maxzoom=14` to reduce size

### Upload data to MinIO

Create a MinIO instance of fly.io (config in `oneway-minio` directory), see [README](https://github.com/ebp-group/oneway-map/blob/main/oneway-minio/README.md).

```
mc alias set oneway-minio https://oneway-minio.fly.dev <ROOT-USER> <ROOT-PASS>
```

```
mc put output/europe.pmtiles oneway-minio/onway-map
mc put output/merged.pmtiles oneway-minio/onway-map
```


