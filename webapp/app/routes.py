from flask import render_template, flash, redirect, url_for, request, session
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Ratings, Animes
from flask import request, g
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, SearchForm, RatingForm
from app.email import send_password_reset_email
import pandas as pd
import numpy as np
from surprise import Dataset, Reader, SVD, dump


# Index (Home Page)
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Log In', form=form)


# Logout
@app.route('/logout')
def logout():
    logout_user()
    return render_template('logout.html')


# Register
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


# Request a password reset email
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


# Reset password
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


# Search
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm(csrf=False)
    if form.validate_on_submit():
        search_term = form.search.data
        query, total = Animes.search(search_term, 1, 10)
        results = query.all()
        user_id = current_user.id
        for i in results:
            anime_name = i.name
            rating = Ratings.query.filter_by(anime_name=anime_name, user_id=user_id).order_by(Ratings.id.desc()).first()
            if rating:
                i.user_rating = rating.user_rating
            else:
                i.user_rating = None
        return render_template('search.html', search_term=search_term, form=form, results=results)
    return render_template('search.html', form=form)


# Rating page for each anime
@app.route('/<anime_name>', methods=['GET', 'POST'])
@login_required
def display_anime(anime_name):
    anime = Animes.query.filter_by(name=anime_name).first()
    user_id = current_user.id
    form = RatingForm(csrf=False)

    if form.validate_on_submit():
        new_rating = form.rating.data  # New rating
        # Upon submission, delete older ratings for the anime
        prev_ratings = Ratings.query.filter_by(anime_name=anime_name, user_id=user_id)
        if prev_ratings:
            for rating in prev_ratings:
                db.session.delete(rating)
                db.session.commit()
        if new_rating not in ['None', None]:
            r = Ratings(anime_id=anime.id, anime_name=anime.name, user_rating=new_rating, user_id=user_id)
            db.session.add(r)
            db.session.commit()
        return redirect(url_for('search'))

    return render_template('anime.html', anime=anime, form=form)


# Give anime recommendations to users
@app.route('/recommend', methods=['GET', 'POST'])
@login_required
def recommend():
    model_path = 'app/algo/svd_model'
    anime_ids_path = 'app/data/clean_data/anime_ids.csv'

    # Load trained model
    _, algo = dump.load(model_path)

    # Read in user rating data
    reader = Reader(rating_scale=(1, 10))

    # Create a dataframe of user's ratings
    user_id = current_user.id
    query = Ratings.query.filter_by(user_id=user_id).all()
    ratings = [[user_id, i.anime_id, i.user_rating] for i in query]
    rating_df = pd.DataFrame(ratings, columns=['user_id', 'anime_id', 'rating'])

    # Identify the animes the user has not seen yet
    anime_df = pd.read_csv(anime_ids_path)
    anime_ids = anime_df['id'].to_numpy()
    animes_rated_by_user = rating_df['anime_id'].values
    animes_to_predict = np.setdiff1d(anime_ids, animes_rated_by_user)
    name_id_key = dict(anime_df.values)

    # Create user testset and predict
    user_testset = [[user_id, anime_id, None] for anime_id in animes_to_predict]
    predictions = algo.test(user_testset)
    pred_ratings = np.array([pred.est for pred in predictions])

    user_predictions = pd.DataFrame((zip(animes_to_predict, pred_ratings*10)), columns=['anime_id', 'match'])
    user_predictions = user_predictions.sort_values('match', ascending=False).iloc[:20]
    user_predictions['anime_name'] = user_predictions['anime_id'].apply(lambda x: name_id_key.get(x))
    user_predictions['match'] = user_predictions['match'].apply(lambda x: round(x, 1))
    user_predictions = user_predictions.to_dict(orient='records')

    return render_template('recommend.html', user_predictions=user_predictions)
