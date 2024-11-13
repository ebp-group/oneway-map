from SPARQLWrapper import SPARQLWrapper, JSON


def query(query, endpoint="https://register.ld.admin.ch/query"):
    user_agent = "Mozilla Firefox Mozilla/5.0; metaodi oneway-map"
    sparql = SPARQLWrapper(endpoint, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.queryAndConvert()
    return results['results']['bindings']
