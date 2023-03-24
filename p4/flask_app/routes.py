# 3rd-party packages
from flask import render_template, request, redirect, url_for, flash
from flask_login import ( # provides current_user
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask import session

# encode images
import io 
import base64

from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
from datetime import datetime

# local
from . import app, bcrypt, client
from .forms import (
    SearchForm,
    MovieReviewForm,
    RegistrationForm,
    LoginForm,
    UpdateUsernameForm,
    UpdateProfilePicForm,
    DarkModeForm,
    UpdatePasswordForm
)
from .models import User, Review, load_user
from .utils import current_time

""" ************ View functions ************ """


@app.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("query_results", query=form.search_query.data))

    return render_template("index.html", form=form)


@app.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = client.search(query)
    except:
        str = '''Ups! The movie you're looking for is not found!'''
        return render_template("query.html", error_msg=str)

    return render_template("query.html", results=results, enum=enumerate(results))


@app.route("/movies/<movie_id>", methods=["GET", "POST"])
def movie_detail(movie_id):
    try:
        result = client.retrieve_movie_by_id(movie_id)
    except ValueError as e:
        return render_template("movie_detail.html", error_msg=str(e))

    form = MovieReviewForm()
    if form.validate_on_submit():
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            imdb_id=movie_id,
            movie_title=result.title,
        )
        review.save()
        return redirect(request.path)

    reviews = Review.objects(imdb_id=movie_id)

    return render_template(
        "movie_detail.html", form=form, movie=result, reviews=reviews
    )

# DONE
@app.route("/user/<username>")
def user_detail(username):
    # grab user by finding username in the db
    user = User.objects(username=username).first()

    # if found, pull reviews from this username and pass to the rendertemplate
    if user is not None:
        movies = list()
        user_review = Review.objects(commenter=user)
        image = get_b64_img(username)

        for each in user_review:
            movie = client.retrieve_movie_by_id(each.imdb_id)
            movies.append(movie)

    # if username not found, handle error and pass into rendertemplate
    else:
        error_msg = f'The user "{username}" does not exist'
        return render_template('user_detail.html', error_msg=error_msg)
    return render_template('user_detail.html', username=username, user_review=user_review, image=image, movies_reviews=zip(movies,user_review))

#DONE
@app.errorhandler(404)# Add decorator
def custom_404(e):
    return render_template('404.html'), 404


""" ************ User Management views ************ """

#DONE
@app.route("/register", methods=["GET", "POST"])
def register():

    # if user is auth, redirect to main page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # otherwise, proceed with registration form
    form = RegistrationForm()

    # if registeration form is submitted and validated
    if form.validate_on_submit():

        # Hash password for security
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Create new User object (document) for our collection "User"s
        user = User(
            username=form.username.data, 
            email=form.email.data,
            password=hashed
            )
        
        
        # Set default image
        # Open the default image file
        with open('./flask_app/static/default.jpg', 'rb') as imagefile:
            # Read the contents of the file
            content = io.BytesIO(imagefile.read())
            filename = 'default.jpg'
            content_type = 'image/jpeg'
            user.profile_pic.put(content, content_type=content_type, filename=filename)

        # save user into db
        user.save()

        # redirect user to login route
        return redirect(url_for('login'))
        
    # Render the register.html page
    return render_template('register.html', title='Register', form=form)

#DONE
@app.route("/login", methods=["GET", "POST"])
def login():
    # if user is auth, redirect to main page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # otherwise, proceed with login form
    form = LoginForm()
    # if login form is submitted and validated
    if form.validate_on_submit():
        # find appropiate user in db
        user = User.objects(username=form.username.data).first()

        # if user exists and hash-password matches
        if (user is not None and bcrypt.check_password_hash(user.password, form.password.data)):
            # make user auth and
            login_user(user)

            flash('You are logged-in', 'success')
            flash('Try New Dark Mode Theme 🌚', 'primary')
            # redirect to his account
            return redirect(url_for('account'))
        # otherwise prompt flash message
        flash('Please Log-in again', 'warning')
        return redirect(url_for('login'))

    # Render the login.html page
    # user no auth, not found or password no match, redirect to login page again to enter login form again
    return render_template('login.html', tittle='Login', form=form)


# DONE
@app.route("/logout")
@login_required # logged-in user access only
def logout():
    logout_user() # logout current user
    return redirect(url_for('index'))


#DONE
@app.route("/account", methods=["GET", "POST"])
@login_required # logged-in user access only
def account():
    
    # get user from this session
    user_object = User.objects(username=current_user.username).first()

    # See how it is done in movie_detail.html
    updatePicForm = UpdateProfilePicForm()
    updateNameForm = UpdateUsernameForm()
    updatePassForm = UpdatePasswordForm()

    # get user avatar  
    user_avatar = get_b64_img(current_user.username)

    # Update Avatar
    if updatePicForm.validate_on_submit():
        # Check file security and file extension
        img = updatePicForm.picture.data
        filename = secure_filename(img.filename)
        content_type = f'images/{filename[-3:]}'

        # if current_user doesnt have pic, place one and save 
        if current_user.profile_pic.get() is None:
            current_user.profile_pic.put(img.stream, content_type=content_type)
        # if current_user already has pic, replace one and save
        else:
            current_user.profile_pic.replace(img.stream, content_type=content_type)
        
        # save user into db
        current_user.save()
        flash('Your avatar has been updated successfully!', 'success')
        return redirect(url_for('account'))

    # Update Name 
    elif updateNameForm.validate_on_submit():
        # if user doesnt exist with username in db, then modify username
        if User.objects(username=updateNameForm.username.data).first() is None: 
            user_object.modify(username=updateNameForm.username.data)
            user_object.save() # save modify user into db
            flash('Your username has been updated successfully!', 'success')
            return redirect(url_for('account'))
        else:
            flash('User already exists!', 'danger')
            return redirect(url_for('account'))
    
    # Update Password
    elif updatePassForm.validate_on_submit():

        # Hash password before changing in db
        hashed = bcrypt.generate_password_hash(updatePassForm.new_password.data).decode('utf-8')

        user_object.modify(password=hashed)
        user_object.save()

        flash('Password has been updated succesfully', 'success')
        return redirect(url_for('account'))

    return render_template(
        "account.html", 
        picform=updatePicForm,
        nameform=updateNameForm,
        passform=updatePassForm,
        image=user_avatar
    )

# encode and decode image
def get_b64_img(username):
    user= User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image


@app.route('/dark-mode', methods=['POST'])
@login_required
def dark_mode():
    user = User.objects(username=current_user.username).first()
    user.modify(dark_mode= not user.dark_mode)
    user.save()
    return redirect(request.referrer) # redirect user tp the page perviously on


# all templates has access to dark_mode_form
@app.context_processor
def inject_forms():
    dark_mode_form = DarkModeForm()
    return dict(dark_mode_form=dark_mode_form)

