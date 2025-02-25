import streamlit as st
from utils.api import *
from utils.helpers import *

# Custom CSS for styling
st.markdown(
    """
    <style>
        /* Center align content */
        .movie-card {
            display: inline-block;
            width: 150px;
            margin-right: 20px;
            text-align: center;
        }

        /* Style for movie poster */
        .rounded-image {
            border-radius: 15px;
            width: 120px;
            height: 180px;
            margin-bottom: 10px;
        }

        /* Style for description box */
        .description-box {
            background-color: rgba(0, 0, 0, 0.7); /* Semi-transparent black */
            color: white;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            font-size: 12px;  /* Smaller font */
            max-width: 180px; /* Smaller width */
            margin: 0 auto;
        }

        /* Title styling */
        .movie-title {
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 10px;
        }

        /* Horizontal scrolling for recommendations */
        .recommendations-row {
            display: flex;
            overflow-x: auto;
            padding: 10px;
        }

        /* Hide the radio buttons once a selection is made */
        .selection-radio {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎬 Movie recommender")

# User inputs a movie name
movie_name = st.text_input("Enter a movie you've recently watched and liked:", "")

if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None

if movie_name:
    # Search for the movie and show top 5 matches
    search_results = get_top5_movies(movie_name)
    
    if search_results:
        if not st.session_state.selected_movie:
            movie_selection = None

            with st.expander("Is your movie one of these?"):
                # Displaying movies with their posters
                cols = st.columns(5)  # Display in a row of 5 columns
                selected_index = -1

                for i, movie in enumerate(search_results):
                    col = cols[i % 5]  # Distribute movies into columns

                    with col:
                        # Show poster with title and year for easier recognition
                        if movie["poster"]:
                            st.image(movie["poster"], width=120, use_container_width=True)
                        else:
                            st.image("https://images.entertainment.ie/uploads/2021/08/27144852/generic-movie-poster.jpg?w=400&q=high", width=120, use_container_width=True)

                        st.markdown(f'**{movie["title"]} ({movie["year"]})**')

                selected_movie = st.radio("", options=search_results, format_func=lambda m: f"{m['title']} ({m['year']})", index=None)

                if selected_movie:  # Movie selected
                    st.session_state.selected_movie = selected_movie

        if st.session_state.selected_movie:
            selected_movie = st.session_state.selected_movie
            movie_id = selected_movie["id"]

            # Get recommendations
            content_recs = get_content_based_recommendations(movie_id)
            collab_recs = get_collaborative_recommendations(movie_id)

            # Display results
            st.subheader(f"✨ Since you liked '{selected_movie['title']}':")

            # Display Collaborative Filtering Recommendations in columns
            st.markdown("### 🤝 Collaborative Filtering recommendations")
            st.markdown(f"These recommendations are based on the preferences of other users who have watched and liked similar movies. "
                        f"The algorithm looks at patterns in user behavior, like ratings and watch history, to suggest movies that similar users liked.")
            cols = st.columns(len(collab_recs))  # Create a column for each recommendation
            for i, rec in enumerate(collab_recs):
                with cols[i]:
                    st.image(rec["poster"], width=120)
                    st.markdown(f'**{rec["title"]}** ({rec["year"]})')

            # Display Content-Based Recommendations in columns
            st.markdown("### 🔍 Content-Based recommendations")
            st.markdown(f"These recommendations are based on the attributes of the movie you selected, such as the genre and the plot. "
                        f"The algorithm finds other movies with similar features and suggests them to you.")
            cols = st.columns(len(content_recs))  # Create a column for each recommendation
            for i, rec in enumerate(content_recs):
                with cols[i]:
                    st.image(rec["poster"], width=120)
                    st.markdown(f'**{rec["title"]}** ({rec["year"]})')

    else:
        st.error("No movies found. Try another title!")