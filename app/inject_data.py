import sys
from SPARQLWrapper import SPARQLWrapper, JSON
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask.cli import with_appcontext
from . import app, db, logging
from .models import Human, Film
from datetime import datetime


endpoint_url = "https://query.wikidata.org/sparql"

query = """
#films released in 2017
SELECT DISTINCT
  ?film
  ?filmLabel
  (SAMPLE(?imdbid) as ?a_imdbid)
  (MIN(?pubdate) as ?first_pubdate)
  (MAX(?duration) as ?max_duration)
  (GROUP_CONCAT(DISTINCT ?genre; SEPARATOR=", ") as ?genres)
  (GROUP_CONCAT(DISTINCT ?director; SEPARATOR=", ") as ?directors)
  (GROUP_CONCAT(DISTINCT ?screenwriter; SEPARATOR=", ") as ?screenwriters)
  (GROUP_CONCAT(DISTINCT ?producer; SEPARATOR=", ") as ?producers)
  (GROUP_CONCAT(DISTINCT ?cast_member; SEPARATOR=", ") as ?cast_members)
WHERE {
  {
    SELECT DISTINCT ?film ?filmLabel ?pubdate ?imdbid
    WHERE {
      ?film wdt:P31 wd:Q11424.
      ?film wdt:P577 ?pubdate.
      ?film wdt:P345 ?imdbid.
      FILTER (?pubdate >= "2017-01-01T00:00:00Z"^^xsd:dateTime &&
              ?pubdate <= "2017-12-31T23:59:59Z"^^xsd:dateTime)
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
  }
  OPTIONAL {
    ?film wdt:P2047 ?duration.
  }
  OPTIONAL {
    ?film wdt:P136 ?genre.
  }
  OPTIONAL {
    ?film wdt:P57 ?director.
  }
  OPTIONAL {
    ?film wdt:P58 ?screenwriter.
  }
  OPTIONAL {
    ?film wdt:P162 ?producer.
  }
  OPTIONAL {
    ?film wdt:P161 ?cast_member.
  }
}
GROUP BY ?film ?filmLabel
ORDER BY ?pubdate
"""

query = """
SELECT DISTINCT
?film
?filmLabel
?filmDescription
(SAMPLE(?imdbid) as ?a_imdbid)
(MIN(?pubdate) as ?first_pubdate)
(MAX(?duration) as ?max_duration)
WHERE {
  ?film wdt:P31 wd:Q11424.
  ?film wdt:P577 ?pubdate.
  ?film wdt:P345 ?imdbid.
  OPTIONAL {
    ?film wdt:P2047 ?duration.
  }
  FILTER (?pubdate >= "2013-01-01T00:00:00Z"^^xsd:dateTime)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
GROUP BY ?film ?filmLabel ?filmDescription
"""


def create_from_uri_concact(model, uri_concact):
    obj_arr = []
    for uri in uri_concact.split(', '):
        if not uri: continue
        id = uri.split('/')[-1]
        # Check if the object already exists
        obj = db.session.get(model, id)
        if not obj:
            # Create a new object if it does not exist
            # this sends get request; takes too long
            # obj = model.init_from_uri(uri)
            obj = model(id=id)
            db.session.add(obj)
            db.session.commit()
        obj_arr.append(obj)
    return obj_arr


def fetch_sparql(endpoint_url, query):
    logging.info(f"Fetching data from {endpoint_url}")
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def populate_db(app):
    with app.app_context():
        raw_data = fetch_sparql(endpoint_url, query)

        logging.info(f"Creating model instances")
        for film_data in raw_data['results']['bindings']:

            uri = film_data['film']['value']
            id = uri.split('/')[-1]

            label = film_data['filmLabel']['value']

            description = film_data.get('filmDescription', {}).get('value')

            pubdate = film_data['first_pubdate']['value']
            pubdate = datetime.strptime(pubdate, "%Y-%m-%dT%H:%M:%SZ")

            imdbid = film_data['a_imdbid']['value']

            duration = film_data.get('max_duration', {})
            duration = float(duration.get('value')) if duration.get('type') == 'literal' else None

            film = Film(
                id=id,
                label=label,
                description=description,
                # producers=create_from_uri_concact(Human, film_data['producers']['value']),
                # directors=create_from_uri_concact(Human, film_data['directors']['value']),
                # screenwriters=create_from_uri_concact(Human, film_data['screenwriters']['value']),
                # cast_members=create_from_uri_concact(Human, film_data['cast_members']['value']),
                pubdate=pubdate,
                imdbid=imdbid,
                duration=duration,
            )
            db.session.add(film)

        logging.info(f"Saving data to db")
        db.session.commit()

