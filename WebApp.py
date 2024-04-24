import pickle # Importing pickle in order to open .pkl embeddings
import streamlit as sl  # Importing Streamlit for building the web app
import requests  # Importing requests library for API calls

# Function to fetch the movie poster using the movie ID from The Movie Database (TMDb)
def fetchPic(movie_id):
    # Creating the URL to request movie data from TMDb
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)
    
    # Setting up the required headers for the API request
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxMTcxYmM3MzkzNTc4MGE5OWY3NzhkOGZhYjIwMjA4NCIsInN1YiI6IjY2MjE5NWEyZTRjOWViMDE3Y2Y2MDMyZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Ju3GQ931E3dg3F-SqP9G8-v1q80dqHN4so3QZcSi91o"
    }
    
    # Sending the request and getting the response
    response = requests.get(url, headers=headers)
    response = response.json()
    
    # Extracting the poster path from the response
    poster_path = response['poster_path']
    
    # Constructing the full path for the movie poster
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

    return full_path

# Function that recommends similar movies when a movie is passed through as an argument
def recommendMovie(movie):
    # Find the index of the movie in the data frame based on its title
    index = movies[movies['title'] == movie].index[0]
    
    # Sort the indices of movies based on their cosine similarity scores in descending order
    distances = sorted(list(enumerate(similarities[index])), reverse=True, key=lambda x: x[1])
    
    # Lists to store recommended movie names and their posters
    recMovieNames = []
    recMoviePics = []
    
    # Printing titles of the recommended movies
    for i in distances[1:6]:
        # Fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recMoviePics.append(fetchPic(movie_id))
        recMovieNames.append(movies.iloc[i[0]].title)

    return recMovieNames, recMoviePics

# Display header
sl.header("MovieMate")

# Loading embeddings of movie data and similarity scores
movies = pickle.load(open('movies.pkl', 'rb'))
similarities = pickle.load(open('similarity.pkl', 'rb'))

# Creating a dropdown list of movie titles
movieList = movies['title'].values

# Select box to enter or choose a movie to receive a recommendation
chosenMovie = sl.selectbox('Enter/choose a movie to receive a recommendation', movieList)

# Button to trigger the recommendation process
if sl.button('Go'):
    # Getting recommended movie names and their poster URLs
    recMovieNames, recMoviePics = recommendMovie(chosenMovie)
    
    # Displaying recommended movies and their posters in columns
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

