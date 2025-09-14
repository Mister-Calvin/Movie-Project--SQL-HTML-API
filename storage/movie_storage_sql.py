import os
from sqlalchemy import create_engine, text

db_path = os.path.join("data", "movies.db")
DB_URL = f"sqlite:///{db_path}"


# Create the engine
engine = create_engine(DB_URL)

# Create the movies table if it does not exist
def create_movies_table():
    """ create a table if it doesn't exist """
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL,
                poster TEXT NOT NULL
            )
        """))
        return connection.commit()


def get_movies():
    """Retrieve all movies from the database."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT title, year, rating, poster FROM movies"))
            movies = result.fetchall()

        return {row[0]: {"year": row[1], "rating": row[2], "poster": row[3]} for row in movies}
    except Exception as e:
        print(f"Error getting movies: {e}")


def add_movie(title, year, rating, poster):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO movies (title, year, rating, poster) VALUES (:title, :year, :rating, :poster)"),
                               {"title": title, "year": year, "rating": rating, "poster": poster})
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            connection.rollback()
            print(f"Error adding Movie: {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("DELETE FROM movies WHERE title = :title"),
                               {"title": title})
            connection.commit()
            print(f"Movie '{title}' deleted successfully.")
        except Exception as e:
            connection.rollback()
            print(f"Error delete Movie: {e}")


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("UPDATE movies SET rating = :rating WHERE title = :title"),
                               {"rating": rating, "title": title})
            connection.commit()
            print(f"Movie '{title}' updated successfully.")
        except Exception as e:
            connection.rollback()
            print(f"Error update Movie: {e}")
