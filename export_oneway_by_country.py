import overpass
from utils import sparql
import os
import json
import logging

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")

api = overpass.API(timeout=4000)

# get all countries in Europe from Wikidata
# get list of swiss municipalities incl. zip code
query = """
SELECT ?countryLabel ?country ?isoCode
{
  ?country wdt:P31 wd:Q6256 .
  ?country wdt:P30 wd:Q46 .
  ?country wdt:P297 ?isoCode .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }
}
ORDER BY ?countryLabel
"""

result = sparql.query(query, endpoint="https://query.wikidata.org/sparql")
european_countries = [{k: v["value"] for k, v in m.items()} for m in result]
for country in european_countries:
    logging.debug(f"* Query overpass for {country['countryLabel']}...")
    gj_path = os.path.join(
        __location__, "oneway_countries", f"Oneway_{country['isoCode']}.geojson"
    )
    if os.path.exists(gj_path):
        continue
    query = f"""
    rel["ISO3166-1:alpha2"="{country['isoCode']}"]["boundary"="administrative"];
    map_to_area;
    way["highway"!="motorway"]["highway"!="trunk"]["highway"!="primary_link"]["highway"!="motorway_link"]["highway"!="path"][!"lanes"][!"tramway"][!"railway"]["oneway"="yes"](area);
    out geom;
    """
    logging.debug(f" -> Query: {query}")
    try:
        response = api.get(query, responseformat="geojson")
    except overpass.OverpassError:
        logging.exception(f"Error from Overpass for {country['countryLabel']}")
        pause = input("**** PRESS ANY KEY TO CONTINUE ****")
        continue
    logging.debug(f" -> Found {len(response['features'])} features.")
    with open(gj_path, "w") as f:
        f.write(json.dumps(response, indent=4))
    logging.debug(f" -> Save GeoJSON at {gj_path}.")
