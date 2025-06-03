from sqlalchemy import (
    Column, Integer, String, ForeignKey,
    ForeignKeyConstraint, UniqueConstraint
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Club(Base):
    __tablename__ = 'clubs'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=True)

    footballers = relationship('Footballer', back_populates='club', cascade='all, delete-orphan')

class Footballer(Base):
    __tablename__ = 'footballers'

    club_id = Column(Integer, ForeignKey('clubs.id'), primary_key=True)
    shirt_number = Column(Integer, primary_key=True)  # composite PK

    name = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    position = Column(String, nullable=True)
    nationality = Column(String, nullable=True)

    club = relationship('Club', back_populates='footballers')

    former_clubs = relationship('FormerClub', back_populates='footballer', cascade='all, delete-orphan')
    season_stats = relationship('SeasonStat', back_populates='footballer', cascade='all, delete-orphan')

class FormerClub(Base):
    __tablename__ = 'former_clubs'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    years_played = Column(String, nullable=True)

    footballer_club_id = Column(Integer, nullable=False)
    footballer_shirt_number = Column(Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['footballer_club_id', 'footballer_shirt_number'],
            ['footballers.club_id', 'footballers.shirt_number']
        ),
    )

    footballer = relationship('Footballer')

class Season(Base):
    __tablename__ = 'seasons'

    id = Column(Integer, primary_key=True)
    year = Column(String, unique=True, nullable=False)  # e.g. "2023/2024"

    season_stats = relationship('SeasonStat', back_populates='season', cascade='all, delete-orphan')

class SeasonStat(Base):
    __tablename__ = 'season_stats'

    id = Column(Integer, primary_key=True)

    footballer_club_id = Column(Integer, nullable=False)
    footballer_shirt_number = Column(Integer, nullable=False)
    season_id = Column(Integer, ForeignKey('seasons.id'), nullable=False)

    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    appearances = Column(Integer, default=0)
    yellow_cards = Column(Integer, default=0)
    red_cards = Column(Integer, default=0)

    __table_args__ = (
        ForeignKeyConstraint(
            ['footballer_club_id', 'footballer_shirt_number'],
            ['footballers.club_id', 'footballers.shirt_number']
        ),
        UniqueConstraint('footballer_club_id', 'footballer_shirt_number', 'season_id', name='uix_footballer_season')
    )

    footballer = relationship('Footballer')
    season = relationship('Season', back_populates='season_stats')