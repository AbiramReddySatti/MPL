import mysql.connector as sqlc
import time
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt


cxn1 = sqlc.connect(
    host="localhost",
    user="root",
    password="q1w2qw12",
)

cursor = cxn1.cursor()

# Check if the database exists before creating it
cursor.execute("SHOW DATABASES LIKE 'mpl';")
result = cursor.fetchone()

if result:
     print("Welcome to the 'MPL Experience'!\n")
else:
    sql_query = "CREATE DATABASE mpl;"
    cursor.execute(sql_query)
    cxn1.commit()
    print("Database 'mpl' created successfully.")


sql_query = "USE mpl;"
cursor.execute(sql_query)
cxn1.commit()

cursor.close()
cxn1.close()

# Database Connection 2
cxn = sqlc.connect(
    host="localhost",
    user="root",
    password="q1w2qw12",
    database = "MPL"
)
cursor = cxn.cursor()


global id_player

# Functions
def loading():
    """Simulates loading to enhance user experience."""
    print("\nLoading...\nKindly wait...\n")
    time.sleep(1)

def start_screen():
    """Displays the start screen and prompts user to continue."""
    print('''
     __       __  _______   __       
    /  \     /  |/       \ /  |      
    $$  \   /$$ |$$$$$$$  |$$ |      
    $$$  \ /$$$ |$$ |__$$ |$$ |      
    $$$$  /$$$$ |$$    $$/ $$ |      
    $$ $$ $$/$$ |$$$$$$$/  $$ |      
    $$ |$$$/ $$ |$$ |      $$ |_____ 
    $$ | $/  $$ |$$ |      $$       |
    $$/      $$/ $$/       $$$$$$$$/
    ''')
    
    loading()
    user_input = input("Do you wish to continue? (yes/no): ").lower()
    return user_input in {"yes", "y"}

def view_table(option):

    sql_query = "use mpl;"
    cursor.execute(sql_query)
    cxn.commit()
    
    """Displays the requested table from the database."""
    query_map = {
        "1": "SELECT Team, Team_Name, Team_Owner, Awards FROM Teams",
        "2": "SELECT Player_ID, Player_Name, Specialization FROM Players",
        "3": "SELECT Player_Name, Specialization FROM Players"
    }
    headers_map = {
        "1": ["Team", "Name", "Owner", "Awards"],
        "2": ["Player ID", "Player Name", "Specialization"],
        "3": ["Player Name", "Specialization"]
    }

    if option in query_map:
        loading()
        cursor.execute(query_map[option])
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=headers_map[option])
        print(tabulate(df, headers="keys", tablefmt="grid"))

    
def specific_view():
    
    """Prompts user to view specific details of a player."""
    view_table("2")  
    id_player = input("Enter the Player ID from the above list to view details: ")

  
    all_player_details = pd.DataFrame(
        columns=["Year", "Base Price", "Bid Price", "Sold Status", "Team", "Runs", "Wickets", "Injuries"]
    )

   
    query = f"""
        SELECT Player_Year, Base_Price, Bid_Price, Sold_Status, Team, Runs, Wickets, Injuries
        FROM mpl.player_rec
        WHERE Player_ID = '{id_player}';
    """
    
    cursor.execute(query)
    player_details = cursor.fetchall()  

    if player_details:  
       
        for i, row in enumerate(player_details):
            all_player_details.loc[i] = row

        
        print("Player Details:")
        print(tabulate(all_player_details, headers="keys", tablefmt="grid", showindex=False))
        
        #Algorithm
        query = f"""
        SELECT Players.Specialization, player_rec.Runs, player_rec.Wickets, player_rec.Injuries
        FROM player_rec
        INNER JOIN Players ON player_rec.Player_ID = Players.Player_ID
        WHERE Players.Player_ID = '{id_player}';
        """ 
    
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            specialization, runs, wickets, injuries = result
        
            # Calculate the score based on specialization
            if specialization == "Batsman":
                score = (3 * runs) + (1 * wickets) - injuries
            elif specialization == "Bowler":
                score = (1 * runs) + (3 * wickets) - injuries
            elif specialization in {"All-Rounder", "Wicket-Keeper"}:
                score = (2 * runs) + (2 * wickets) - injuries
            else:
                score = 0

            print(f"Player's Performance Score is: {score}")
        else:
            print(f"Player not found ")
            calculate_score()

    else:
        
        print(f"No details found for Player ID {id_player}. Please try again.")
        specific_view()
        


def update_player_statistics():

   player_id = input("Enter the Player ID to update: ").strip()
   year = int(input("Enter the Year (2022, 2023, 2024) to update the player's statistics: ").strip())
   if year not in [2022, 2023, 2024]:
        print("Invalid year. Please enter 2022, 2023, or 2024.")
   else:
        sql_query = """
        SELECT Runs, Wickets, Injuries
        FROM player_rec
        WHERE Player_ID = %s AND Player_Year = %s;
        """
        cursor.execute(sql_query, (player_id, year))
        result = cursor.fetchone()

        if not result:
            print(f"No record found for Player ID {player_id} in the year {year}.")
        else:
            current_runs, current_wickets, current_injuries = result
            print(f"Current Stats for Player ID {player_id} in {year}:")
            print(f"Runs: {current_runs}, Wickets: {current_wickets}, Injuries: {current_injuries}")

            runs = input(f"Enter new Runs (current: {current_runs}): ").strip()
            wickets = input(f"Enter new Wickets (current: {current_wickets}): ").strip()
            injuries = input(f"Enter new Injuries (current: {current_injuries}): ").strip()

            # Set default values if the user leaves the input blank
            runs = int(runs) if runs else current_runs
            wickets = int(wickets) if wickets else current_wickets
            injuries = int(injuries) if injuries else current_injuries

            # Proceed with the update query
            update_query = """
            UPDATE player_rec
            SET Runs = %s, Wickets = %s, Injuries = %s
            WHERE Player_ID = %s AND Player_Year = %s;
            """
            cursor.execute(update_query, (runs, wickets, injuries, player_id, year))
            cxn.commit()

            # Check if the update was successful
            if cursor.rowcount > 0:
                print(f"Statistics updated successfully for Player ID {player_id} in the year {year}.")
            else:
                print(f"No record found to update for Player ID {player_id} in the year {year}.")    

        
def compare_player_statistics_by_year():
    """Compares Runs, Wickets, and Injuries for a specific player across years using a bar graph."""
    
    # Get player ID input
    player_id = input("Enter the Player ID to compare statistics across years: ")


    query = f"""
        SELECT Player_Year, Runs, Wickets, Injuries
        FROM player_rec
        WHERE Player_ID = '{player_id}'
        ORDER BY Player_Year
    """  

    cursor.execute(query)
    players_data = cursor.fetchall()

    if not players_data:
        print(f"No data found for Player ID '{player_id}'.")
        return

    df = pd.DataFrame(players_data, columns=["Player_Year", "Runs", "Wickets", "Injuries"])   
    df.set_index("Player_Year").plot(kind='bar', figsize=(12, 8), width=0.8)
    plt.title(f'Statistics Comparison for Player ID: {player_id}')
    plt.ylabel('Statistics')
    plt.xlabel('Year')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Show the plot
    plt.show()
    
def compare_players_by_year():
    
    year = int(input("Enter the Year (2022, 2023, 2024) to update the player's statistics: "))
    
    query = f"""
        SELECT players.player_name, Runs, Wickets, Injuries
        FROM player_rec
        JOIN players ON player_rec.player_id = players.player_id
        WHERE player_rec.Player_Year = {year}
        ORDER BY players.player_name
    """
    
    cursor.execute(query)
    players_data = cursor.fetchall()
   
    
    # Creating DataFrame from the fetched data
    df = pd.DataFrame(players_data, columns=["Player_Name", "Runs", "Wickets", "Injuries"])

    # Plotting
    ax = df.set_index("Player_Name").plot(kind='bar', figsize=(10, 6), width=0.8)

    # Labeling and aesthetics
    ax.set_ylabel('Statistics')
    ax.set_title(f'Player Statistics of {year}: Runs, Wickets, Injuries')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

                  
def mysql_setup():
    ###Setting Up The Database

    sql_query = '''
    create table Teams(
        id int not null auto_increment,
        Team varchar(20),
        Team_Name varchar(40),
        Team_Owner varchar(40),
        Awards int,
        primary key(id),
        unique key(Team)
    );'''
    cursor.execute(sql_query)
    cxn.commit()

    sql_query = '''
    create table Players(
        id int not null auto_increment,
        Player_ID varchar(10),
        Player_Name varchar(20),
        Specialization varchar(20),
        primary key(id),
        unique key(Player_ID)
    );
    '''
    cursor.execute(sql_query)
    cxn.commit()

    sql_query = '''
    CREATE TABLE CareerDetails (
        id int not null auto_increment,
        Player_ID VARCHAR(100),
        Sold_Status VARCHAR(70),
        Runs INT,
        Wickets INT,
        Injuries INT,
        PRIMARY KEY(id),
        FOREIGN KEY(Player_ID) REFERENCES Players(Player_ID)

    );'''
    cursor.execute(sql_query)
    cxn.commit()

    sql_query = '''
    CREATE TABLE player_rec(
        id int not null auto_increment,
        Player_ID VARCHAR(100),
        Player_Year INT,
        Base_Price INT,
        Bid_Price INT,
        Sold_Status VARCHAR(70),
        Team VARCHAR(100),
        Runs INT,
        Wickets INT,
        Injuries INT,
        PRIMARY KEY(id),
        FOREIGN KEY(Player_ID) REFERENCES Players(Player_ID)
    );'''
    cursor.execute(sql_query)
    cxn.commit()
    
    ### Inserting into the "Teams" table...
    sql_query = '''
    insert into Teams(Team,Team_Name, Team_Owner, Awards) values
        ('KSK', 'Kolkata Super Kings', 'Vikram Vinod', '5'),
        ('SRK', 'Sunrisers Kanyakumari', 'Tasmeem Anasari', '2');'''
    cursor.execute(sql_query)
    cxn.commit()

    ### Inserting into the "Players" table...
    sql_query = '''
    insert into Players(Player_ID, Player_Name, Specialization) values
        ('P001', 'M.K Dhobi', 'All-rounder'),
        ('P002', 'Bhuvi Kumar', 'Bowler'),
        ('P003', 'Virajj Kholi', 'Batsman'),
        ('P004', 'Siru Mohammad', 'Bowler'),
        ('P005', 'Triple Boult', 'Bowler'),
        ('P006', 'Rishabh Kunt', 'Wicket-Keeper'),
        ('P007', 'Jofra Gunner', 'Bowler'),
        ('P008', 'M.S Kabhi', 'Batsman'),
        ('P009', 'Frank Livingstone', 'All-rounder'),
        ('P010', 'Ladis Zumpa', 'Bowler'),
        ('P011', 'Plad Comin', 'All-rounder'),
        ('P012', 'Shy Hopeless', 'Batsman'),
        ('P013', 'Peri Singh', 'Bowler'),
        ('P014', 'Sreekar Dhavan', 'Batsman'),
        ('P015', 'Mark Micheal', 'Bowler'),
        ('P016', 'Puff du Paner', 'All-rounder'),
        ('P017', 'Aigen Murkali', 'All-rounder'),
        ('P018', 'Kami Shaker', 'Batsman'),
        ('P019', 'Urvash Rathore', 'Bowler'),
        ('P020', 'Shrek Rao', 'All-rounder'),
        ('P021', 'Santosh Khaleel', 'Wicket-Keeper'),
        ('P022', 'Mukund Krome', 'Bowler');'''
    cursor.execute(sql_query)
    cxn.commit()

    ### Inserting into the values "PlayerDetails" table...
    sql_query = '''
    INSERT INTO CareerDetails(Player_ID, Sold_Status, Runs, Wickets, Injuries) VALUES
        ('P001', 'Sold', 2435, 3, 2),
        ('P002', 'Sold', 355, 90, 1),
        ('P003', 'Sold', 2285, 1, 1),
        ('P004', 'Sold', 1535, 48, 0),
        ('P005', 'Sold', 165, 67, 2),
        ('P006', 'Sold', 1830, 1, 0),
        ('P007', 'Sold', 98, 54, 1),
        ('P008', 'Sold', 1230, 33, 1),
        ('P009', 'Sold', 2115, 3, 2),
        ('P010', 'Sold', 63, 47, 0),
        ('P011', 'Sold', 113, 60, 0),
        ('P012', 'Sold', 2580, 1, 1),
        ('P013', 'Sold', 315, 78, 1),
        ('P014', 'Sold', 1365, 39, 1),
        ('P015', 'Sold', 1855, 1, 0),
        ('P016', 'Sold', 233, 37, 2),
        ('P017', 'Sold', 1535, 54, 1),
        ('P018', 'Sold', 142, 53, 1),
        ('P019', 'Sold', 1680, 3, 1),
        ('P020', 'Sold', 1230, 37, 2),
        ('P021', 'Sold', 1080, 24, 1),
        ('P022', 'Sold', 1530, 45, 1);'''
    cursor.execute(sql_query)
    cxn.commit()

    sql_query = '''
    INSERT INTO player_rec(Player_ID, Player_Year, Base_Price, Bid_Price, Sold_Status, Team, Runs, Wickets, Injuries) VALUES
        ('P001', '2022', 750000, 41250000, 'Sold', 'KSK', 800, 0, 1),
        ('P001', '2023', 750000, 85000000, 'Sold', 'SRK', 820, 2, 0),
        ('P001', '2024', 4000000, 30000000, 'Sold', 'SRK', 815, 1, 1),
        ('P002', '2022', 1000000, 37500000, 'Sold', 'SRK', 100, 30, 0),
        ('P002', '2023', 1000000, 90000000, 'Sold', 'KSK', 120, 32, 0),
        ('P002', '2024', 1300000, 37500000, 'Sold', 'SRK', 115, 28, 1),
        ('P003', '2022', 750000, 45000000, 'Sold', 'SRK', 750, 0, 0),
        ('P003', '2023', 750000, 82000000, 'Sold', 'KSK', 770, 0, 0),
        ('P003', '2024', 1000000, 45000000, 'Sold', 'SRK', 765, 1, 1),
        ('P004', '2022', 1500000, 25000000, 'Sold', 'KSK', 500, 15, 0),
        ('P004', '2023', 1500000, 51000000, 'Sold', 'SRK', 525, 17, 0),
        ('P004', '2024', 2500000, 25000000, 'Sold', 'KSK', 510, 16, 0),
        ('P005', '2022', 500000, 18750000, 'Sold', 'SRK', 50, 25, 1),
        ('P005', '2023', 500000, 51000000, 'Sold', 'KSK', 60, 22, 0),
        ('P005', '2024', 600000, 18750000, 'Sold', 'SRK', 55, 20, 1),
        ('P006', '2022', 750000, 48750000, 'Sold', 'SRK', 600, 0, 0),
        ('P006', '2023', 750000, 91000000, 'Sold', 'SRK', 620, 1, 0),
        ('P006', '2024', 1100000, 48750000, 'Sold', 'KSK', 610, 0, 0),
        ('P007', '2022', 1000000, 32500000, 'Sold', 'KSK', 30, 20, 0),
        ('P007', '2023', 1000000, 91000000, 'Sold', 'KSK', 35, 18, 1),
        ('P007', '2024', 1500000, 32500000, 'Sold', 'KSK', 33, 16, 0),
        ('P008', '2022', 1000000, 37500000, 'Sold', 'KSK', 400, 10, 0),
        ('P008', '2023', 1000000, 82000000, 'Sold', 'SRK', 420, 12, 1),
        ('P008', '2024', 1300000, 37500000, 'Sold', 'SRK', 410, 11, 0),
        ('P009', '2022', 500000, 25000000, 'Sold', 'SRK', 700, 0, 1),
        ('P009', '2023', 500000, 82000000, 'Sold', 'KSK', 710, 2, 0),
        ('P009', '2024', 600000, 25000000, 'Sold', 'SRK', 705, 1, 1),
        ('P010', '2022', 1000000, 31250000, 'Sold', 'KSK', 20, 18, 0),
        ('P010', '2023', 1000000, 61000000, 'Sold', 'KSK', 22, 15, 0),
        ('P010', '2024', 1300000, 31250000, 'Sold', 'SRK', 21, 14, 0),
        ('P011', '2022', 1000000, 35000000, 'Sold', 'KSK', 35, 22, 0),
        ('P011', '2023', 1000000, 61000000, 'Sold', 'SRK', 40, 20, 0),
        ('P011', '2024', 1300000, 35000000, 'Sold', 'KSK', 38, 18, 0),
        ('P012', '2022', 1000000, 40000000, 'Sold', 'SRK', 850, 0, 0),
        ('P012', '2023', 1000000, 75000000, 'Sold', 'SRK', 870, 1, 0),
        ('P012', '2024', 1300000, 40000000, 'Sold', 'KSK', 860, 0, 1),
        ('P013', '2022', 750000, 35000000, 'Sold', 'SRK', 100, 28, 0),
        ('P013', '2023', 750000, 71000000, 'Sold', 'KSK', 110, 26, 0),
        ('P013', '2024', 1000000, 35000000, 'Sold', 'SRK', 105, 24, 1),
        ('P014', '2022', 1000000, 45000000, 'Sold', 'KSK', 450, 12, 0),
        ('P014', '2023', 1000000, 82000000, 'Sold', 'SRK', 460, 14, 1),
        ('P014', '2024', 1300000, 45000000, 'Sold', 'KSK', 455, 13, 0),
        ('P015', '2022', 500000, 30000000, 'Sold', 'SRK', 600, 0, 0),
        ('P015', '2023', 500000, 62000000, 'Sold', 'SRK', 620, 1, 0),
        ('P015', '2024', 600000, 30000000, 'Sold', 'SRK', 615, 0, 0),
        ('P016', '2022', 750000, 32500000, 'Sold', 'SRK', 70, 15, 1),
        ('P016', '2023', 750000, 67000000, 'Sold', 'KSK', 85, 12, 0),
        ('P016', '2024', 1000000, 32500000, 'Sold', 'SRK', 78, 10, 1),
        ('P017', '2022', 1000000, 47500000, 'Sold', 'KSK', 500, 18, 0),
        ('P017', '2023', 1000000, 91000000, 'Sold', 'SRK', 520, 20, 1),
        ('P017', '2024', 1300000, 47500000, 'Sold', 'KSK', 515, 16, 0),
        ('P018', '2022', 1000000, 37500000, 'Sold', 'KSK', 45, 20, 0),
        ('P018', '2023', 1000000, 75000000, 'Sold', 'SRK', 50, 18, 0),
        ('P018', '2024', 1300000, 37500000, 'Sold', 'KSK', 47, 15, 1),
        ('P019', '2022', 500000, 30000000, 'Sold', 'SRK', 550, 0, 0),
        ('P019', '2023', 500000, 62000000, 'Sold', 'SRK', 570, 2, 1),
        ('P019', '2024', 600000, 30000000, 'Sold', 'KSK', 560, 1, 0),
        ('P020', '2022', 1500000, 45000000, 'Sold', 'SRK', 400, 14, 1),
        ('P020', '2023', 1500000, 82000000, 'Sold', 'KSK', 420, 12, 0),
        ('P020', '2024', 2500000, 45000000, 'Sold', 'SRK', 410, 11, 1),
        ('P021', '2022', 1000000, 35000000, 'Sold', 'KSK', 350, 10, 0),
        ('P021', '2023', 1000000, 71000000, 'Sold', 'SRK', 370, 8, 1),
        ('P021', '2024', 1300000, 35000000, 'Sold', 'KSK', 360, 6, 0),
        ('P022', '2022', 1000000, 37500000, 'Sold', 'KSK', 500, 15, 0),
        ('P022', '2023', 1000000, 75000000, 'Sold', 'SRK', 520, 18, 1),
        ('P022', '2024', 1300000, 37500000, 'Sold', 'KSK', 510, 12, 0);
        '''
    cursor.execute(sql_query)
    cxn.commit()
    

    print("The Database Has Been  Downloaded Into Your System")
      
def main():
    """Main driver function."""
    if not start_screen():
        print("Thank you for visiting! Goodbye!")
        return

    while True:
        print("\nOptions:")
        print("1 - Database Setup")
        print("2 - View Team Roster")
        print("3 - View Players List")
        print("4 - View Specializations")
        print("5 - View Player Statistics")
        print("6 - Update Player Scores")
        print("7 - Visualize Player Statistics")
        print("8 - Compare Players Performace year wise")
        print("9 - Exit")

        choice = input("Enter your choice: ")
        
        
        if choice == "1":
            inp2 = input("Do You Want To Install The Database: ").lower()  
            if inp2 == 'yes' or inp2 == 'y': 
                mysql_setup()
            else:
                start_screen()
        elif choice == "2":
            view_table("1")
        elif choice == "3":
            view_table("2")
        elif choice == "4":
            view_table("3")
        elif choice == "5":
            specific_view()
        elif choice == "6":
            update_player_statistics()
        elif choice == "7":
            compare_player_statistics_by_year()
        elif choice == "8":
            compare_players_by_year()
        else:
            print("Thank you for using MPL Experience. Goodbye!")
            break

        
main()
cursor.close()
cxn.close()
    
