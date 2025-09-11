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

3. **Create a `.env` file**
- Inside the root directory, create a file called .env and add your OMDb API key:
- Used API: https://www.omdbapi.com/
- API_KEY=your_omdb_api_key_here

## ▶️ Usage
```bash
python main.py
```

## 📁 Project Structure
```bash
project-name/
├── main.py
├── requirements.txt
├── .env
├── /data/            # Database or files
├── /api/             # API integration
├── /utils/           # Utility functions
├── /storage/         # Database access
├── /web/             # HTML/CSS files
└── README.md
```

## 🔐 Notes
	•	API key is not included
	•	Make sure the /web/ and /data/ folders exist before running

## 📃 License

This project is for educational purposes. Feel free to use and modify it.