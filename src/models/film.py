class Film:
    def __init__(self, filmID, title, year, rating, genres: list):
        self.filmID = filmID
        self.title = title
        self.year = year
        self.rating = rating
        self.genres = genres