from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
import requests
from imdb import Cinemagoer
from random import sample
from main import app, db
from main.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, SearchForm
from main.models import User, Movie
from main.email import send_password_reset_email


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    movie_list = {}
    ia = Cinemagoer()
    top_250_movies = ia.get_top250_movies()
    random_10_movies = sample(top_250_movies, 10)
    for movie in random_10_movies:
        api_url = 'http://www.omdbapi.com/?apikey=b49eb448&t={}'.format(movie)
        try:
            response = requests.get(api_url)
            if response.status_code == requests.codes.ok:
                title = response.json()["Title"]
                year = response.json()["Year"]
                type = response.json()["Type"]
                poster = response.json()["Poster"]
                movie_list.update({title: [year, type, poster]})
            else:
                print("Error:", response.status_code, response.text)
        except ConnectionError as e:
            print("No internet connection!")
    return render_template('index.html', title='Home', movies=movie_list)


# PASS STUFF TO NAVBAR
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@app.route('/search', methods=['POST', 'GET'])
def search():
    page = request.args.get('page', 1, type=int)
    form = SearchForm()
    if form.validate_on_submit():
        movie_list = {}
        searched = form.searched.data
        search_api_url = 'http://www.omdbapi.com/?apikey=b49eb448&s={}&page={}'.format(searched, page)

        try:
            response = requests.get(search_api_url)
            if response.status_code == requests.codes.ok:
                data = response.json()['Search']
                for movie in data:
                    title = movie['Title']
                    year = movie['Year']
                    poster = movie['Poster']
                    type = movie['Type']
                    movie_list.update({title: [year, type, poster]})
            else:
                print("Error:", response.status_code, response.text)
        except ConnectionError as e:
            print("No internet connection!")
        except KeyError:
            print(f"Movie {searched} doesn't exit!")

        return render_template('search.html',
                               form=form, searched=searched,
                               title='Search', movies=movie_list)


@login_required
@app.route('/collection', methods=['GET'])
def collection():
    movie_dict = []
    movie_list = {}
    movies = Movie.query.filter_by(add_user=current_user).all()
    for movie in movies:
        movie_dict.append(movie.title)
    for movie in movie_dict:
        api_url = 'http://www.omdbapi.com/?apikey=b49eb448&t={}'.format(movie)
        try:
            response = requests.get(api_url)
            if response.status_code == requests.codes.ok:
                title = response.json()["Title"]
                year = response.json()["Year"]
                type = response.json()["Type"]
                poster = response.json()["Poster"]
                movie_list.update({title: [year, type, poster]})
            else:
                print("Error:", response.status_code, response.text)
        except ConnectionError as e:
            print("No internet connection!")
    return render_template('collection.html', title='Collection', movies=movie_list)


@login_required
@app.route('/add/<title>', methods=['POST'])
def add(title):
    user = current_user
    movie = Movie.query.filter_by(title=title).first()
    if movie:
        return jsonify({'error': 'Movie already exists in the collection.'}), 400
    movie = Movie(title=title, add_user=user)
    db.session.add(movie)
    db.session.commit()
    flash('Movie add successfully!')
    return redirect(url_for('index'))


# SIGN UP, SIGN IN AND PASSWORD RESET -> (START)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data))
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

# SIGN UP, SIGN IN AND PASSWORD RESET -> (END)
