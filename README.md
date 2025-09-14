# 🎬 Movie Project

A simple terminal-based Python application to manage your favorite movies.

## 🚀 Features

- List, add, and delete movies
- Search movies by name using the OMDb API
- Sort and filter movies
- Show statistics (average, median, etc.)
- Pick a random movie
- Export movies to an HTML website

## 🛠️ Installation

1. **Clone this repository**

```bash
git clone https://github.com/yourusername/movie-project-term4.git
cd movie-project-term4
```

2.	***Install dependencies***
```bash
pip install -r requirements.txt
```
## 📦 Imports & Dependencies

## Standard Library
	•	random → Selects a random movie from the database.
	•	os → File system handling (paths, env variables).
	•	statistics.median → Calculate the median rating.

## Third-Party Libraries
	•	colorama.Fore → Colored terminal output.
	•	fuzzywuzzy.process → Fuzzy string matching for search suggestions.
	•	requests → HTTP requests to OMDb API.
	•	dotenv → Load environment variables from .env.
	•	sqlalchemy → SQL database connection and queries.

## Local Modules
	•	utils.write__html → Generate HTML output.
	•	utils.filter_movies → Handle filtering logic for years and ratings.
	•	utils.Fore_color → Centralized colored text helper.
	•	storage.movie_storage_sql → Manage SQLite movie storage.
	•	api.Movie_API → Fetch movie data from OMDb API.

3. **Create a `.env` file**
- Inside the root directory, create a file called .env and add your OMDb API key:
- Used API: https://www.omdbapi.com/
- API_KEY=your_omdb_api_key_here


## ▶️ Usage
```bash
python main.py
```
**Menu options allow you to**:

	•	Add a movie via API
	•	Delete a movie
	•	Show statistics
	•	Filter by year or rating
	•	Pick a random movie
	•	Export to HTML

## 📁 Project Structure
```bash
project-name/
├── main.py                # Program entry point
├── requirements.txt       # Dependencies
├── .env                   # API key storage
├── /data/                 # Database files
│   └── movies.db
├── /api/                  # API integration
│   └── Movie_API.py
├── /utils/                # Utility functions
│   ├── write__html.py
│   ├── filter_movies.py
│   └── Fore_color.py
├── /storage/              # Database logic
│   └── movie_storage_sql.py
├── /web/                  # Website export
│   ├── movies.html
│   ├── movies_template.html
│   └── style.css
└── README.md
```

## 🔐 Notes
	•	API key is not included
	•	Make sure the /web/ and /data/ folders exist before running

## 📃 License

This project is for educational purposes. Feel free to use and modify it.