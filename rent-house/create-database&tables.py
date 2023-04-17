import sqlite3


def createDatabase(dbFileName):
    conn = sqlite3.connect(dbFileName)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS USER(
    username TEXT NOT NULL PRIMARY KEY,
    password TEXT NOT NULL,
    fullname TEXT NOT NULL,
    email TEXT NOT NULL,
    sessionID INTEGER ,
    phone_number TEXT NOT NULL)""")

    c.execute("""CREATE TABLE IF NOT EXISTS CITY(
    cid INTEGER PRIMARY KEY ,
    cname TEXT NOT NULL)""")

    # Because of the [1:M] relationship, House table gets the primary key of the tables above.
    c.execute("""CREATE TABLE IF NOT EXISTS HOUSE(
    houseid INTEGER PRIMARY KEY AUTOINCREMENT,
    street TEXT NOT NULL,
    number_of_bedrooms INTEGER,
    monthly_fee INTEGER,
    username TEXT NOT NULL,
    cid INTEGER,
    FOREIGN KEY (username) REFERENCES USER(username),
    FOREIGN KEY (cid) REFERENCES CITY(cid))""")

    conn.commit()
    conn.close()


def insertRecords(dbFileName):
    conn = sqlite3.connect(dbFileName)
    c = conn.cursor()

    users = [("kutayural", "kutay123", "Ahmet Kutay URAL", "ahmetkutayural@gmail.com", -1, "+905389123844"),
             ("ardakskbs", "ar90da96", "Arda Kesikbas", "ardakskbs@gmail.com", -1, "+905338883940")]
    c.executemany("INSERT INTO USER VALUES (?,?,?,?,?,?)", users)

    cities = [(1, "LEFKOSA"),
              (2, "GIRNE"),
              (3, "GAZI MAGUSA"),
              (4, "ISKELE"),
              (5, "GUZELYURT"),
              (6, "LEFKE")]
    c.executemany("INSERT INTO CITY VALUES (?,?)", cities)

    homes = [(1, "kalkanli", 4, 900, "kutayural", 5),
             (2, "bellapais", 3, 1100, "ardakskbs", 2),
             (3, "karmi", 5, 2000, "kutayural", 2)]
    c.executemany("INSERT INTO HOUSE VALUES (?,?,?,?,?,?)", homes)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    dbFileName = "rent-house.db"
    createDatabase(dbFileName)
    insertRecords(dbFileName)
