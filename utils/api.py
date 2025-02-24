import requests
from config import API_KEY, BASE_URL

def get_movie_id(movie_name):
    """Fetches the movie ID from TMDb API."""
    url = f"{BASE_URL}search/movie?api_key={API_KEY}&query={movie_name}"
    response = requests.get(url).json()
    return response["results"][0]["id"] if response.get("results") else None

def get_movie_metadata(movie_id):
    """Fetches metadata for a movie."""
    url = f"{BASE_URL}movie/{movie_id}?api_key={API_KEY}&append_to_response=keywords,credits"
    response = requests.get(url).json
    return response
