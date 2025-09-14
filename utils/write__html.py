from storage.movie_storage_sql import get_movies
import os



def serialize_type():
    """ returns the html for each movie """
    movies = get_movies()

    output = ""
    output += '<html>\n'
    output += '<head>\n'
    output += '<title>My Movie App</title>\n'
    output += '<link rel="stylesheet" href="style.css"/>\n'
    output += '</head>\n'
    output += '<body>\n'
    output += '<div class="list-movies-title">\n'
    output += '<h1>My Movie App</h1>\n'
    output += '</div>\n'
    output += '<div>\n'
    output += '<ol class="movie-grid">\n'


    for title, info in movies.items():
        output += '<li>\n'
        output += '<div class="movie">\n'
        output += f'<img class="movie-poster" src="{info["poster"]}"/>\n'
        output += f'<div class="movie-title">{title}</div>\n'
        output += f'<div class="movie-year">{info["year"]}</div>\n'
        output += '</div>\n'
        output += '</li>\n'

    output += '</ol>\n'
    output += '</div>\n'
    output += '</body>\n'
    output += '</html>\n'

    return output


def write_html(output):
    """ writes the html to disk """
    try:
        output_path = os.path.join("web", "movies.html")
        with open(output_path, "w") as file:
            file.write(serialize_type())
            print("Website was generated successfully.")
    except Exception as e:
        print(f"Error while writing html file: {e}")


