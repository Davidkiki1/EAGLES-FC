from lib import session
from lib.models import Club, Footballer, FormerClub, Season, SeasonStat
from tabulate import tabulate

def print_table(data, headers):
    print(tabulate(data, headers, tablefmt="fancy_grid"))

def select_club():
    clubs = session.query(Club).all()
    if not clubs:
        print("No clubs found. Please add clubs first.")
        return None
    print("\nAvailable Clubs:")
    for i, club in enumerate(clubs, 1):
        print(f"{i}. {club.name} ({club.location})")
    choice = input("Select club by number: ").strip()
    try:
        idx = int(choice) - 1
        return clubs[idx]
    except (IndexError, ValueError):
        print("Invalid choice.")
        return None

def list_footballers(club):
    footballers = club.footballers
    if not footballers:
        print(f"No footballers found in {club.name}.")
        return
    data = []
    for f in footballers:
        data.append([f.shirt_number, f.name, f.position or 'N/A', f.age or 'N/A', f.nationality or 'N/A'])
    headers = ["Shirt #", "Name", "Position", "Age", "Nationality"]
    print(f"\n--- Footballers in {club.name} ---")
    print_table(data, headers)

def show_footballer_details(club):
    shirt_num = input("Enter footballer shirt number: ").strip()
    if not shirt_num.isdigit():
        print("Invalid shirt number.")
        return
    shirt_num = int(shirt_num)
    footballer = session.query(Footballer).filter_by(club_id=club.id, shirt_number=shirt_num).first()
    if footballer:
        print(f"\nDetails for {footballer.name} (#{footballer.shirt_number}):")
        print(f"Age: {footballer.age or 'N/A'}")
        print(f"Position: {footballer.position or 'N/A'}")
        print(f"Nationality: {footballer.nationality or 'N/A'}")

        # Former clubs
        if footballer.former_clubs:
            print("\nFormer Clubs:")
            data = [[fc.name, fc.years_played or 'N/A'] for fc in footballer.former_clubs]
            print_table(data, ["Club Name", "Years Played"])
        else:
            print("No former clubs on record.")

        # Show season stats
        if footballer.season_stats:
            print("\nSeason Stats:")
            data = []
            for stat in footballer.season_stats:
                data.append([
                    stat.season.year,
                    stat.goals,
                    stat.assists,
                    stat.appearances,
                    stat.yellow_cards,
                    stat.red_cards
                ])
            print_table(data, ["Season", "Goals", "Assists", "Appearances", "Yellow Cards", "Red Cards"])
        else:
            print("No season stats available.")
    else:
        print("Footballer not found.")
    print()

def add_footballer(club):
    print(f"Adding new footballer to {club.name}:")
    name = input("Name: ").strip()
    shirt_number = input("Shirt Number: ").strip()
    if not shirt_number.isdigit():
        print("Shirt number must be a number.")
        return
    shirt_number = int(shirt_number)
    existing = session.query(Footballer).filter_by(club_id=club.id, shirt_number=shirt_number).first()
    if existing:
        print(f"Shirt number {shirt_number} already taken in this club.")
        return
    age = input("Age: ").strip()
    age = int(age) if age.isdigit() else None
    position = input("Position: ").strip()
    nationality = input("Nationality: ").strip()

    footballer = Footballer(
        club_id=club.id,
        shirt_number=shirt_number,
        name=name,
        age=age,
        position=position,
        nationality=nationality
    )
    session.add(footballer)
    session.commit()
    print(f"{name} added to {club.name}.\n")

def update_footballer(club):
    shirt_number = input("Enter shirt number of footballer to update: ").strip()
    if not shirt_number.isdigit():
        print("Invalid shirt number.")
        return
    shirt_number = int(shirt_number)
    footballer = session.query(Footballer).filter_by(club_id=club.id, shirt_number=shirt_number).first()
    if not footballer:
        print("Footballer not found.")
        return

    print(f"Updating {footballer.name} (#{footballer.shirt_number}):")
    age = input(f"New Age [{footballer.age or 'N/A'}]: ").strip()
    footballer.age = int(age) if age.isdigit() else footballer.age

    position = input(f"New Position [{footballer.position or 'N/A'}]: ").strip()
    footballer.position = position if position else footballer.position

    nationality = input(f"New Nationality [{footballer.nationality or 'N/A'}]: ").strip()
    footballer.nationality = nationality if nationality else footballer.nationality

    print("Cannot update shirt number because it's part of the primary key.\n")

    session.commit()
    print("Footballer updated.\n")

def delete_footballer(club):
    shirt_number = input("Enter shirt number of footballer to delete: ").strip()
    if not shirt_number.isdigit():
        print("Invalid shirt number.")
        return
    shirt_number = int(shirt_number)
    footballer = session.query(Footballer).filter_by(club_id=club.id, shirt_number=shirt_number).first()
    if not footballer:
        print("Footballer not found.")
        return
    confirm = input(f"Are you sure you want to delete {footballer.name}? (y/N): ").strip().lower()
    if confirm == 'y':
        session.delete(footballer)
        session.commit()
        print("Footballer deleted.\n")
    else:
        print("Delete cancelled.\n")

def list_clubs():
    clubs = session.query(Club).all()
    if not clubs:
        print("No clubs found.")
        return
    data = [[c.id, c.name, c.location or 'Unknown'] for c in clubs]
    headers = ["ID", "Name", "Location"]
    print_table(data, headers)

def add_club():
    name = input("Club Name: ").strip()
    location = input("Location: ").strip()
    club = Club(name=name, location=location)
    session.add(club)
    session.commit()
    print(f"Club '{name}' added.\n")

def add_former_club(club):
    shirt_number = input("Enter footballer shirt number: ").strip()
    if not shirt_number.isdigit():
        print("Invalid shirt number.")
        return
    shirt_number = int(shirt_number)
    footballer = session.query(Footballer).filter_by(club_id=club.id, shirt_number=shirt_number).first()
    if not footballer:
        print("Footballer not found.")
        return

    name = input("Former Club Name: ").strip()
    years_played = input("Years Played (e.g. 2015–2019): ").strip()

    former_club = FormerClub(
        name=name,
        years_played=years_played,
        footballer_club_id=club.id,
        footballer_shirt_number=shirt_number
    )
    session.add(former_club)
    session.commit()
    print(f"Added former club {name} for {footballer.name}.\n")

def list_seasons():
    seasons = session.query(Season).all()
    if not seasons:
        print("No seasons found.")
        return
    print("\n--- Seasons ---")
    for s in seasons:
        print(s.year)
    print()

def add_season():
    year = input("Enter new season (e.g. 2023/2024): ").strip()
    existing = session.query(Season).filter_by(year=year).first()
    if existing:
        print("Season already exists.")
        return
    season = Season(year=year)
    session.add(season)
    session.commit()
    print(f"Season '{year}' added.\n")

def add_season_stats(club):
    shirt_number = input("Enter footballer shirt number: ").strip()
    if not shirt_number.isdigit():
        print("Invalid shirt number.")
        return
    shirt_number = int(shirt_number)
    footballer = session.query(Footballer).filter_by(club_id=club.id, shirt_number=shirt_number).first()
    if not footballer:
        print("Footballer not found.")
        return

    list_seasons()
    season_year = input("Enter season year from above list: ").strip()
    season = session.query(Season).filter_by(year=season_year).first()
    if not season:
        print("Season not found.")
        return

    existing_stat = session.query(SeasonStat).filter_by(
        footballer_club_id=club.id,
        footballer_shirt_number=shirt_number,
        season_id=season.id
    ).first()

    if existing_stat:
        print("Season stats for this player and season already exist. Use update option.")
        return

    goals = input("Goals: ").strip()
    assists = input("Assists: ").strip()
    appearances = input("Appearances: ").strip()
    yellow_cards = input("Yellow Cards: ").strip()
    red_cards = input("Red Cards: ").strip()

    stat = SeasonStat(
        footballer_club_id=club.id,
        footballer_shirt_number=shirt_number,
        season_id=season.id,
        goals=int(goals) if goals.isdigit() else 0,
        assists=int(assists) if assists.isdigit() else 0,
        appearances=int(appearances) if appearances.isdigit() else 0,
        yellow_cards=int(yellow_cards) if yellow_cards.isdigit() else 0,
        red_cards=int(red_cards) if red_cards.isdigit() else 0
    )
    session.add(stat)
    session.commit()
    print("Season stats added.\n")

def update_season_stats(club):
    shirt_number = input("Enter footballer shirt number: ").strip()
    if not shirt_number.isdigit():
        print("Invalid shirt number.")
        return
    shirt_number = int(shirt_number)

    list_seasons()
    season_year = input("Enter season year from above list: ").strip()
    season = session.query(Season).filter_by(year=season_year).first()
    if not season:
        print("Season not found.")
        return

    stat = session.query(SeasonStat).filter_by(
        footballer_club_id=club.id,
        footballer_shirt_number=shirt_number,
        season_id=season.id
    ).first()

    if not stat:
        print("No stats found for this player and season.")
        return

    print(f"Updating stats for {stat.footballer.name} - Season {stat.season.year}")
    goals = input(f"Goals [{stat.goals}]: ").strip()
    assists = input(f"Assists [{stat.assists}]: ").strip()
    appearances = input(f"Appearances [{stat.appearances}]: ").strip()
    yellow_cards = input(f"Yellow Cards [{stat.yellow_cards}]: ").strip()
    red_cards = input(f"Red Cards [{stat.red_cards}]: ").strip()

    stat.goals = int(goals) if goals.isdigit() else stat.goals
    stat.assists = int(assists) if assists.isdigit() else stat.assists
    stat.appearances = int(appearances) if appearances.isdigit() else stat.appearances
    stat.yellow_cards = int(yellow_cards) if yellow_cards.isdigit() else stat.yellow_cards
    stat.red_cards = int(red_cards) if red_cards.isdigit() else stat.red_cards

    session.commit()
    print("Season stats updated.\n")

def delete_season_stats(club):
    shirt_number = input("Enter footballer shirt number: ").strip()
    if not shirt_number.isdigit():
        print("Invalid shirt number.")
        return
    shirt_number = int(shirt_number)

    list_seasons()
    season_year = input("Enter season year from above list: ").strip()
    season = session.query(Season).filter_by(year=season_year).first()
    if not season:
        print("Season not found.")
        return

    stat = session.query(SeasonStat).filter_by(
        footballer_club_id=club.id,
        footballer_shirt_number=shirt_number,
        season_id=season.id
    ).first()

    if not stat:
        print("No stats found for this player and season.")
        return

    confirm = input("Are you sure you want to delete these stats? (y/N): ").strip().lower()
    if confirm == 'y':
        session.delete(stat)
        session.commit()
        print("Season stats deleted.\n")
    else:
        print("Delete cancelled.\n")

def main_menu():
    while True:
        print("\n--- Football Club Manager ---")
        print("1. List Clubs")
        print("2. Add Club")
        print("3. Manage Club")
        print("4. Exit")
        choice = input("Choose option: ").strip()

        if choice == '1':
            list_clubs()
        elif choice == '2':
            add_club()
        elif choice == '3':
            club = select_club()
            if club:
                club_menu(club)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

def club_menu(club):
    while True:
        print(f"\n--- Managing {club.name} ---")
        print("1. List Footballers")
        print("2. Show Footballer Details")
        print("3. Add Footballer")
        print("4. Update Footballer")
        print("5. Delete Footballer")
        print("6. Add Former Club to Footballer")
        print("7. Add Season Stats")
        print("8. Update Season Stats")
        print("9. Delete Season Stats")
        print("10. Back to Main Menu")
        choice = input("Choose option: ").strip()

        if choice == '1':
            list_footballers(club)
        elif choice == '2':
            show_footballer_details(club)
        elif choice == '3':
            add_footballer(club)
        elif choice == '4':
            update_footballer(club)
        elif choice == '5':
            delete_footballer(club)
        elif choice == '6':
            add_former_club(club)
        elif choice == '7':
            add_season_stats(club)
        elif choice == '8':
            update_season_stats(club)
        elif choice == '9':
            delete_season_stats(club)
        elif choice == '10':
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()