from flask import render_template, flash, redirect, url_for, request, session
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Ratings, Animes
from flask import request, g
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, RecommendationForm, ResetPasswordRequestForm, ResetPasswordForm, \
    SearchForm, RatingForm, ContactForm
from app.email import send_password_reset_email, send_contact_email
from app.predictions import predict_ratings
from sqlalchemy.sql import func



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

# Contact page
@app.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        subject = form.subject.data
        name = form.name.data
        email = form.email.data
        message = form.message.data
        send_contact_email(subject, name, email, message)
        return redirect(url_for('index'))
    return render_template('contact.html',
                           title='Contact Us', form=form)

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
    return render_template('search.html', form=form, title='Search')


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

    return render_template('anime.html', anime=anime, form=form, title=anime_name)


# Give anime recommendations to users
@app.route('/recommend', methods=['GET', 'POST'])
@login_required
def recommend():
    form = RecommendationForm(csrf=False)
    if form.validate_on_submit():
        user_id = current_user.id
        user_predictions = predict_ratings(user_id)
        return render_template('recommend.html', user_predictions=user_predictions, form=form)
    return render_template('recommend.html', form=form, title='Recommendations')

# User homepage
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    user_id = current_user.id
    top_rated = Animes.query.order_by(Animes.avg_rating.desc()).limit(10)
    most_popular = Animes.query.order_by(Animes.members.desc()).limit(10)
    user_favorites = Ratings.query.filter_by(user_id=user_id).order_by(Ratings.user_rating.desc()).limit(10)
    user_recents = Ratings.query.filter_by(user_id=user_id).order_by(Ratings.id.desc()).limit(10)
    user_rating_count = Ratings.query.filter_by(user_id=user_id).count()
    user_avg_rating = Ratings.query.with_entities(func.avg(Ratings.user_rating).label('average')).filter_by(
        user_id=user_id).all()[0][0]
    return render_template('dashboard.html', top_rated=top_rated, most_popular=most_popular,
                           user_favorites=user_favorites, user_recents=user_recents,
                           user_rating_count=user_rating_count, user_avg_rating=user_avg_rating, title='Dashboard')