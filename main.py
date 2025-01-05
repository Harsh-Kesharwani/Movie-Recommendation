import streamlit as st
import pickle
import pandas as pd
import requests

import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('API_KEY')

def fetch_posters(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}')
    data = response.json()
    if 'poster_path' in data:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    return None

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # Assuming you have movie_id column in your DataFrame
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_posters(movie_id))
    
    return recommended_movies, recommended_movies_posters

# Load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie',  # Updated the label to be more clear
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    
    # Create 5 columns for the 5 recommendations
    cols = st.columns(5)
    
    for idx, (name, poster) in enumerate(zip(names, posters)):
        with cols[idx]:
            if poster:
                st.image(poster)
            st.write(name)