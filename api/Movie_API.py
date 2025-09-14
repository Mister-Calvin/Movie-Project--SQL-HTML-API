import requests
import os
from dotenv import load_dotenv
from utils.Fore_color import fore_color_text, Fore

load_dotenv()
API_KEY = os.getenv("API_KEY")



def search_movie_and_get_movies(search_movie):
    """
    :param search_movie: user-input search movie name
    :return: returns a list of dictionaries containing movie details
    """
    try:
        url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={search_movie}"
        response = requests.get(url)
        movies_as_json = response.json()
        return movies_as_json
    except KeyError:
        print("Key not found.")
    except requests.exceptions.ConnectionError:
        print("No connection to the API (ConnectionError).")
    except requests.exceptions.Timeout:
        print("API request took too long (Timeout).")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP-Error: {e.response.status_code}")

    user_input = input(fore_color_text("\nPress Enter to continue...", Fore.YELLOW))

