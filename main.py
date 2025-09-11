# === Standard Library ===
import random
import os
from statistics import median

# === Third-Party Libraries ===
from colorama import Fore
from fuzzywuzzy import process
import requests
from dotenv import load_dotenv

# === Local Modules ===
from utils import write__html
from utils.write__html import write_html
from storage import movie_storage_sql
from storage.movie_storage_sql import get_movies
from api.Movie_API import search_movie_and_get_movies
"""
Imports used in this project:

- Standard Library:
    - random: Selects a random movie from the database.
    - os: Interacts with the operating system (e.g. for file paths).
    - statistics.median: Calculates the median of all ratings.

- Third-Party Libraries:
    - colorama.Fore: Enables colored terminal output.
    - fuzzywuzzy.process: Enables fuzzy string matching for search suggestions.
    - requests: Handles HTTP requests to the OMDb API.
    - dotenv: Loads environment variables (e.g., API keys) from a .env file.

- Local Modules:
    - utils.write__html: Contains HTML generation functions.
    - storage.movie_storage_sql: Manages SQL-based movie storage.
    - api.Movie_API: Fetches movie data from the OMDb API.
"""


class InvalidRangeError(Exception):
    """ my own Error-funktion for numbers
    not in range 0-10"""
    pass


def fore_color_text(text, fore_color):
    """
    :param text: the text to be colored
    :param fore_color: the color of the text
    :return: reset the original color
    """
    return (f"{fore_color}{text}{Fore.RESET}")


def check_keys_and_return_them(movie_input):
    """ checks if input.lower is in dictionary or not
    :param movie_input: the movie to check
    :return: return keys from dictionary so the title or if movie not exist return None
    """
    movies = get_movies()
    for keys in movies:
        if keys.lower() == movie_input.lower():
            return keys
    return None


def list_movies():
    """
    :print list all the movies
    """
    movies = get_movies()
    for title, info in movies.items():
        print(fore_color_text(f"{title} ({info["year"]}): {info["rating"]}", Fore.MAGENTA))


def add_movie():
    """ add a new movie to the database"""
    movies = get_movies()
    while True:
        movie_input = input(fore_color_text("Enter movie name: ", Fore.YELLOW)).title()
        if not movie_input:
            print("Movie name cannot be empty")
            continue

        movie_keys = check_keys_and_return_them(movie_input)
        if movie_keys:
            print(fore_color_text("Movie already exists", Fore.RED))
            return

        title = search_movie_and_get_movies(movie_input)["Title"]
        year = search_movie_and_get_movies(movie_input)["Year"]
        rating = search_movie_and_get_movies(movie_input)["imdbRating"]
        poster = search_movie_and_get_movies(movie_input)["Poster"]
        movie_storage_sql.add_movie(title, year, rating, poster)
        print(f"Movie {movie_input} successfully added")
        return


def delete_movie():
    """
    :delete a existing movie from the database
    """
    movies = get_movies()
    while True:
        movie_input = input(fore_color_text("Enter movie name: ", Fore.YELLOW)).title()
        movie_keys = check_keys_and_return_them(movie_input)
        if movie_keys:
            del movies[movie_keys]
            movie_storage_sql.delete_movie(movie_keys)
            print(f"Movie {movie_keys} successfully deleted")
            return
        else:
            print(fore_color_text("Movie does not exist", Fore.RED))


def update_movie():
    """update the rating of the movie"""
    movies = get_movies()
    while True:
        movie_input = input(fore_color_text("Enter movie name: ", Fore.YELLOW)).title()
        movie_keys = check_keys_and_return_them(movie_input)

        if movie_keys:
            while True:
                try:
                    rating_input = float(input("Enter new movie rating 1-10: "))
                    if rating_input < 1 or rating_input > 10:
                        print("Invalid rating")
                        continue
                    break
                except ValueError:
                    print("Please enter ONLY numbers between 1-10!")

            movie_storage_sql.update_movie(movie_keys, rating_input)
            print(f"Movie {movie_keys} successfully updated")
            return
        else:
            print(fore_color_text("Movie does not exist", Fore.RED))


def movies_sorted_by_year():
    """print sorted movies by the parameter "year" """
    movies = get_movies()

    def clean_year(year_value):
        """Take only the first 4 digits if year looks like '1997–' """
        year_str = str(year_value)
        if year_str[:4].isdigit():
            return int(year_str[:4])

    sorted_movies = sorted(movies.items(), key=lambda x: clean_year(x[1].get("year", 0)), reverse=True)
    for title, info in sorted_movies:
        print(f"{title} ({info.get('year', "Unknown")}): {info['rating']}")


def movies_sorted_by_rating():
    """print sorted movies by the parameter "rating" """
    movies = get_movies()
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]["rating"], reverse=True)
    for title, info in sorted_movies:
        print(f"{title} ({info['year']}): {info['rating']}")


def all_ratings():
    """ return: a list of all ratings """
    movies = get_movies()
    ratings = []
    for info in movies.values():
        ratings.append(info["rating"])
    return ratings


def average_rating():
    """print the average rating of the movies"""
    movies = get_movies()
    ratings = all_ratings()
    print(f"Average rating: {sum(ratings) / len(ratings):.2f}")


def find_median():
    """find and print the median rating of the movies"""
    movies = get_movies()
    ratings = all_ratings()
    movie_median = median(ratings)
    print(f"Movie median rating: {movie_median:.2f}")


def best_and_worst():
    """find and the best and worst rating of the movies and print the title and info"""
    movies = get_movies()
    max_rating = max(all_ratings())
    min_rating = min(all_ratings())
    for title, info in movies.items():
        if info["rating"] == max_rating:
            print(f"Best Film: {title} ({info['year']}): {info['rating']}")
        elif info["rating"] == min_rating:
            print(f"Worst Film: {title} ({info['year']}): {info['rating']}")


def stats():
    """print the statistics of the movies"""
    average_rating()
    find_median()
    best_and_worst()


def menu():
    """the choose menu with inbuilt functions"""
    movies = get_movies()
    while True:
        try:
            choose_menu = int(input(fore_color_text("Menu: "
                                                    "\n0. Exit"
                                                    "\n1. List movies "
                                                    "\n2. Add movie "
                                                    " \n3. Delete movie"
                                                    "\n4. Stats"
                                                    "\n5. Random movie"
                                                    "\n6. Search movie"
                                                    "\n7. Movies sorted by rating"
                                                    "\n8. Movies sorted by year"
                                                    "\n9. Filter Movies"
                                                    "\n10. Generate Website"

                                                    "\nEnter choice (0-10): \n", Fore.CYAN)))

            if choose_menu == 0:
                return False
            elif choose_menu < 0 or choose_menu > 10:
                raise InvalidRangeError("Please enter a number between 1-10.")

            elif choose_menu == 1:
                list_movies()
            elif choose_menu == 2:
                add_movie()
            elif choose_menu == 3:
                delete_movie()
            elif choose_menu == 4:
                stats()
            elif choose_menu == 5:
                random_movie()
            elif choose_menu == 6:
                search_movie()
            elif choose_menu == 7:
                movies_sorted_by_rating()
            elif choose_menu == 8:
                movies_sorted_by_year()
            elif choose_menu == 9:
                filter_movies()
            elif choose_menu == 10:
                write_html(write__html.serialize_type())

            return True

        except ValueError:
            print("You did not enter a valid number.")
        except InvalidRangeError as e:
            print(e)


def random_movie():
    """ prints a random movie """
    movies = get_movies()
    random_film = (random.choice(list(movies.items())))
    print(
        f"Your movie for tonight: {random_film[0]} ({random_film[1]['year']}), \nit´s rated {random_film[1]['rating']}")
    return


def search_movie():
    """ search for a movie"""
    movies = get_movies()
    """ new modul for better search in the dictionary"""

    which_movie = input(fore_color_text("Which movie do you want to search? ", Fore.YELLOW))

    movie_titles = list(movies.keys())
    best_film, score = process.extractOne(which_movie, movie_titles)

    if score == 100:
        print(best_film, movies[best_film])
    elif score > 60:
        print(f"did you mean {best_film}?")
    else:
        print("No movie found")


def filter_movies():
    """ print the movies by filtering out movies """
    movies = get_movies()

    def clean_year(year_value):
        """Take only the first 4 digits if year looks like '1997–' """
        year_str = str(year_value)
        if year_str[:4].isdigit():
            return int(year_str[:4])

    # Min Rating
    while True:
        min_rating = input("Enter min rating (leave blank if you want None): ")
        if not min_rating:
            min_rating = None
            break
        try:
            min_rating = float(min_rating)
            if min_rating < 0 or min_rating > 10:  # keine negativen Ratings
                print("Rating cannot be negative or greater than 10.")
                continue
            break
        except ValueError:
            print("Please enter a valid number for rating.")

    # Start Year
    while True:
        start_year = input("Enter start year (leave blank if you want None): ")
        if not start_year:
            start_year = None
            break
        try:
            start_year = int(start_year)
            if start_year < 0:  # keine negativen Jahreszahlen
                print("Year cannot be negative.")
                continue
            break
        except ValueError:
            print("Please enter a valid year.")

    # End Year
    while True:
        end_year = input("Enter end year (leave blank if you want None): ")
        if not end_year:
            end_year = None
            break
        try:
            end_year = int(end_year)
            if end_year < 0:
                print("Year cannot be negative.")
                continue
            break
        except ValueError:
            print("Please enter a valid year.")

    print("----Filtering movies----")
    for title, info in movies.items():
        if min_rating is not None and info["rating"] < min_rating:
            continue
        if start_year is not None and clean_year(info["year"]) < start_year:
            continue
        if end_year is not None and clean_year(info["year"]) > end_year:
            continue

        print(fore_color_text(f"{title} ({info['year']}): {info['rating']}", Fore.GREEN))


def main():
    """ the main function"""
    print(fore_color_text("Welcome to my Movie-Tool :-)", Fore.MAGENTA))
    movie_storage_sql.create_movies_table()
    while True:
        try:
            if not menu():
                print(fore_color_text("Bye!", Fore.YELLOW))
                break
            user_input = input(fore_color_text("\nPress Enter to continue...", Fore.YELLOW))
        except FileNotFoundError:
            print("File not found.")
            break
        except KeyError:
            print("Key not found.")
            user_input = input(fore_color_text("\nPress Enter to continue...", Fore.YELLOW))
        except requests.exceptions.ConnectionError:
            print("No connection to the API (ConnectionError).")
            user_input = input(fore_color_text("\nPress Enter to continue...", Fore.YELLOW))
        except requests.exceptions.Timeout:
            print("API request took too long (Timeout).")
            user_input = input(fore_color_text("\nPress Enter to continue...", Fore.YELLOW))
        except requests.exceptions.HTTPError as e:
            print(f"HTTP-Error: {e.response.status_code}")
            user_input = input(fore_color_text("\nPress Enter to continue...", Fore.YELLOW))


if __name__ == "__main__":
    main()

