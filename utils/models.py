class Movie:
    def __init__(self, title, genre, duration):
        self.title = title
        self.genre = genre
        self.duration = duration


class Cinema:
    def __init__(self, name, location, movies_playing):
        self.name = name
        self.location = location
        self.movies_playing = movies_playing


class Screening:
    def __init__(self, movie, cinema, time):
        self.movie = movie
        self.cinema = cinema
        self.time = time


class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
