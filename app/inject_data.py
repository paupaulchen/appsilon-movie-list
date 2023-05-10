# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

query = """
#Movies released in 2017
SELECT DISTINCT
  ?movie
  ?movieLabel
  ?imdbid
  (MIN(?pubdate) as ?first_pubdate)
  (MAX(?duration) as ?max_duration)
  (GROUP_CONCAT(DISTINCT ?genre; SEPARATOR=", ") as ?genres)
  (GROUP_CONCAT(DISTINCT ?director; SEPARATOR=", ") as ?directors)
  (GROUP_CONCAT(DISTINCT ?screenwriter; SEPARATOR=", ") as ?screenwriters)
  (GROUP_CONCAT(DISTINCT ?producer; SEPARATOR=", ") as ?producers)
  (GROUP_CONCAT(DISTINCT ?cast_member; SEPARATOR=", ") as ?cast_members)
WHERE {
  {
    SELECT DISTINCT ?movie ?movieLabel ?pubdate ?imdbid
    WHERE {
      ?movie wdt:P31 wd:Q11424.
      ?movie wdt:P577 ?pubdate.
      ?movie wdt:P345 ?imdbid.
      FILTER (?pubdate >= "2017-01-01T00:00:00Z"^^xsd:dateTime &&
              ?pubdate <= "2017-12-31T23:59:59Z"^^xsd:dateTime)
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
  }
  OPTIONAL {
    ?movie wdt:P2047 ?duration.
  }
  OPTIONAL {
    ?movie wdt:P136 ?genre.
  }
  OPTIONAL {
    ?movie wdt:P57 ?director.
  }
  OPTIONAL {
    ?movie wdt:P58 ?screenwriter.
  }
  OPTIONAL {
    ?movie wdt:P162 ?producer.
  }
  OPTIONAL {
    ?movie wdt:P161 ?cast_member.
  }
}
GROUP BY ?movie ?movieLabel ?imdbid
ORDER BY ?pubdate
"""


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)

for result in results["results"]["bindings"]:
    print(result)
