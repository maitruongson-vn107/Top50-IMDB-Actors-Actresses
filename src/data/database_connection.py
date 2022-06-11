import sqlite3

DATABASE_URL = '/Users/sonmt/OTH/OTH_COURSES/AppliedDS/Projects/imdb_prj/src/data/imdb_top_50.db'
DB = sqlite3.connect(DATABASE_URL)  # Creates or opens a file called Actor_database with a SQLite3 DB
CURSOR = DB.cursor()  # Get a cursor object


def drop_tables():
    DB.commit()

    CURSOR.execute('''
            DROP TABLE IF EXISTS `ACTOR`;
        ''')
    CURSOR.execute('''
                DROP TABLE IF EXISTS `FILM`;
            ''')
    CURSOR.execute('''
                DROP TABLE IF EXISTS `AWARD`;
            ''')
    CURSOR.execute('''
                DROP TABLE IF EXISTS `GENRE`;
            ''')
    CURSOR.execute('''
                DROP TABLE IF EXISTS `FILM_GENRE`;
            ''')
    DB.commit()


def create_tables():
    CURSOR.execute('''PRAGMA foreign_keys = 1''')
    DB.commit()

    CURSOR.execute('''
        CREATE TABLE IF NOT EXISTS ACTOR (
            ActorID     INTEGER PRIMARY KEY AUTOINCREMENT,
            Name        VARCHAR(50),
            Birth_Name  VARCHAR(100),
            Nickname    VARCHAR(50),
            DOB         DATE,
            Origin      VARCHAR(50),
            Height      VARCHAR(20),
            Image	    VARCHAR,
            Bio         VARCHAR
        ) ''')
    DB.commit()

    CURSOR.execute('''
        CREATE TABLE IF NOT EXISTS FILM
            (
            FilmID      INTEGER PRIMARY KEY AUTOINCREMENT,
            ActorID     INTEGER,
            Title	    TEXT,
            Year	    INTEGER,
            Rating	    FLOAT,
            FOREIGN KEY(ActorID) REFERENCES Actor(`ActorID`) ON UPDATE CASCADE ON DELETE SET NULL
            )
            ''')
    DB.commit()

    CURSOR.execute('''
        CREATE TABLE IF NOT EXISTS GENRE
            (
            GenreID INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT
            )
            ''')
    DB.commit()

    CURSOR.execute('''
        CREATE TABLE IF NOT EXISTS FILM_GENRE
            (
            'FilmID'    INTEGER,
            'GenreID'   INTEGER,
            FOREIGN KEY(`FilmID`) REFERENCES `FILM`(`FilmID`) ON DELETE CASCADE,
            FOREIGN KEY(`GenreID`) REFERENCES `GENRE`(`GenreID`) ON DELETE CASCADE
            )
            ''')
    DB.commit()

    CURSOR.execute('''
        CREATE TABLE IF NOT EXISTS AWARD
            (
            ActorID	    INTEGER,
            Category	TEXT,
            Outcome     TEXT,
            Title       TEXT,
            FilmID      INTEGER,
            Year	    INTEGER,
            FOREIGN KEY(`ActorID`) REFERENCES `ACTOR`(`ActorID`) ON UPDATE CASCADE ON DELETE SET NULL,
            FOREIGN KEY(`FilmID`) REFERENCES `FILM`(`FilmID`) ON UPDATE CASCADE ON DELETE SET NULL
            )
            ''')
    DB.commit()


def reset_data():
    drop_tables()
    create_tables()
    print("Reset Database")
