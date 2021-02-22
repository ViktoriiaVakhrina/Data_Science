from core import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base



# Table name -> 'association'
# Columns: 'actor_id' -> db.Integer, db.ForeignKey -> 'actors.id', primary_key = True
#          'movie_id' -> db.Integer, db.ForeignKey -> 'movies.id', primary_key = True

association = db.Table('association',
                     Column('actor_id', Integer, ForeignKey('actors.id'), primary_key=True),
                     Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True))
