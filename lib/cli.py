from lib import session
from lib.models import Club, Footballer, FormerClub

def list_footballers():
    print("\n--- Footballers (Name & Shirt Number) ---")
    footballers = session.query(Footballer).all()
    for f in footballers:
        print(f"{f.name} - Shirt Number: {f.shirt_number if f.shirt_number else 'N/A'}")
    print()

def show_footballer_details():
    shirt_num = input("Enter footballer shirt number: ").strip()
    footballer = session.query(Footballer).filter(Footballer.shirt_number == shirt_num).first()
    if footballer:
        print(f"\nDetails for {footballer.name}:")
        print(f"Shirt Number: {footballer.shirt_number}")
        print(f"Age: {footballer.age}")
        print(f"Position: {footballer.position}")
        print(f"Nationality: {footballer.nationality}")
        print(f"Current Club: {footballer.club.name if footballer.club else 'None'}")
        if footballer.former_clubs:
            print("Former Clubs:")
            for fc in footballer.former_clubs:
                print(f" - {fc.name} ({fc.years_played})")
        else:
            print("No former clubs on record.")
    else:
        print("Footballer not found.")
    print()

def add_footballer():
    club = session.query(Club).first()
    if not club:
        print("No club found in the database. Please seed your club first.")
        return
    name = input("Name: ").strip()
    age = int(input("Age: ").strip())
    position = input("Position: ").strip()
    nationality = input("Nationality: ").strip()
    shirt_number = input("Shirt Number: ").strip()
    footballer = Footballer(name=name, age=age, position=position, nationality=nationality, shirt_number=shirt_number, club=club)
    session.add(footballer)
    session.commit()
    print(f"{name} added to {club.name}.\n")

def update_footballer():
    shirt_num = input("Enter footballer shirt number to update: ").strip()
    footballer = session.query(Footballer).filter(Footballer.shirt_number == shirt_num).first()
    if footballer:
        print(f"Updating {footballer.name}:")
        footballer.age = int(input(f"New Age [{footballer.age}]: ") or footballer.age)
        footballer.position = input(f"New Position [{footballer.position}]: ") or footballer.position
        footballer.nationality = input(f"New Nationality [{footballer.nationality}]: ") or footballer.nationality
        footballer.shirt_number = input(f"New Shirt Number [{footballer.shirt_number}]: ") or footballer.shirt_number
        session.commit()
        print("Footballer updated.\n")
    else:
        print("Footballer not found.\n")

def delete_footballer():
    shirt_num = input("Enter footballer shirt number to delete: ").strip()
    footballer = session.query(Footballer).filter(Footballer.shirt_number == shirt_num).first()
    if footballer:
        session.delete(footballer)
        session.commit()
        print(f"Footballer {footballer.name} deleted.\n")
    else:
        print("Footballer not found.\n")

def list_former_clubs():
    print("\n--- Former Clubs ---")
    former_clubs = session.query(FormerClub).all()
    for fc in former_clubs:
        print(f"{fc.name} ({fc.years_played}) - Player: {fc.footballer.name}")
    print()

def add_former_club():
    shirt_num = input("Enter footballer shirt number for former club: ").strip()
    footballer = session.query(Footballer).filter(Footballer.shirt_number == shirt_num).first()
    if not footballer:
        print("Footballer not found.\n")
        return
    name = input("Former Club Name: ").strip()
    years_played = input("Years Played (e.g. 2015–2019): ").strip()
    former_club = FormerClub(name=name, years_played=years_played, footballer=footballer)
    session.add(former_club)
    session.commit()
    print(f"Added former club {name} for {footballer.name}.\n")

def main_menu():
    while True:
        print("""--- Football Club CLI ---
1. List all footballers
2. Show footballer details (by shirt number)
3. Add a new footballer
4. Update footballer
5. Delete footballer
6. List all former clubs
7. Add former club to a footballer
8. Exit
""")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            list_footballers()
        elif choice == '2':
            show_footballer_details()
        elif choice == '3':
            add_footballer()
        elif choice == '4':
            update_footballer()
        elif choice == '5':
            delete_footballer()
        elif choice == '6':
            list_former_clubs()
        elif choice == '7':
            add_former_club()
        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.\n")

if __name__ == "__main__":
    main_menu()