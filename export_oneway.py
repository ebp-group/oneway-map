"""Export oneways for regions as GeoHSON

Usage:
  export_oneway.py --region-query <query-file> --overpass-query <query-file> [--force]
  export_oneway.py (-h | --help)
  export_oneway.py --version

Options:
  -h, --help                        Show this screen.
  --version                         Show version.
  -r, --region-query <query-file>   File with SPARQL query for regions.
  -o, --overpass-query <query-file> File with Overpass API query.
  -f. --force                       Overwrite existing GeoJSON files.
"""

import overpass
from utils import sparql
import os
import json
import logging
import time
from docopt import docopt


arguments = docopt(__doc__, version="Increase website error count 1.0")
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


# get all part of France from Wikidata
with open(arguments["--region-query"]) as rq:
    query = rq.read()

result = sparql.query(query, endpoint="https://query.wikidata.org/sparql")
regions = [{k: v["value"] for k, v in m.items()} for m in result]
api = overpass.API(timeout=4000)
for region in regions:
    logging.debug(f"* Query overpass for {region['regionLabel']}...")
    gj_path = os.path.join(
        __location__, "oneway_countries", f"Oneway_{region['isoCode']}.geojson"
    )
    if not arguments["--force"] and os.path.exists(gj_path):
        logging.debug(f" -> File {gj_path} already exists, skipping (use --force to overwrite files)")
        continue

    with open(arguments["--overpass-query"]) as oq:
        overpass_text = oq.read()
        overpass_query = overpass_text.format(iso=region["isoCode"])

    logging.debug(f" -> Query: {overpass_query}")
    try:
        response = api.get(overpass_query, responseformat="geojson", verbosity="body geom")
        time.sleep(5)
    except overpass.OverpassError:
        logging.exception(f"Error from Overpass for {region['regionLabel']}")
        pause = input("**** PRESS ANY KEY TO CONTINUE ****")
        continue
    logging.debug(f" -> Found {len(response['features'])} features.")
    with open(gj_path, "w") as f:
        f.write(json.dumps(response, indent=4))
    logging.debug(f" -> Save GeoJSON at {gj_path}.")
