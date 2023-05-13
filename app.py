from flask import Flask, render_template, request, redirect, url_for
import pickle
import pandas as pd

app = Flask(__name__)

# Load pickled movie list and similarity matrix
movie_list = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get movie title entered by user from form
    movie_title = request.form['movie']

    # Get index of movie in movie_list
    movie_index = movie_list[movie_list['title'] == movie_title].index

    if len(movie_index) == 0:
        # Movie not found
        return redirect(url_for('not_found'))

    movie_index = movie_index[0]

    # Get indices and similarity scores of 5 most similar movies
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])
    top_indices = [i[0] for i in distances[1:6]]
    top_scores = [i[1] for i in distances[1:6]]

    # Get titles and overviews of recommended movies
    top_movies = movie_list.iloc[top_indices][['title', 'tags']].values.tolist()

    # Pass recommended movies and scores to template
    return render_template('recommend.html', movie=movie_title, top_movies=top_movies, scores=top_scores)

@app.route('/not-found')
def not_found():
    return render_template('not_found.html')

if __name__ == '__main__':
    app.run(debug=True)
