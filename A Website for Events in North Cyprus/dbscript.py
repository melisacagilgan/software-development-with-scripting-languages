import sqlite3


# Create database
def init_db(db_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS USER (username TEXT PRIMARY KEY, firstname TEXT, lastname TEXT, password TEXT, email TEXT)""")

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS CITY (cityid INTEGER PRIMARY KEY AUTOINCREMENT, cityname TEXT)""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS EVENT (eventid INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, price REAL, date TEXT, time TEXT, isActive BOOLEAN, location TEXT, cityid INTEGER, username TEXT, FOREIGN KEY(cityid) REFERENCES CITY(cityid), FOREIGN KEY(username) REFERENCES USER(username))""")

    connection.commit()
    connection.close()


# Connect to the database
def connect_db(db_name="events.db"):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    return connection, cursor


# Insert event records
def insert_event(name, description, price, date, time, location, cityid, username):
    connection, cursor = connect_db()
    cursor.execute("INSERT INTO EVENT(name, description, price, date, time, isActive, location, cityid, username) VALUES (?,?,?,?,?,?,?,?,?)",
                   (name, description, price, date, time, True, location, cityid, username))
    connection.commit()
    connection.close()


# Insert user records
def insert_user(username, firstname, lastname, password, email):
    connection, cursor = connect_db()
    cursor.execute("INSERT INTO USER VALUES (?,?,?,?,?)",
                   (username, firstname, lastname, password, email))
    connection.commit()
    connection.close()


# Insert city records
def insert_city(cityname):
    connection, cursor = connect_db()
    cursor.execute("INSERT INTO CITY(cityname) VALUES (?)", (cityname,))
    connection.commit()
    connection.close()


# Deactivate event by eventid
def deactivate_event(eventid):
    connection, cursor = connect_db()
    cursor.execute(
        "UPDATE EVENT SET isActive = ? WHERE eventid = ?", (False, eventid))
    connection.commit()
    connection.close()


# Get all events from database
def get_events():
    connection, cursor = connect_db()
    events = cursor.execute(
        "SELECT * FROM EVENT WHERE isActive=?", (True,)).fetchall()
    connection.close()
    return events


# Get all events by userid from database
def get_events_by_username(username):
    connection, cursor = connect_db()
    try:
        events = cursor.execute(
            "SELECT * FROM EVENT WHERE username=? and isActive=?", (username, True)).fetchall()
    except:
        events = []
    connection.close()
    return events


# Get event by eventid from database
def get_event_by_eventid(eventid):
    connection, cursor = connect_db()
    event = cursor.execute(
        "SELECT * FROM EVENT WHERE eventid=? and isActive=?", (eventid, True)).fetchall()
    connection.close()
    return event


# Get all events by keyword from database
def get_events_by_keyword(keyword):
    connection, cursor = connect_db()

    city_events = get_city_events()
    kw_events = cursor.execute(
        "SELECT * FROM EVENT WHERE name LIKE ? OR description LIKE ? OR location LIKE ? and isActive=? ORDER BY eventid DESC", (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", True)).fetchall()

    city_dict = {}
    for cityname, events in city_events.items():
        city_dict[cityname] = []
        for event in events:
            if event in kw_events:
                city_dict[cityname].append(event)
    connection.close()
    return city_dict


# Get all events by cityids from database and return them up to 5
def get_city_events():
    connection, cursor = connect_db()
    cities = cursor.execute("SELECT * FROM CITY").fetchall()

    city_events = {}
    for cityid, cityname in cities:
        events = cursor.execute(
            "SELECT * FROM EVENT WHERE isActive=? and cityid=? ORDER BY eventid DESC", (True, cityid)).fetchall()
        if len(events) > 5:
            city_events[cityname] = events[:5]
        else:
            city_events[cityname] = events

    connection.close()
    return city_events


# Get all users from database
def get_users():
    connection, cursor = connect_db()
    users = cursor.execute("SELECT * FROM USER").fetchall()
    connection.close()
    return users


# Get user by username from database
def get_usernames():
    connection, cursor = connect_db()
    usernames = []
    for username in cursor.execute("SELECT username FROM USER").fetchall():
        usernames.append(username[0])
    connection.close()
    return usernames


# Get cityname by cityid from database
def get_cityname_by_cityid(cityid):
    connection, cursor = connect_db()
    cityname = cursor.execute(
        "SELECT cityname FROM CITY WHERE cityid=?", (cityid,)).fetchone()[0]
    connection.close()
    return cityname


# Get cityid by cityname from database
def get_cityid_by_cityname(cityname):
    connection, cursor = connect_db()
    cityid = cursor.execute(
        "SELECT cityid FROM CITY WHERE cityname=?", (cityname,)).fetchone()[0]
    connection.close()
    return cityid


# Get all city names from database
def get_citynames():
    connection, cursor = connect_db()
    citynames = []
    for cityname in cursor.execute("SELECT cityname FROM CITY").fetchall():
        citynames.append(cityname[0])
    connection.close()
    return citynames


# Insert mock cities mentioned in the assignment
def insert_mock_cities():
    city_list = [("Lefkosa",), ("Girne",), ("Guzelyurt",),
                 ("Gazi Magusa",), ("Lefke",), ("Iskele",)]
    for city in city_list:
        insert_city(city[0])


# Insert mock data
def insert_mock_data():
    # Insert mock users
    insert_user("doge", "dogukan", "baysal", "123", "abc")
    insert_user("mel", "melisa", "cagilgan", "123", "abc")

    # Insert mock cities
    insert_mock_cities()

    # Insert mock events
    insert_event("event1-1", "description1", 10, "2021-01-01",
                 "10:00", "location1", 1, "mel")
    insert_event("event1-2", "description1", 10, "2021-01-01",
                 "10:00", "location1", 1, "doge")
    insert_event("event1-3", "description1", 10, "2021-01-01",
                 "10:00", "location1", 1, "mel")
    insert_event("event1-4", "description1", 10, "2021-01-01",
                 "10:00", "location1", 1, "mel")
    insert_event("event1-5", "description1", 10, "2021-01-01",
                 "10:00", "location1", 1, "mel")
    insert_event("event1-6", "description1", 10, "2021-01-01",
                 "10:00", "location1", 1, "mel")
    insert_event("combined-key-1", "description-event1", 10, "2021-01-01",
                 "10:00", "location1", 1, "mel")
    insert_event("combined-key-2", "description1", 10, "2021-01-01",
                 "10:00", "location-event1", 1, "mel")
    insert_event("event2", "description2", 20, "2021-01-02",
                 "11:00", "location2", 2, "mel")
    insert_event("event3", "description3", 30, "2021-01-03",
                 "12:00", "location3", 3, "mel")
    insert_event("event4", "description4", 40, "2021-01-04",
                 "13:00", "location4", 4, "mel")
    insert_event("event5", "description5", 50, "2021-01-05",
                 "14:00", "location5", 5, "mel")
    insert_event("event6", "description6", 60, "2021-01-06",
                 "15:00", "location6", 6, "mel")


if __name__ == "__main__":
    try:
        init_db("events.db")
        insert_mock_data()
    except:
        print("Database already exists.")
