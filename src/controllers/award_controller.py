import src.data.database_connection as dc
from src.models.award import Award
from src.controllers import film_controller


def createAward(actorID: int, award: Award):
    filmID = film_controller.getFilmByNameAndYear(actorID, award.award_film_name, award.award_film_year)
    insert_award_query = '''INSERT INTO AWARD(ActorID, Category, Outcome, Title, FilmID, Year) 
    VALUES(?, ?, ?, ?, ?, ?)'''
    award_tuple = (actorID, award.category, award.outcome, award.title, filmID, award.year)
    dc.DB.commit()
    dc.CURSOR.execute(insert_award_query, award_tuple)
    dc.DB.commit()


def getAwardsListByActorID(actorID: int):
    # GET Categories List
    dc.DB.commit()
    select_categories_query = '''SELECT DISTINCT(Category) FROM AWARD a WHERE a.ActorID = ?'''
    dc.CURSOR.execute(select_categories_query, (actorID,))
    dc.DB.commit()
    categories = dc.CURSOR.fetchall()
    categories = [category[0] for category in categories]

    # GET Awards of each Category
    rs = {}
    dc.DB.commit()
    select_awards_query = '''SELECT Outcome, Title, Year FROM Award WHERE ActorID = ? AND Category = ?'''
    for category in categories:
        dc.CURSOR.execute(select_awards_query, (actorID, category))
        awards = dc.CURSOR.fetchall()
        rs[category] = awards
        dc.DB.commit()
    return rs


def getAwardsCountByActorID(actorID: int):
    dc.DB.commit()
    select_awards_count_query = '''SELECT count(*) FROM AWARD a WHERE a.ActorID = ?'''
    dc.DB.commit()
    dc.CURSOR.execute(select_awards_count_query, (actorID,))
    rs = dc.CURSOR.fetchone()[0]
    return rs


def getTotalAwardsCount():
    dc.DB.commit()
    select_awards_count_query = '''SELECT COUNT(*) FROM AWARD'''
    dc.CURSOR.execute(select_awards_count_query)
    dc.DB.commit()
    rs = dc.CURSOR.fetchone()[0]
    return rs
