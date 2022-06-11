from src.models.actor import Actor
from src.data import database_connection as dc
from collections import Counter, OrderedDict
import itertools
from datetime import datetime


def getNewestActor():
    dc.DB.commit()
    dc.CURSOR.execute('''SELECT max(ActorID) FROM ACTOR''')
    dc.DB.commit()
    return int(dc.CURSOR.fetchone()[0])


def createActor(newActor: Actor):
    dc.DB.commit()
    insert_actor_query = '''
        INSERT INTO ACTOR(Name, Birth_Name, Nickname, DOB, Origin, Height, Image, Bio) 
        VALUES(?, ?, ?, ?, ?, ?, ? ,?);'''

    actor_tuple = (newActor.name, newActor.birth_name, newActor.nick_name, newActor.dob,
                   newActor.origin, newActor.height, newActor.image, newActor.bio)

    dc.CURSOR.execute(insert_actor_query, actor_tuple)
    dc.DB.commit()
    return getNewestActor()


def getAllActors():
    dc.DB.commit()
    dc.CURSOR.execute('''
        SELECT * FROM `ACTOR`''')
    all_actors = dc.CURSOR.fetchall()
    dc.DB.commit()
    return all_actors


def getOneActorInfoById(actor_id: int):
    dc.DB.commit()
    select_actor_query = '''
        SELECT * FROM `ACTOR` WHERE ActorID = ?;'''
    dc.CURSOR.execute(select_actor_query, (actor_id,))
    actor_info = dc.CURSOR.fetchone()
    dc.DB.commit()
    return actor_info


def getOriginStats():
    dc.DB.commit()
    select_origins_query = '''SELECT Origin FROM ACTOR'''
    dc.CURSOR.execute(select_origins_query)
    dc.DB.commit()
    origins = dc.CURSOR.fetchall()
    origins = [origin[0].split(', ')[-1] for origin in origins]
    origins_count = dict(Counter(origins))

    origins_count = dict(sorted(origins_count.items(), key=lambda item: item[1], reverse=True))
    rs = {"Others": 0}
    for k, v in origins_count.items():
        if v > 2:
            rs[k] = v
        else:
            rs["Others"] += v
    return rs


def getAgeStats():
    dc.DB.commit()
    select_dobs_query = '''SELECT DOB FROM Actor'''
    dc.CURSOR.execute(select_dobs_query)
    dc.DB.commit()

    dob_list = dc.CURSOR.fetchall()
    age_list = [datetime.now().__getattribute__("year") - int(dob[0].split("-")[0]) for dob in dob_list]
    age_count = dict(Counter(age_list))
    age_count = OrderedDict(sorted(age_count.items()))

    rs = {"<50": 0, "50-60": 0, "60-70": 0, "70+": 0}

    for k, v in age_count.items():
        if k < 50:
            rs["<50"] += v
        elif 50 <= k < 60:
            rs["50-60"] += v
        elif 60 <= k < 70:
            rs["60-70"] += v
        else:
            rs["70+"] += v

    return rs