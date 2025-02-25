import streamlit as st
from utils.api import *
from utils.helpers import *

# Custom CSS for styling
st.markdown(
    """
    <style>
        /* Center align content */
        .movie-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-bottom: 20px;
        }
        
        /* Style for movie poster */
        .rounded-image {
            border-radius: 15px;
            width: 100px;
            margin-bottom: 10px;
        }
        
        /* Style for description box */
        .description-box {
            background-color: rgba(0, 0, 0, 0.7); /* Semi-transparent black */
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            width: 90%;
        }

        /* Title styling */
        .movie-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎬 Movie recommender")

movie_name = st.text_input("Enter a movie you've recently watched and liked: ")

if movie_name:
    # User inputs a movie name
    search_results = get_top5_movies(movie_name)

    # Search for the movie and show top 5 matches
    if search_results:
        movie_selection = st.radio("Is the movie you're referring to one of these?",
                                   [f"{m['title']} ({m['year']})" for m in search_results])
        
    # User selects the movie
    selected_movie = next(m for m in search_results if f"{m['title']} ({m['year']})" == movie_selection)
    movie_id = selected_movie["id"]

    # Get recommendations
    content_recs = get_content_based_recommendations(movie_id)
    collab_recs = get_collaborative_recommendations(movie_id)

    # Display results
    st.subheader(f"Since you liked {selected_movie['title']}:")

    # Display Content-Based recommendations
    display_recommendations(content_recs, "🔍 Content-Based recommendations")

    # Display Collaborative Filtering recommendations
    display_recommendations(collab_recs, "🤝 Collaborative Filtering")

else:
    st.error("No movies found. Try another title!")