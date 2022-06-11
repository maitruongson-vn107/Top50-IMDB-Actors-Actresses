from src.models.genre import Genre
from src.data import database_connection as dc


def findGenre(genre_title):
    dc.DB.commit()
    select_genre_query = """SELECT GenreID FROM GENRE WHERE Title=?"""
    dc.CURSOR.execute(select_genre_query, (genre_title,))
    rs = dc.CURSOR.fetchone()
    if rs is None:
        return None
    else:
        return int(rs[0])


def createGenre(genre_title):
    if findGenre(genre_title):
        return findGenre(genre_title)
    dc.DB.commit()
    insert_genre_query = """INSERT INTO GENRE(Title) VALUES (?)"""
    dc.CURSOR.execute(insert_genre_query, (genre_title,))
    dc.DB.commit()
    return findGenre(genre_title)


def createFilmGenre(filmID: int, genreID: int):
    dc.DB.commit()
    insert_film_genre_query = """INSERT INTO FILM_GENRE(FilmID, GenreID) VALUES(?, ?)"""
    dc.CURSOR.execute(insert_film_genre_query, (filmID, genreID))
    dc.DB.commit()


def getGenresByActorID(actorID: int):
    dc.DB.commit()
    get_actor_genre_query = """SELECT (g.Title) 
                                FROM GENRE g 
                                JOIN FILM_GENRE fg on g.GenreID = fg.GenreID
                                JOIN FILM f on fg.FilmID = f.FilmID
                                WHERE f.ActorID = ?
                                GROUP BY (g.Title) ORDER BY COUNT(*) DESC LIMIT 5"""
    dc.CURSOR.execute(get_actor_genre_query, (actorID,))
    dc.DB.commit()
    rs = dc.CURSOR.fetchall()
    rs = [item[0].strip() for item in rs]
    return rs