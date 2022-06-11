import requests as rq
from bs4 import BeautifulSoup, SoupStrainer
import re
import datetime

from src.controllers import film_controller, award_controller
from src.data import database_connection as dc
from src.models.actor import Actor
from src.controllers import actor_controller
from src.models.award import Award
from src.models.film import Film

BASEURL = "http://www.imdb.com"
ACTOR_LIST_URL = "/list/ls053501318/"
BIO_ENDPOINT = "bio"
AWARDS_ENDPOINT = "awards"
months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8,
          'September': 9, 'October': 10, 'November': 11, 'December': 12}


# CRAWL THE MAIN PAGE
def crawlMainPage():
    '''
    Using BeautifulSoup to scrap data from IMDb Top-50 page
    Crawl Main List -> Actor Biography Page, Actor's Filmography, Actor's Awards
    Save Data to SQLite file
    :return:
    '''
    print("Begin Crawling: ", datetime.datetime.now().time())
    rqMainList = rq.get(BASEURL + ACTOR_LIST_URL)  # request the website
    soup = BeautifulSoup(rqMainList.text, 'lxml')

    # Get list with all actors
    all_actors = soup.find('div', {'class': "lister list detail sub-list"})

    # Get div with all images
    all_actors_images = all_actors.findAll('div', {'class': 'lister-item-image'})

    for actor_image in all_actors_images:
        # Get all 'a' links starting with '/name/'
        actor_image_link_container = actor_image.findAll("a", href=re.compile('^/name/'))
        for each_actor_image_link in actor_image_link_container:
            my_actor_image_link = each_actor_image_link['href']
            if my_actor_image_link:
                # STEP ONE - GET INFORMATION ABOUT ACTOR
                actor_id, actor_name = crawlActor(link_to_profile=my_actor_image_link)

                print("**ACTOR: " + actor_name + "**")

                # STEP TWO - GET ALL FILMS OF ACTOR
                crawlActorFilms(link_to_profile=my_actor_image_link, actorID=actor_id)

                # STEP THREE - GET ALL AWARDS OF ACTOR
                crawlActorAwards(link_to_profile=my_actor_image_link, actorID=actor_id)

    print("End Crawling: ", datetime.datetime.now().time())


def crawlActor(link_to_profile):
    """
    Get each actor's personal information
    :param link_to_profile: link to actor's profile page
    :return:
    """
    # Request to profile page
    headers = {"Accept-Language": "en-US,en;q=0.5"}
    params = dict(lang='en-US,en;q=0.5')
    actor_info_page = rq.get(BASEURL + link_to_profile + BIO_ENDPOINT, headers=headers, params=params)
    parse_only = SoupStrainer('div', {'class': 'article listo'})
    actor_soup = BeautifulSoup(actor_info_page.text, 'lxml', parse_only=parse_only)

    # Get actor's image link
    img_container = actor_soup.find("img", {"class": "poster"})
    actor_image_link = img_container['src']

    # Get actor's name
    actor_name = ""
    anchor_tag_list = actor_soup.find_all('a', href=True)
    for anchor_tag in anchor_tag_list:
        href = anchor_tag['href']
        if re.match('^' + link_to_profile, href) and len(anchor_tag.text.strip()) > 0:
            actor_name = anchor_tag.text

    # Get actor's Birth name, DOB, Origin, Height
    actor_birth_name = ""
    actor_nick_name = ""
    actor_dob = ""
    actor_origin = ""
    actor_height = ""
    overview_table = actor_soup.find("table", id="overviewTable")
    if overview_table is not None:
        table_rows = overview_table.find_all('tr')
        for row in table_rows:
            row_data = row.find_all('td')
            if row_data[0].text == "Birth Name":
                actor_birth_name = row_data[1].text
            elif row_data[0].text == "Nickname":
                actor_nick_name = row_data[1].text.strip()
            elif row_data[0].text == "Height":
                actor_height = row_data[1].text

        overview = overview_table.find_all('a')
        if overview is not None:
            actor_origin = str(overview[2].text)
            actor_birth_day = int(overview[0].text.split(" ")[1])
            actor_birth_month = months[overview[0].text.split(" ")[0]]
            actor_birth_year = int(overview[1].text)
            actor_dob = datetime.date(year=actor_birth_year, month=actor_birth_month, day=actor_birth_day)

            # actor_dob = "/".join([actor_birth_day, actor_birth_month, actor_birth_year])

    # Get actor's Biography
    actor_bio = ""
    biography_container = actor_soup.find('div', {'class': 'soda odd'})
    if biography_container is not None:
        all_bio_paragraphs = biography_container.findAll('p')
        if all_bio_paragraphs[0] is not None:
            actor_bio = removeHTMLTags(str(all_bio_paragraphs[0]), 'br', 'a')

    new_actor = Actor(actorID=None, name=actor_name, birth_name=actor_birth_name,
                      nick_name=actor_nick_name, dob=actor_dob, height=actor_height,
                      image=actor_image_link, origin=actor_origin, bio=actor_bio)
    new_actor_id = actor_controller.createActor(new_actor)
    return new_actor_id, actor_name


def crawlActorFilms(link_to_profile, actorID):
    """
    From Actor's Filmography, scarping actor's film list and storing in SQLite
    :param link_to_profile: link to actor's profile page
    :param actorID: actorID saved in SQLite
    :return:
    """
    # REQUEST TO GET ACTOR'S FILM LIST (HTML VERSION)
    headers = {"Accept-Language": "en-US,en;q=0.5"}
    params = dict(lang='en-US,en;q=0.5')
    actor_films_page = rq.get(BASEURL + link_to_profile, headers=headers, params=params)
    actor_films_soup = BeautifulSoup(actor_films_page.text, 'lxml')
    actor_films_list = actor_films_soup.find('div', {'class': 'filmo-category-section'})
    actor_films_row = actor_films_list.findAll('div', attrs={"class": re.compile('^filmo-row')})

    for film_row in actor_films_row:
        film_title = ""
        film_genres = []
        film_year = ""
        film_rating = 0.0

        # GET FILM'S TITLE
        film_title_container = film_row.findAll("a", href=re.compile('^/title/tt'))
        if film_title_container[0] is not None:
            film_title = film_title_container[0].string

        # GET FILM'S YEAR
        film_year_container = film_row.findAll("span", {'class': "year_column"})
        if film_year_container[0] is not None:
            film_year = re.sub(re.compile('\n'), '', film_year_container[0].string)  # remove html tags
            film_year = film_year.strip()  # remove white spaces
            if film_year != "":
                film_year = int(film_year[:4])  # only the first four characters represent a year

        # GET FILM'S GENRE AND RATING
        film_details_page = rq.get(BASEURL + film_title_container[0]['href'])
        film_details_soup = BeautifulSoup(film_details_page.text, 'lxml')

        if film_details_soup:
            film_genres_container = film_details_soup.find('div', attrs={"data-testid": "genres"})
            if film_genres_container:
                film_genres_items = film_genres_container.findAll('span', attrs={"class": "ipc-chip__text"})
                for genre_item in film_genres_items:
                    film_genres.append(genre_item.text.strip())

        film_rating_container = film_details_soup.find('div',
                                                       {'data-testid': 'hero-rating-bar__aggregate-rating__score'})
        if film_rating_container:
            film_rating_span = film_rating_container.find('span', attrs={"class": True})
            if film_rating_span:
                film_rating = float(film_rating_span.text)

        # SAVE NEW FILM
        new_film = Film(filmID=None, title=film_title, year=film_year, rating=film_rating, genres=film_genres)
        film_controller.createFilm(actorID, new_film)


def crawlActorAwards(link_to_profile, actorID):
    """
    From actor's award page, scraping actor's award list and storing in SQLite
    :param link_to_profile: link to actor's personal information page
    :param actorID: actorID saved in SQLite
    :return:
    """
    actor_award_page = rq.get(BASEURL + link_to_profile + AWARDS_ENDPOINT)
    actor_award_soup = BeautifulSoup(actor_award_page.text, 'lxml')
    actor_award_tables = actor_award_soup.findAll('table', {'class': 'awards'})
    award_outcome = ""
    award_year = ""
    award_category = ""
    award_film_name = ""
    award_film_year = ""

    for award_table in actor_award_tables:
        award_rows = award_table.find_all('tr')
        for award_row in award_rows:
            award_year_container = award_row.find('td', attrs={"class": "award_year"})
            if award_year_container:
                award_year = int(award_year_container.find('a', href=True).text.strip())

            award_outcome_container = award_row.find('td', attrs={"class": "award_outcome"})
            if award_outcome_container:
                award_outcome = award_outcome_container.find('b').text.strip()
                award_category = award_outcome_container.find('span', attrs={"class": "award_category"}).text.strip()

            award_description_container = award_row.find('td', attrs={"class": "award_description"})
            if award_description_container:
                award_description_list = award_description_container.text.strip().split("\n")
                award_title = award_description_list[0].strip()
                if len(award_description_list) > 1:
                    award_film = award_description_list[1]
                    award_film_year = award_film.split(" ")[-1][1:-1].strip()
                    award_film_name = award_film[: award_film.find(award_film_year) - 1]
            else:
                award_title = ""
                award_film_name = ""
                award_film_year = ""

            new_award = Award(year=award_year, category=award_category, title=award_title, outcome=award_outcome,
                              award_film_name=award_film_name, award_film_year=award_film_year)

            award_controller.createAward(actorID=actorID, award=new_award)
            print("Award: " + award_title)


def removeHTMLTags(html, *tags):
    """
    Remove HTML Tags from an HTML passage
    :param html: html passage
    :param tags: tags to be removed
    :return:
    """
    soup = BeautifulSoup(html, "lxml")

    for tag in tags:
        if tag == 'br':
            for each_br in soup.findAll(tag):
                each_br.replaceWith('\n')
        else:
            for eachElement in soup.findAll(tag):
                eachElement.replaceWith(eachElement.string)

    return soup.get_text().lstrip().rstrip()


if __name__ == "__main__":
    dc.reset_data()
    crawlMainPage()
