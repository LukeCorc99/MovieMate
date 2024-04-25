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
    posterPath = response['poster_path']
    
    # Constructing the full path for the movie poster
    fullPath = "https://image.tmdb.org/t/p/w500/" + posterPath

    return fullPath

# Function to fetch the movie official homepage using the movie ID from The Movie Database (TMDb)
def fetchHomepage(movie_id):
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
    
    # Extracting the homepage path from the response
    homepage = response['homepage']

    return homepage

# Function to fetch the movie's information using the movie ID from The Movie Database (TMDb)
def fetchInfo(movie_id):
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
    
    # Extracting the information on the movie from the response
    info = response['overview']

    return info

# Function to fetch the movie's rating using the movie ID from The Movie Database (TMDb)
def fetchRating(movie_id):
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
    
    # Extracting the rating of the movie from the response
    rating = response['vote_average']
    
    # Convert the rating to two decimal places
    rating = round(rating, 2)

    return rating

# Function that recommends similar movies when a movie is passed through as an argument
def recommendMovie(movie):
    # Find the index of the movie in the data frame based on its title
    index = movies[movies['title'] == movie].index[0]
    
    # Sort the indices of movies based on their cosine similarity scores in descending order
    distances = sorted(list(enumerate(similarities[index])), reverse=True, key=lambda x: x[1])
    
    # Lists to store recommended movie names and their posters, and links to info
    recMovieNames = []
    recMoviePics = []
    recMovieHomepage = []
    recMovieInfo = []
    recMovieRating = []
    
    # Printing titles of the recommended movies
    for i in distances[1:6]:
        # Fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recMoviePics.append(fetchPic(movie_id))
        recMovieNames.append(movies.iloc[i[0]].title)
        recMovieHomepage.append(fetchHomepage(movie_id))
        recMovieInfo.append(fetchInfo(movie_id))
        recMovieRating.append(fetchRating(movie_id))

    return recMovieNames, recMoviePics, recMovieHomepage, recMovieInfo, recMovieRating

# Display header
sl.header("MovieMate")

# Loading embeddings of movie data and similarity scores
movies = pickle.load(open('movies.pkl', 'rb'))
similarities = pickle.load(open('similarity.pkl', 'rb'))

# Creating a dropdown list of movie titles
movieList = movies['title'].values

# Select box to enter or choose a movie to receive a recommendation
chosenMovie = sl.selectbox('Enter/choose a movie to receive five similar movies', movieList)

# Button to trigger the recommendation process
if sl.button('Go'):
    # Getting recommended movie names and their poster URLs
    recMovieNames, recMoviePics, recMovieHomepage, recMovieInfo, recMovieRating = recommendMovie(chosenMovie)
    
    # Displaying recommended movies and their posters in columns
    col1, col2, col3, col4, col5 = sl.columns(5)
    with col1:
        sl.text(recMovieNames[0])
        sl.image(recMoviePics[0])
        sl.text("Rating: " + str(recMovieRating[0]) + "/10")
        sl.markdown("[More info](%s)" % recMovieHomepage[0])
        sl.write(recMovieInfo[0], unsafe_allow_html=True)
    with col2:
        sl.text(recMovieNames[1])
        sl.image(recMoviePics[1])
        sl.text("Rating: " + str(recMovieRating[1]) + "/10")
        sl.markdown("[More info](%s)" % recMovieHomepage[1])
        sl.write(recMovieInfo[1], unsafe_allow_html=True)
    with col3:
        sl.text(recMovieNames[2])
        sl.image(recMoviePics[2])
        sl.text("Rating: " + str(recMovieRating[2]) + "/10")
        sl.markdown("[More info](%s)" % recMovieHomepage[2])
        sl.write(recMovieInfo[2], unsafe_allow_html=True)
    with col4:
        sl.text(recMovieNames[3])
        sl.image(recMoviePics[3])
        sl.text("Rating: " + str(recMovieRating[3]) + "/10")
        sl.markdown("[More info](%s)" % recMovieHomepage[3])
        sl.write(recMovieInfo[3], unsafe_allow_html=True)
    with col5:
        sl.text(recMovieNames[4])
        sl.image(recMoviePics[4])
        sl.text("Rating: " + str(recMovieRating[4]) + "/10")
        sl.markdown("[More info](%s)" % recMovieHomepage[4])
        sl.write(recMovieInfo[4], unsafe_allow_html=True)
