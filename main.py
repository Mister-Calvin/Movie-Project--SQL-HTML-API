# === Standard Library ===
import random
import os
from statistics import median

# === Third-Party Libraries ===
from fuzzywuzzy import process
import requests
from dotenv import load_dotenv

# === Local Modules ===
from utils import write__html
from utils.write__html import write_html
from storage import movie_storage_sql
from storage.movie_storage_sql import get_movies
from api.Movie_API import search_movie_and_get_movies
from utils.filter_movies import clean_year, min_rating, start_year, end_year
from utils.Fore_color import fore_color_text, Fore


class InvalidRangeError(Exception):
    """ my own Error-funktion for numbers
    not in range 0-10"""
    pass



def find_movie_by_title(movie_input):
    """Search for a movie title in the database.

        :param movie_input: The title of the movie entered by the user (string).
        :return: The correctly cased movie title from the database if found,
                 otherwise None."""
    movies = get_movies()
    for movie_title in movies:
        if movie_title.lower() == movie_input.lower():
            return movie_title
    return None


def list_movies():
    """
    :print list all the movies
    """
    movies = get_movies()
    for title, info in movies.items():
        print(fore_color_text(f"{title} ({info['year']}): {info['rating']}", Fore.MAGENTA))


def add_movie():
    """ add a new movie to the database"""
    while True:
        movie_input = input(fore_color_text("Enter movie name: ", Fore.YELLOW)).title()
        if not movie_input:
            print("Movie name cannot be empty")
            continue

        movie_keys = find_movie_by_title(movie_input)
        if movie_keys:
            print(fore_color_text("Movie already exists", Fore.RED))
            return
        movie_data = search_movie_and_get_movies(movie_input)
        if movie_data:
            title = movie_data['Title']
            year = movie_data['Year']
            rating = movie_data['imdbRating']
            poster = movie_data['Poster']
            movie_storage_sql.add_movie(title, year, rating, poster)
            print(f"Movie {movie_input} successfully added")
            return
        else:
            print(f"Movie {movie_input} was not found API")


def delete_movie():
    """
    :delete a existing movie from the database
    """
    while True:
        movie_input = input(fore_color_text("Enter movie name: ", Fore.YELLOW)).title()
        movie_keys = find_movie_by_title(movie_input)
        if movie_keys:
            movie_storage_sql.delete_movie(movie_keys)
            print(f"Movie {movie_keys} successfully deleted")
            return
        else:
            print(fore_color_text("Movie does not exist", Fore.RED))


def movies_sorted_by_year():
    """print sorted movies by the parameter "year" """
    movies = get_movies()
    sorted_movies = sorted(movies.items(), key=lambda x: clean_year(x[1].get("year", 0)), reverse=True)
    for title, info in sorted_movies:
        print(f"{title} ({info.get('year', 'Unknown')}): {info['rating']}")


def movies_sorted_by_rating():
    """print sorted movies by the parameter "rating" """
    movies = get_movies()
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
    for title, info in sorted_movies:
        print(f"{title} ({info['year']}): {info['rating']}")


def all_ratings():
    """ return: a list of all ratings """
    movies = get_movies()
    ratings = []
    for info in movies.values():
        ratings.append(info['rating'])
    return ratings


def average_rating():
    """print the average rating of the movies"""
    ratings = all_ratings()
    print(f"Average rating: {sum(ratings) / len(ratings):.2f}")


def find_median():
    """find and print the median rating of the movies"""
    ratings = all_ratings()
    movie_median = median(ratings)
    print(f"Movie median rating: {movie_median:.2f}")


def best_and_worst():
    """find and the best and worst rating of the movies and print the title and info"""
    movies = get_movies()
    rating = all_ratings()
    max_rating = max(rating)
    min_rating = min(rating)
    for title, info in movies.items():
        if info["rating"] == max_rating:
            print(f"Best Film: {title} ({info['year']}): {info['rating']}")
        elif info['rating'] == min_rating:
            print(f"Worst Film: {title} ({info['year']}): {info['rating']}")


def stats():
    """print the statistics of the movies"""
    average_rating()
    find_median()
    best_and_worst()


def menu():
    """the choose menu with inbuilt functions"""
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
    min_rating_value = min_rating()
    start_year_value = start_year()
    end_year_value = end_year()

    print("----Filtering movies----")
    for title, info in movies.items():
        if min_rating_value is not None and info['rating'] < min_rating_value:
            continue
        if start_year_value is not None and clean_year(info['year']) < start_year_value:
            continue
        if end_year_value is not None and clean_year(info['year']) > end_year_value:
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
        except ValueError:
            print("You did not enter a valid number.")
        except InvalidRangeError:
            print("You did not enter a number between the range.")
        user_input = input(fore_color_text("\nPress Enter to continue...", Fore.YELLOW))


if __name__ == "__main__":
    main()

