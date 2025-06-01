from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Club(Base):
    __tablename__ = 'clubs'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)

    footballers = relationship('Footballer', back_populates='club')

class Footballer(Base):
    __tablename__ = 'footballers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    shirt_number = Column(Integer)          # <-- Add this line
    age = Column(Integer)
    position = Column(String)
    nationality = Column(String)

    club_id = Column(Integer, ForeignKey('clubs.id'))
    club = relationship('Club', back_populates='footballers')

    former_clubs = relationship('FormerClub', back_populates='footballer')

class FormerClub(Base):
    __tablename__ = 'former_clubs'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    years_played = Column(String)

    footballer_id = Column(Integer, ForeignKey('footballers.id'))
    footballer = relationship('Footballer', back_populates='former_clubs')


from lib import Base, engine

Base.metadata.create_all(engine)