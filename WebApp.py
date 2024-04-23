import pickle
import streamlit as sl
import requests

def fetchPic(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxMTcxYmM3MzkzNTc4MGE5OWY3NzhkOGZhYjIwMjA4NCIsInN1YiI6IjY2MjE5NWEyZTRjOWViMDE3Y2Y2MDMyZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Ju3GQ931E3dg3F-SqP9G8-v1q80dqHN4so3QZcSi91o"
    }
    response = requests.get(url, headers=headers)
    response = response.json()
    poster_path = response['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

    return full_path

# Function that recommends similar movies when a movie is passed through as an argument
def recommendMovie(movie):
    # finds the index of the movie in the data frame based on its title
    index = movies[movies['title'] == movie].index[0]
    # Sorts the indices of movies based on their cosine similarity scores in descending order
    distances = sorted(list(enumerate(similarities[index])), reverse=True, key=lambda x: x[1])
    recMovieNames = []
    recMoviePics = []
    # Print titles of the recommended movies
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recMoviePics.append(fetchPic(movie_id))
        recMovieNames.append(movies.iloc[i[0]].title)

    return recMovieNames,recMoviePics

sl.header("MovieMate")
movies = pickle.load(open('MovieMate\embeddings\movies.pkl', 'rb'))
similarities = pickle.load(open('MovieMate\embeddings\similarity.pkl', 'rb'))

movieList = movies['title'].values

chosenMovie = sl.selectbox('Enter/choose a movie to receive a recommendation', movieList)

if sl.button('Go'):
    recMovieNames, recMoviePics = recommendMovie(chosenMovie)
    col1, col2, col3, col4, col5 = sl.columns(5)
    with col1:
        sl.text(recMovieNames[0])
        sl.image(recMoviePics[0])
    with col2:
        sl.text(recMovieNames[1])
        sl.image(recMoviePics[1])
    with col3:
        sl.text(recMovieNames[2])
        sl.image(recMoviePics[2])
    with col4:
        sl.text(recMovieNames[3])
        sl.image(recMoviePics[3])
    with col5:
        sl.text(recMovieNames[4])
        sl.image(recMoviePics[4])
