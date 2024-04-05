import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=bb728eaadde245328754b6d098f6162c&language=en-US')
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        return f'https://image.tmdb.org/t/p/w500/{data["poster_path"]}'
    else:
        return None

# Function to recommend similar movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = i[0]
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app title and header
st.set_page_config(layout="wide")
st.title("🎬 Movie Recommender System")
st.markdown(
"""
<style>
h1 {
    color: #ff6347;
    text-align: center;
    font-size: 3.5rem;
}
.sidebar .sidebar-content {
    background-color: #f8f9fa;
}
.sidebar .sidebar-content .block-container {
    padding: 1rem;
}
.sidebar .sidebar-content .block-container .stButton>button {
    background-color: #007bff;
    color: white;
    border-radius: 0.5rem;
    padding: 0.5rem 1rem;
    font-size: 1rem;
    border: none;
    cursor: pointer;
}
.sidebar .sidebar-content .stSelectbox>div>div>div {
    background-color: #e9ecef;
    color: #343a40;
}
.stButton>button {
    background-color: #007bff;
    color: white;
    border-radius: 0.5rem;
    padding: 0.5rem 1rem;
    font-size: 1rem;
    border: none;
    cursor: pointer;
}
</style>
""",
unsafe_allow_html=True)

# Sidebar options
selected_movie_name = st.sidebar.selectbox('Select a Movie', movies['title'].values)
if st.sidebar.button('Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    num_recommendations = len(recommended_movie_names)
    num_columns = 3  # Number of columns for displaying recommendations
    num_rows = (num_recommendations + num_columns - 1) // num_columns  # Calculate number of rows

    # Create columns for recommendations
    cols = [st.columns(num_columns) for _ in range(num_rows)]

    # Iterate over recommendations and populate columns
    for i, (name, poster) in enumerate(zip(recommended_movie_names, recommended_movie_posters)):
        row_index = i // num_columns
        col_index = i % num_columns
        with cols[row_index][col_index]:
            st.text(name)
            if poster is not None:
                st.image(poster, use_column_width=True)
            else:
                st.text("No poster available")
