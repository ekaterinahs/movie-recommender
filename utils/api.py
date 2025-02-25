import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access variables
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

def get_movie_id(movie_name):
    """Fetches multiple movies matching the query."""
    url = f"{BASE_URL}search/movie?api_key={API_KEY}&query={movie_name}&page=1"
    response = requests.get(url).json()

    if "results" not in response or len(response["results"]) == 0:
        return None # No movies found

    movies = []
    for movie in response["results"][:5]: # Get top 5 results
        movies.append({
            "id": movie["id"],
            "title": movie["title"],
            "year": movie.get("release_date", "Unknown")[:4],
            "poster": f"https://image.tmdb.org/t/p/w200{movie.get('poster_path')}" if movie.get("poster_path") else None
        })

    return movies

def get_movie_metadata(movie_id):
    """Fetches metadata for a movie."""
    url = f"{BASE_URL}movie/{movie_id}?api_key={API_KEY}&append_to_response=keywords,credits"
    response = requests.get(url).json
    return response
