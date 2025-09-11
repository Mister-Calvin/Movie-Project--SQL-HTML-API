import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")



def search_movie_and_get_movies(search_movie):
    """
    :param search_movie: user-input search movie name
    :return: returns a list of dictionaries containing movie details
    """
    url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={search_movie}"
    response = requests.get(url)
    movies_as_json = response.json()
    return movies_as_json
