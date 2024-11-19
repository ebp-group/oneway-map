import overpass
from utils import sparql
import os
import json
import logging
import time

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")

api = overpass.API(timeout=4000)

# get all part of France from Wikidata
query = """
SELECT DISTINCT ?regionLabel ?region ?isoCode
{
  ?region wdt:P31/wdt:P279* wd:Q36784 . # Region in France
  ?region wdt:P300 ?isoCode .
  FILTER NOT EXISTS {
    ?region wdt:P31/wdt:P279* wd:Q202216 . # oversea territory
  }
  FILTER NOT EXISTS {
    ?region wdt:P1366 ?endDate . # replacedBy
  }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
}
ORDER BY ?isoCode
"""

result = sparql.query(query, endpoint="https://query.wikidata.org/sparql")
regions = [{k: v["value"] for k, v in m.items()} for m in result]
for region in regions:
    logging.debug(f"* Query overpass for {region['regionLabel']}...")
    gj_path = os.path.join(
        __location__, "oneway_countries", f"Oneway_{region['isoCode']}.geojson"
    )
    if os.path.exists(gj_path):
        continue
    query = f"""
    rel["ISO3166-2"="{region['isoCode']}"]["boundary"="administrative"];
    map_to_area;
    way["highway"!="motorway"]["highway"!="trunk"]["highway"!="primary_link"]["highway"!="motorway_link"]["highway"!="path"][!"lanes"][!"tramway"][!"railway"]["oneway"="yes"](area);
    """
    logging.debug(f" -> Query: {query}")
    try:
        response = api.get(query, responseformat="geojson", verbosity="body geom")
        time.sleep(5)
    except overpass.OverpassError:
        logging.exception(f"Error from Overpass for {region['regionLabel']}")
        pause = input("**** PRESS ANY KEY TO CONTINUE ****")
        continue
    logging.debug(f" -> Found {len(response['features'])} features.")
    with open(gj_path, "w") as f:
        f.write(json.dumps(response, indent=4))
    logging.debug(f" -> Save GeoJSON at {gj_path}.")
