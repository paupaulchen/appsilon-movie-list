from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Table, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property


"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""
class WikidataEntityMixin:
    id = Column(Integer, primary_key=True)
    label =  Column(String(100), unique=False, nullable=True)
    description =  Column(String(100), unique=False, nullable=True)

    def __repr__(self):
        return self.label | self.id
    
    @hybrid_property
    def uri(self):
        return f"http://www.wikidata.org/entity/{self.id}"


def film_crew_relationship_factory(crew_title: str):
    assoc_table = Table(
        f'assoc_film_{crew_title}',
        Model.metadata,
        Column('id', Integer, primary_key=True),
        Column('film_id', Integer, ForeignKey('film.id')),
        Column('human_id', Integer, ForeignKey('human.id'))
    )
    return relationship('Human', secondary=assoc_table, backref=f'{crew_title}_of')


class Human(Model, WikidataEntityMixin):
    ...


class FilmGenre(Model, WikidataEntityMixin):
    ...


class Film(Model, WikidataEntityMixin):
    producers = film_crew_relationship_factory('producer')
    directors = film_crew_relationship_factory('director')
    screenwriters = film_crew_relationship_factory('screenwriter')
    cast_members = film_crew_relationship_factory('cast_member')
    pubdate = Column(Date, unique=False, nullable=False)
    imdbid = Column(String(20), unique=True, nullable=False)
    imdbid = Column(Float, unique=False, nullable=True)
