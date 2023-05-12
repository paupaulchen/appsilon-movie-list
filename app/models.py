from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Table, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
import requests


"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""
class WikidataEntityMixin:
    id = Column(String(20), primary_key=True)
    label =  Column(String(100), unique=False, nullable=True)
    description =  Column(String(100), unique=False, nullable=True)

    def __repr__(self):
        return self.label or self.id
    
    @hybrid_property
    def uri(self):
        return f"http://www.wikidata.org/entity/{self.id}"
    
    @classmethod
    def init_from_uri(cls, uri, *args, **kwargs):
        id = uri.split('/')[-1]
        kwargs.setdefault('id', id)
        response = requests.get(uri)
        entity = response.json().get('entities', {}).get(id, {})
        label = entity.get('labels', {}).get('en', {}).get('value')
        kwargs.setdefault('label', label)
        description = entity.get('descriptions', {}).get('en', {}).get('value')
        kwargs.setdefault('description', description)
        return cls(*args, **kwargs)


def film_crew_relationship_factory(crew_title: str):
    assoc_table = Table(
        f'assoc_film_{crew_title}',
        Model.metadata,
        Column('id', Integer, primary_key=True),
        Column('film_id', Integer, ForeignKey('film.id')),
        Column('human_id', Integer, ForeignKey('human.id'))
    )
    return relationship('Human', secondary=assoc_table, backref=f'{crew_title}_of')


class Human(WikidataEntityMixin, Model):
    ...


class FilmGenre(WikidataEntityMixin, Model):
    ...


class Film(WikidataEntityMixin, Model):
    # producers = film_crew_relationship_factory('producer')
    # directors = film_crew_relationship_factory('director')
    # screenwriters = film_crew_relationship_factory('screenwriter')
    # cast_members = film_crew_relationship_factory('cast_member')
    pubdate = Column(Date, unique=False, nullable=False)
    imdbid = Column(String(20), unique=False, nullable=False)
    duration = Column(Float, unique=False, nullable=True)
