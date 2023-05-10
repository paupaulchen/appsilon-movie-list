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


class Human(BaseWikidataEntity):
    ...


assoc_screenwriter = Table(
    'screenwriter',
    Model.metadata,
    Column('id', Integer, primary_key=True),
    Column('movie_id', Integer, ForeignKey('movie.id')),
    Column('human_id', Integer, ForeignKey('human.id'))
)


assoc_director = Table(
    'director',
    Model.metadata,
    Column('id', Integer, primary_key=True),
    Column('movie_id', Integer, ForeignKey('movie.id')),
    Column('human_id', Integer, ForeignKey('human.id'))
)


assoc_cast_member = Table(
    'cast_member',
    Model.metadata,
    Column('id', Integer, primary_key=True),
    Column('movie_id', Integer, ForeignKey('movie.id')),
    Column('human_id', Integer, ForeignKey('human.id'))
)


class FilmGenre(BaseWikidataEntity):
    ...


class Movie(BaseWikidataEntity):
    director = relationship('Human', secondary=assoc_director, backref='movie')
    cast_member = relationship('Human', secondary=assoc_cast_member, backref='movie')
    screenwriter = relationship('Human', secondary=assoc_screenwriter, backref='movie')
    pubdate = Column(Date, unique=False, nullable=False)
    imdbid = Column(String(20), unique=False, nullable=False)
