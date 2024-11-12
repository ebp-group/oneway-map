from SPARQLWrapper import SPARQLWrapper, JSON


def query(query, endpoint="https://register.ld.admin.ch/query"):
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.queryAndConvert()
    return results['results']['bindings']