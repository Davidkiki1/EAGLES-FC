from lib import session
from lib.models import Club, Footballer

man_city = Club(name="Manchester City", location="Manchester")

footballers = [
    Footballer(name="Ederson", shirt_number=1, age=30, position="Goalkeeper", nationality="Brazilian", club=man_city),
    Footballer(name="Kyle Walker", shirt_number=2, age=33, position="Defender", nationality="English", club=man_city),
    Footballer(name="Ruben Dias", shirt_number=3, age=26, position="Defender", nationality="Portuguese", club=man_city),
    Footballer(name="João Cancelo", shirt_number=4, age=28, position="Defender", nationality="Portuguese", club=man_city),
    Footballer(name="John Stones", shirt_number=5, age=28, position="Defender", nationality="English", club=man_city),
    Footballer(name="Nathan Aké", shirt_number=6, age=28, position="Defender", nationality="Dutch", club=man_city),
    Footballer(name="Jack Grealish", shirt_number=7, age=28, position="Midfielder", nationality="English", club=man_city),
    Footballer(name="İlkay Gündoğan", shirt_number=8, age=33, position="Midfielder", nationality="German", club=man_city),
    Footballer(name="Erling Haaland", shirt_number=9, age=23, position="Forward", nationality="Norwegian", club=man_city),
    Footballer(name="Phil Foden", shirt_number=10, age=23, position="Midfielder", nationality="English", club=man_city),
    Footballer(name="Bernardo Silva", shirt_number=11, age=29, position="Midfielder", nationality="Portuguese", club=man_city),
    Footballer(name="Julian Alvarez", shirt_number=14, age=23, position="Forward", nationality="Argentine", club=man_city),
    Footballer(name="Rodri", shirt_number=16, age=27, position="Midfielder", nationality="Spanish", club=man_city),
    Footballer(name="Kevin De Bruyne", shirt_number=17, age=31, position="Midfielder", nationality="Belgian", club=man_city),
    Footballer(name="Riyad Mahrez", shirt_number=20, age=32, position="Forward", nationality="Algerian", club=man_city),
    Footballer(name="Cole Palmer", shirt_number=21, age=22, position="Midfielder", nationality="English", club=man_city),
    Footballer(name="Jack Harrison", shirt_number=25, age=26, position="Midfielder", nationality="English", club=man_city),
    Footballer(name="Benjamin Mendy", shirt_number=26, age=29, position="Defender", nationality="French", club=man_city),
    Footballer(name="Julian Weigl", shirt_number=27, age=28, position="Midfielder", nationality="German", club=man_city),
    Footballer(name="Tommy Doyle", shirt_number=47, age=22, position="Midfielder", nationality="English", club=man_city),
]

session.add(man_city)
session.add_all(footballers)
session.commit()

print("Database seeded with Manchester City players!")