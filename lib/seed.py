from lib import session
from lib.models import Club, Footballer, Season, SeasonStat

# --- Create Clubs ---
clubs = [
    Club(name="Manchester City", location="Manchester"),
    Club(name="Liverpool", location="Liverpool"),
    Club(name="Chelsea", location="London"),
]

session.add_all(clubs)
session.commit()  # commit so clubs have IDs for FK relations

# --- Create Footballers per Club ---
footballers = [
    # Manchester City (club_id = clubs[0].id)
    Footballer(name="Ederson", shirt_number=1, age=30, position="Goalkeeper", nationality="Brazilian", club=clubs[0]),
    Footballer(name="Kevin De Bruyne", shirt_number=17, age=31, position="Midfielder", nationality="Belgian", club=clubs[0]),
    Footballer(name="Erling Haaland", shirt_number=9, age=23, position="Forward", nationality="Norwegian", club=clubs[0]),
    Footballer(name="Ruben Dias", shirt_number=3, age=26, position="Defender", nationality="Portuguese", club=clubs[0]),
    Footballer(name="Phil Foden", shirt_number=10, age=23, position="Midfielder", nationality="English", club=clubs[0]),

    # Liverpool (club_id = clubs[1].id)
    Footballer(name="Alisson Becker", shirt_number=1, age=31, position="Goalkeeper", nationality="Brazilian", club=clubs[1]),
    Footballer(name="Virgil van Dijk", shirt_number=4, age=32, position="Defender", nationality="Dutch", club=clubs[1]),
    Footballer(name="Mohamed Salah", shirt_number=11, age=30, position="Forward", nationality="Egyptian", club=clubs[1]),
    Footballer(name="Jordan Henderson", shirt_number=14, age=33, position="Midfielder", nationality="English", club=clubs[1]),
    Footballer(name="Trent Alexander-Arnold", shirt_number=66, age=25, position="Defender", nationality="English", club=clubs[1]),

    # Chelsea (club_id = clubs[2].id)
    Footballer(name="Kepa Arrizabalaga", shirt_number=1, age=28, position="Goalkeeper", nationality="Spanish", club=clubs[2]),
    Footballer(name="Reece James", shirt_number=24, age=23, position="Defender", nationality="English", club=clubs[2]),
    Footballer(name="Mason Mount", shirt_number=19, age=25, position="Midfielder", nationality="English", club=clubs[2]),
    Footballer(name="Raheem Sterling", shirt_number=7, age=28, position="Forward", nationality="English", club=clubs[2]),
    Footballer(name="Thiago Silva", shirt_number=6, age=38, position="Defender", nationality="Brazilian", club=clubs[2]),
]

session.add_all(footballers)
session.commit()

# --- Create Seasons ---
seasons = [
    Season(year="2023"),
    Season(year="2024"),
]

session.add_all(seasons)
session.commit()

# --- Create Season Stats (sample data) ---
# For each club's players, for each season, create some stats
for club in clubs:
    for player in club.footballers[:5]:  # first 5 players in each club (since we have 5 per club)
        for season in seasons:
            stats = SeasonStat(
                footballer_club_id=club.id,
                footballer_shirt_number=player.shirt_number,
                season_id=season.id,
                goals=5 if player.position == "Forward" else 0,
                assists=3 if player.position in ["Forward", "Midfielder"] else 0,
                appearances=20,
                yellow_cards=2,
                red_cards=0
            )
            session.add(stats)

session.commit()

print("Database seeded players and stats successfully!")