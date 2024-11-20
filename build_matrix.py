from utils import sparql
import os
import json


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

config = {
    "europe": {
        "region_query": "europe.sparql",
        "overpass": "oneway_country.overpassql",
    },
    "france": {
        "region_query": "france.sparql",
        "overpass": "oneway_regions.overpassql",
    },
}


def load_file(path):
    with open(path) as f:
        text = f.read()
    return text


matrix_config = []
for r, r_config in config.items():
    query = load_file(r_config["region_query"])

    result = sparql.query(query, endpoint="https://query.wikidata.org/sparql")
    regions = [{k: v["value"] for k, v in m.items()} for m in result]
    # add overpass to regions
    for region in regions:
        region["overpass_query"] = r_config["overpass"]

    matrix_config.extend(regions)

# output matrix as JSON
matrix = {"include": regions}
print(json.dumps(matrix))
