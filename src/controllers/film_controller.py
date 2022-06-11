from src.models.film import Film
from src.data import database_connection as dc
from src.controllers import genre_controller


def getNewestFilm():
    dc.DB.commit()
    dc.CURSOR.execute('''SELECT max(FilmID) FROM FILM''')
    dc.DB.commit()
    return int(dc.CURSOR.fetchone()[0])


def createFilm(actorID: int, film: Film):
    # CREATE NEW FILM
    dc.DB.commit()
    insert_film_query = '''INSERT INTO FILM (ActorID, Title, Year, Rating)
    VALUES (?, ? ,?, ?)'''
    film_tuple = (actorID, film.title, film.year, film.rating)
    dc.CURSOR.execute(insert_film_query, film_tuple)
    dc.DB.commit()

    filmID = getNewestFilm()

    # CREATE FILM GENRE
    for genre in film.genres:
        genreID = genre_controller.createGenre(genre)
        genre_controller.createFilmGenre(filmID=filmID, genreID=genreID)

    return filmID


def getFilmByNameAndYear(actorID: int, name: str, year: str):
    dc.DB.commit()
    search_film_query = '''SELECT FilmID FROM FILM WHERE (ActorID = ?) AND (Title = ?) AND (Year = ?)'''
    film_tuple = (actorID, name, year)
    dc.CURSOR.execute(search_film_query, film_tuple)
    rs = dc.CURSOR.fetchone()
    if rs is None:
        return None
    else:
        return int(rs[0])


def getFilmsListByActorId(actorID: int):
    dc.DB.commit()
    get_film_query = '''SELECT f.`FilmID`, f.`ActorID`, f.`Title`, f.`Year`, f.`Rating`, 
                                GROUP_CONCAT(g.title, ', ')
                        FROM FILM f 
                        join FILM_GENRE fg on f.FilmID = fg.FilmID
                        join GENRE g on fg.GenreID = g.GenreID
                        WHERE f.ActorID = ?
                        GROUP BY f.`FilmID`, f.`ActorID`, f.`Title`, f.`Year`, f.`Rating`'''
    dc.CURSOR.execute(get_film_query, (actorID,))
    rs = dc.CURSOR.fetchall()
    return rs


def getFilmsCountByActorId(actorID: int):
    dc.DB.commit()
    get_film_count_query = '''SELECT count(*)
                            FROM FILM f 
                            WHERE f.ActorID = ?
                            '''
    dc.CURSOR.execute(get_film_count_query, (actorID,))
    rs = dc.CURSOR.fetchone()[0]
    return rs


def getTopFilmsListByActorId(actorID: int, top: int):
    dc.DB.commit()
    get_film_query = '''SELECT f.`FilmID`, f.`ActorID`, f.`Title`, f.`Year`, f.`Rating`, 
                                    GROUP_CONCAT(g.title, ', ')
                            FROM FILM f 
                            join FILM_GENRE fg on f.FilmID = fg.FilmID
                            join GENRE g on fg.GenreID = g.GenreID
                            WHERE f.ActorID = ?
                            GROUP BY f.`FilmID`, f.`ActorID`, f.`Title`, f.`Year`, f.`Rating`
                            ORDER BY f.Rating DESC LIMIT ?
                            '''
    dc.CURSOR.execute(get_film_query, (actorID, top))
    rs = dc.CURSOR.fetchall()
    return rs


def getAverageRatingByActorID(actorID: int):
    rs = {}
    dc.DB.commit()
    # overall rating
    get_overall_rating_query = '''SELECT ROUND(AVG(f.Rating), 2)
                                FROM FILM f
                                WHERE f.RATING > 0 AND f.ActorID = ?'''
    dc.CURSOR.execute(get_overall_rating_query, (actorID,))
    rs["All Time"] = dc.CURSOR.fetchone()[0]
    dc.DB.commit()
    # each year rating
    get_each_year_rating_query = '''SELECT f.Year, ROUND(AVG(f.Rating), 2)
                                    FROM FILM f
                                    WHERE f.RATING > 0 AND f.ActorID = ?
                                    GROUP BY f.Year'''
    dc.CURSOR.execute(get_each_year_rating_query, (actorID,))
    year_rating_list = dc.CURSOR.fetchall()
    for year_rating in year_rating_list:
        rs[str(year_rating[0])] = year_rating[1]
    return rs


def getTotalFilmsCount():
    dc.DB.commit()
    get_films_count = '''SELECT COUNT(DISTINCT(Title)) FROM Film'''
    dc.CURSOR.execute(get_films_count)
    rs = dc.CURSOR.fetchone()[0]
    dc.DB.commit()
    return rs




