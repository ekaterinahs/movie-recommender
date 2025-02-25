import streamlit as st

def display_recommendations(movies, title):
    """
    Displays a list of recommended movies under a given title using Streamlit.
    """
    st.markdown(f"### {title}")
    for movie in movies:
        # Display movie poster
        if movie["poster"]:
            st.markdown(f'<img src="{movie["poster"]}" class="rounded-image">', unsafe_allow_html=True)
        else:
            st.markdown("🎬")
        
        # Display movie title and year
        st.markdown(f'<div class="movie-title">{movie["title"]} ({movie["year"]})</div>', unsafe_allow_html=True)
        
        # Display movie description in a rounded, opaque box
        st.markdown(f'<div class="description-box">{movie["description"]}</div>', unsafe_allow_html=True)

        st.markdown(f'</div>', unsafe_allow_html=True)