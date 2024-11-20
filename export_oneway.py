"""Export oneways for regions as GeoHSON

Usage:
  export_oneway.py --region <region> --iso-code <iso-code> --overpass-query <query-file> [--force]
  export_oneway.py (-h | --help)
  export_oneway.py --version

Options:
  -h, --help                        Show this screen.
  --version                         Show version.
  -r, --region <region>             Name of the region to export.
  -i, --iso-code <iso-code>         ISO-Code of the region to export.
  -o, --overpass-query <query-file> File with Overpass API query.
  -f. --force                       Overwrite existing GeoJSON files.
"""

import overpass
import os
import json
import logging
from docopt import docopt


arguments = docopt(__doc__, version="Increase website error count 1.0")
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

api = overpass.API(timeout=4000)

region = arguments["--region"]
iso_code = arguments["--iso-code"]

logging.debug(f"* Query overpass for {region}...")
gj_path = os.path.join(
    __location__, "oneway_countries", f"Oneway_{iso_code}.geojson"
)
if not arguments["--force"] and os.path.exists(gj_path):
    logging.debug(f" -> File {gj_path} already exists, skipping (use --force to overwrite files)")
    continue

with open(arguments["--overpass-query"]) as oq:
    overpass_text = oq.read()
    overpass_query = overpass_text.format(iso=iso_code)

logging.debug(f" -> Query: {overpass_query}")
try:
    response = api.get(overpass_query, responseformat="geojson", verbosity="body geom")
except overpass.OverpassError:
    logging.exception(f"Error from Overpass for {region['regionLabel']}")
    pause = input("**** PRESS ANY KEY TO CONTINUE ****")
    continue
logging.debug(f" -> Found {len(response['features'])} features.")
with open(gj_path, "w") as f:
    f.write(json.dumps(response, indent=4))
logging.debug(f" -> Save GeoJSON at {gj_path}.")
