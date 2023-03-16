# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo

# stdlib
import os
from datetime import datetime

# local
from flask_app.forms import SearchForm, MovieReviewForm
from flask_app.model import MovieClient

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/mydatabase"
app.config['SECRET_KEY'] = "b'\xddgY\xe3\xb4^P?IW\xb7u\xf8L\xd6\x95'"

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

mongo = PyMongo(app)

client = MovieClient(os.environ.get('OMDB_API_KEY'))

# --- Do not modify this function ---
@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for('query_results', query=form.search_query.data))

    return render_template('index.html', form=form)

@app.route('/search-results/<query>', methods=['GET'])
def query_results(query):
    client = MovieClient(os.environ.get('OMDB_API_KEY'))
    results = client.search(query)
    message = None
    if results is None:
        return render_template('query_results.html', error_msg=message)
    return render_template('query_results.html', results=results)
    

@app.route('/movies/<movie_id>', methods=['GET', 'POST'])
def movie_detail(movie_id):
    movie_client = MovieClient(os.environ.get('OMDB_API_KEY'))
    
    try:
        movie = movie_client.retrieve_movie_by_id(movie_id)
    except Exception as e:
        return render_template('movie_detail.html', error_msg=str(e))

    #reviews = list(mongo.db.reviews.find({'imdb_id': movie.imdb_id}))

    form = MovieReviewForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            commenter = form.name.data
            content = form.text.data
            date = current_time()
            imdb_id = movie.imdb_id



            # New document is created inside
            new_review = {
                'imdb_id':imdb_id,
                'commenter':commenter,
                'content':content,
                'date':date
                }
            

            # Create document for our collection "reviews", then insert data into our database
            mongo.db.reviews.insert_one(new_review)
            return redirect(url_for('movie_detail', movie_id=movie.imdb_id))
        else:
            print('validation failed')
    # Retrieve 'reviews' from db and display it on movie_detail.html
    reviews = list(mongo.db.reviews.find({'imdb_id': movie.imdb_id}))
    return render_template('movie_detail.html', movie=movie, reviews=reviews, form=form)           

# Not a view function, used for creating a string for the current time.
def current_time() -> str:
    return datetime.now().strftime('%B %d, %Y at %H:%M:%S')