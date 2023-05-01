from flask import session, request
import pytest

from types import SimpleNamespace

from flask_app.forms import RegistrationForm
from flask_app.models import User


def test_register(client, auth):
    """ Test that registration page opens up """
    resp = client.get("/register")
    assert resp.status_code == 200

    response = auth.register()

    assert response.status_code == 200
    user = User.objects(username="test").first()

    assert user is not None


@pytest.mark.parametrize(
    ("username", "email", "password", "confirm", "message"),
    (
        ("test", "test@email.com", "test", "test", b"Username is taken"),
        ("p" * 41, "test@email.com", "test", "test", b"Field must be between 1 and 40"),
        ("username", "test", "test", "test", b"Invalid email address."),
        ("username", "test@email.com", "test", "test2", b"Field must be equal to"),
    ),
)
def test_register_validate_input(auth, username, email, password, confirm, message):
    if message == b"Username is taken":
        auth.register()

    response = auth.register(username, email, password, confirm)

    assert message in response.data


def test_login(client, auth):
    """ Test that login page opens up """
    resp = client.get("/login")
    assert resp.status_code == 200

    auth.register()
    response = auth.login()

    with client:
        client.get("/")
        assert session["_user_id"] == "test"

# 1. Done
@pytest.mark.parametrize(
    ("username", "password", "message"), 
    (
        ("", "", "This field is required"),
        ("", "password", "This field is required"),
        ("username", "", "This field is required"),
        ("badusername", "password", "Login failed. Check your username and/or password"),
        ("goodusername", "badpassword", "Login failed. Check your username and/or password")
    )
)
# 1. Done
def test_login_input_validation(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data.decode('utf-8')

# 2. Done
def test_logout(client, auth):
    # Register
    auth.register()
    
    # Login
    auth.login()
    
    # Check that user is logged in
    response = client.get('/account')
    assert b'Click here to see all of your posts and comments!' in response.data
    
    # Log out
    auth.logout()
    
    # Check that we're logged out
    response = client.get('/')
    assert b"Please use the search bar to search for movies!" in response.data 

# 3. WORKKKKK
def test_change_username(client, auth):
    # Register and login a test user
    auth.register()
    auth.login()

    # Make sure the account page loads successfully
    resp = client.get("/account")
    assert resp.status_code == 200

    # Change the username of the logged-in user
    new_username = "new_username"
    resp = client.post("/account", data={"username": new_username})
    assert resp.status_code == 302

    # Login back new user
    auth.login(username=new_username)

    # Follow the redirect to the account page
    resp = client.get("/account")
    assert resp.status_code == 200

    # Check that the new username shows up on the account page
    assert new_username.encode() in resp.data

    # Check that the new username change is reflected in the database
    user = User.objects(username=new_username).first()
    assert user is not None

# 4. WORK
def test_change_username_taken(client, auth):
    # Register two users (differnet username, same password, and same other fields)
    auth.register("user1", "user1@example.com", "password", "password")
    auth.register("user2", "user2@example.com", "password", "password")

    # Log in as the first user
    auth.login("user1", "password")

    # Attempt to change the username to the second user's username
    response = client.post("/account", data={"username": "user2"})

    # Check that we get an error message
    assert b"That username is already taken" in response.data

    # Assert that the username did not actually change
    user = User.objects(username="user1").first()
    assert user.username == "user1"




# 5. Done
@pytest.mark.parametrize(
    ("new_username",), 
    (
        ("",),  # Test empty string input
        ("a" * 41,),  # Test input string longer than 40 characters
    )
)
# 5. Done
def test_change_username_input_validation(client, auth, new_username):
    # Register tets user
    auth.register()

    # Login with test user
    auth.login()

    # Attempt to change the username
    if len(new_username) > 0:
        resp = client.post("/account", data={"username": new_username})
        assert b'Field must be between 1 and 40 characters long' in resp.data
    
    else: # Attempt to change username with empty string
        resp = client.post("/account", data={"username": new_username})
        assert b'This field is required' in resp.data