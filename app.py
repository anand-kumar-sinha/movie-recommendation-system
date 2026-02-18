import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os


url = "https://drive.google.com/uc?id="
if not os.path.exists("movie_dict.pkl"):
    gdown.download(url + "1tc7X99yKDX6xYR9pOsObE_X9efrpXZIS", "movie_dict.pkl", quiet=False)

if not os.path.exists("movie.pkl"):
    gdown.download(url + "12DVEXIZEEezA9zRelsQYVlmRsNkF5Lhj", "movies.pkl", quiet=False)

if not os.path.exists("similarity.pkl"):
    gdown.download(url + "1y-sXGrGhZy74PyCmXdgnUY22T9TsctFX", "similarity.pkl", quiet=False)

def fetch_poster(movie_id):
    try:
        response = requests.get('https://api.themoviedb.org/3/movie/' +str(movie_id) +'?api_key=50f45a92b2999c23f6b1aac93338b022&language=en', timeout = 3)
        data = response.json()
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    except:
        return "https://image.tmdb.org/t/p/w500/nXdAh5vUwERL4WGVMaee8RoDEAS.jpg"

def recommend_movie(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        #fetch poster from api

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster


similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)


st.title('Movie Recommendation System')
selected_movie_name = st.selectbox("Please select a movie to recommend",movies['title'].values)

if st.button("Recommend"):
    name, posters = recommend_movie(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(name[0])
        st.image(posters[0])
    with col2:
        st.text(name[1])
        st.image(posters[1])
    with col3:
        st.text(name[2])
        st.image(posters[2])
    with col4:
        st.text(name[3])
        st.image(posters[3])
    with col5:
        st.text(name[4])
        st.image(posters[4])