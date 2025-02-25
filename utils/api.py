import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access variables
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

def get_top5_movies(movie_name):
    """
    Fetches multiple movies matching the query.
    """
    url = f"{BASE_URL}search/movie?api_key={API_KEY}&query={movie_name}&page=1"
    response_aux = requests.get(url).json()

    if "results" not in response_aux or len(response_aux["results"]) == 0:
        return None # No movies found
    
    response = sorted(response_aux["results"], key=lambda d: d['vote_count'], reverse=True)

    movies = []
    for movie in response[:5]: # Get top 5 results
        movies.append({
            "id": movie["id"],
            "title": movie["title"],
            "year": movie.get("release_date", "Unknown")[:4] if movie.get("release_date") else "Unknown",
            "poster": f"https://image.tmdb.org/t/p/w200{movie.get('poster_path')}" if movie.get("poster_path") else None
        })
    return movies

def get_collaborative_recommendations(movie_id, num_results=5):
    """
    Fetch movies recommended based on user ratings.
    """
    url = f"{BASE_URL}movie/{movie_id}/recommendations?api_key={API_KEY}"
    response = requests.get(url).json()

    if "results" not in response or len(response["results"]) == 0:
        return []
    
    recommendations = []
    for movie in response["results"][:num_results]:
        recommendations.append({
            "id": movie["id"],
            "title": movie["title"],
            "year": movie.get("release_date", "Unknown")[:4] if movie.get("release_date") else "Unknown",
            "description": movie.get("overview", "No description available.") if movie.get("overview") else "No description available.",
            "poster": f"https://image.tmdb.org/t/p/w200{movie.get('poster_path')}" if movie.get("poster_path") else None
        })
    return recommendations

def get_content_based_recommendations(movie_id, num_results=5):
    """
    Fetch similar movies based on metadata similarity (genre & plot).
    """
    url = f"{BASE_URL}movie/{movie_id}/similar?api_key={API_KEY}"
    response = requests.get(url).json()

    if "results" not in response or len(response["results"]) == 0:
        return []
    
    recommendations = []
    for movie in response["results"][:num_results]:
        recommendations.append({
            "id": movie["id"],
            "title": movie["title"],
            "year": movie.get("release_date", "Unknown")[:4] if movie.get("release_date") else "Unknown",
            "description": movie.get("overview", "No description available.") if movie.get("overview") else "No description available.",
            "poster": f"https://image.tmdb.org/t/p/w200{movie.get('poster_path')}" if movie.get("poster_path") else None
        })
    return recommendations
