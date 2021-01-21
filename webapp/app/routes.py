from flask import render_template, flash, redirect, url_for, request, session
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Ratings, Animes
from flask import request, g
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, SearchForm, RatingForm
from app.email import send_password_reset_email
from app.seed import add_rating


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
        new_rating = form.rating.data
        if new_rating not in ['None', None]:
            r = Ratings(anime_name=anime.name, user_rating=new_rating, user_id=user_id)
            db.session.add(r)
            db.session.commit()
            return redirect(url_for('search'))
        elif new_rating in ['None', None]:
            ratings = Ratings.query.filter_by(anime_name=anime_name, user_id=user_id)
            if ratings:
                for rating in ratings:
                    db.session.delete(rating)
                    db.session.commit()
            return redirect(url_for('search'))


    return render_template('anime.html', anime=anime, form=form)