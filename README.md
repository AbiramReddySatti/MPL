
# 🏏 MPL Experience

Welcome to the **MPL Experience**, a Python-based cricket player management and analysis system that interacts with a MySQL database. This application allows you to create, populate, view, and manipulate player and team data, including dynamic visualizations.

---

## 📦 Features

* ✅ **Database Initialization** with player, team, and performance data
* 🔍 **View** Teams, Players, and Specializations
* 📊 **Analyze Player Performance** over the years
* ✏️ **Update Player Stats** directly from CLI
* 📈 **Visual Comparisons** of player performance across years
* 🧠 **Performance Scoring Algorithm** based on specialization

---

## ⚙️ Requirements

* Python 3.7+
* MySQL Server (running locally)
* Python Packages:

  * `mysql-connector-python`
  * `pandas`
  * `tabulate`
  * `matplotlib`

Install dependencies with:

```bash
pip install mysql-connector-python pandas tabulate matplotlib
```

---

## 🛠️ Setup

1. Ensure MySQL is running on `localhost` with:

   * **Username**: `root`
   * **Password**: `q1w2qw12`
     *(You can modify these in the code if needed)*

2. Run the script:

```bash
python mpl_experience.py
```

3. When prompted:

   * Select `yes` to continue.
   * Choose option `1` to install the database and seed it with initial data.

---

## 🧭 Menu Options

| Option | Description                                                        |
| ------ | ------------------------------------------------------------------ |
| `1`    | Setup the database schema and populate it                          |
| `2`    | View the list of teams                                             |
| `3`    | View all players                                                   |
| `4`    | View player specializations                                        |
| `5`    | View detailed player statistics and calculate performance score    |
| `6`    | Update player scores (Runs, Wickets, Injuries) for a specific year |
| `7`    | Visualize performance (bar graph) of a player across years         |
| `8`    | Compare multiple players for a specific year                       |
| `9`    | Exit the program                                                   |

---

## 🧠 Performance Score Formula

The player's performance score is calculated based on their specialization:

* **Batsman**: `Score = 3×Runs + 1×Wickets - Injuries`
* **Bowler**: `Score = 1×Runs + 3×Wickets - Injuries`
* **All-Rounder / Wicket-Keeper**: `Score = 2×Runs + 2×Wickets - Injuries`

---

## 🧪 Example Data

* Teams like *Kolkata Super Kings*, *Sunrisers Kanyakumari*
* Players like *M.K Dhobi*, *Virajj Kholi*, *Bhuvi Kumar*, etc.
* Stats across **2022**, **2023**, and **2024**

---

## 🚨 Important Notes

* The script connects to MySQL twice:

  * First, to create the `mpl` database (if not already present)
  * Second, to work with the `mpl` schema for all operations
* Tables created: `Teams`, `Players`, `CareerDetails`, and `player_rec`
* Make sure the MySQL user has sufficient privileges to create databases and tables

---

## 📸 Visual Output

All visualizations (bar charts) use `matplotlib` and will pop up in a separate window.

---

## 📃 License

This project is open-source and free to use under the [MIT License](https://opensource.org/licenses/MIT).

---

