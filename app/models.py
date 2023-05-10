from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property


"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""
class BaseWikidataEntity(Model, AuditMixin):
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
        crew_title,
        Model.metadata,
        Column('id', Integer, primary_key=True),
        Column('movie_id', Integer, ForeignKey('movie.id')),
        Column('human_id', Integer, ForeignKey('human.id'))
    )
    return relationship('Human', secondary=assoc_table, backref='movie')


class Human(BaseWikidataEntity):
    ...


class FilmGenre(BaseWikidataEntity):
    ...


class Movie(BaseWikidataEntity):
    producer = film_crew_relationship_factory('producer')
    director = film_crew_relationship_factory('director')
    screenwriter = film_crew_relationship_factory('screenwriter')
    cast_member = film_crew_relationship_factory('cast_member')
    pubdate = Column(Date, unique=False, nullable=False)
    imdbid = Column(String(20), unique=True, nullable=False)
