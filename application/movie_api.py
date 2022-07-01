from urllib.request import urlopen
import json

API_KEY = '6c86c532'


def get_movie_by_title(title):
    url = f"https://www.omdbapi.com?&t={title}&apikey={API_KEY}"
    url = url.replace(" ", "%20")
    response = urlopen(url)
    data_movie_json = json.loads(response.read())
    if "Error" in data_movie_json:
        return data_movie_json
    data_json = {
        'Title': data_movie_json['Title'],
        'Year': data_movie_json['Year'],
        'id': data_movie_json['imdbID'],
        'Released': data_movie_json['Released'],
        'Runtime': data_movie_json['Runtime'],
        'Genre': data_movie_json['Genre'],
        'Director': data_movie_json['Director'],
        'Writer': data_movie_json['Writer'],
        'Actors': data_movie_json['Actors'],
        'Plot': data_movie_json['Plot']
    }
    return data_json


def get_movie_by_id(id):
    url = f"https://www.omdbapi.com?&i={id}&apikey={API_KEY}"
    response = urlopen(url)
    data_movie_json = json.loads(response.read())
    if "Error" in data_movie_json:
        return data_movie_json
    data_json = {
        'Title': data_movie_json['Title'],
        'Year': data_movie_json['Year'],
        'id': data_movie_json['imdbID'],
        'Released': data_movie_json['Released'],
        'Runtime': data_movie_json['Runtime'],
        'Genre': data_movie_json['Genre'],
        'Director': data_movie_json['Director'],
        'Writer': data_movie_json['Writer'],
        'Actors': data_movie_json['Actors'],
        'Plot': data_movie_json['Plot']
    }
    return data_json
