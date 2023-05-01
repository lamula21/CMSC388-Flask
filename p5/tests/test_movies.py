import pytest

from types import SimpleNamespace
import random
import string

from flask_app.forms import SearchForm, MovieReviewForm
from flask_app.models import User, Review


def test_index(client):
    resp = client.get("/")
    assert resp.status_code == 200

    search = SimpleNamespace(search_query="guardians", submit="Search")
    form = SearchForm(formdata=None, obj=search)
    response = client.post("/", data=form.data, follow_redirects=True)

    assert b"Guardians of the Galaxy" in response.data


# 1. DONE
@pytest.mark.parametrize(
    ("query", "message"), 
    (
        ("", b"This field is required."),
        ("a", b"Too many results"),
        ("".join(random.choices(string.ascii_letters + string.digits, k=50)), b"Movie not found"),
        ("".join(random.choices(string.ascii_letters + string.digits, k=150)), b"Field must be between 1 and 100 characters long."),
    )
)
# 1. Done
def test_search_input_validation(client, query, message):
    form = SearchForm(search_query=query)
    response = client.post("/", data=form.data, follow_redirects=True)
    assert message in response.data

# 2. Done
def test_movie_review(client, auth):
    # choose a random movie id to review
    movie_id = "tt1234567"
    
    # register and login
    auth.register()
    auth.login()
    
    # generate a random review content
    review_content = ''.join(random.choices(string.ascii_letters, k=50))
    
    # submit a movie review
    url = f"/movies/{movie_id}"
    response = client.post(url, data={
        'text': review_content,
        'submit': 'Submit'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    # check that the review shows up on the page
    assert review_content.encode() in response.data
    
    # check that the review is saved in the database
    review = Review.objects(content=review_content).first()
    assert review is not None
    assert review.imdb_id == movie_id



# 3. Done
@pytest.mark.parametrize(
    ("movie_id", "message"), 
    (
        ("", "404 - Page Not Found"),
        ("tt99999", "Incorrect IMDb ID"),
        ("tt9999999", "Error getting data."),
        ("tt99999999", "Incorrect IMDb ID"),
    )
)
# 3. Done
def test_movie_review_redirects(client, movie_id, message):
    if movie_id == "":
        # Test for empty movie_id
        response = client.get(f"/movies/{movie_id}")
        assert response.status_code == 404
        assert message.encode() in response.data
    else:
        # Test for invalid movie_id
        response = client.get(f"/movies/{movie_id}")
        assert response.status_code == 302
        response = client.get("/")
        assert message.encode() in response.data

    # url = f"/movies/{movie_id}"
    # response = client.get(url)

    # if len(movie_id) == 0:
    #     assert response.status_code == 404
    #     assert message.encode() in response.data
    # else:
    #     assert response.status_code == 302
    #     print(response.data)
    #     assert b"Incorrect IMDb ID" in response.data


# 4. Done
@pytest.mark.parametrize(
    ("comment", "message"), 
    (
        ('', "This field is required"),
        ('a' * 4, "Field must be between 5 and 500 characters long"),
        ('a' * 501, "Field must be between 5 and 500 characters long")
    )
)
# 4. Done
def test_movie_review_input_validation(client, auth, comment, message):
    # Register user
    auth.register()

    # Log in the user
    auth.login()

    # Test empty comment
    response = client.post('/movies/tt2015381', data={
        'text': comment, 'submit' : 'Submit'
    }, follow_redirects=True)

    assert message.encode() in response.data

