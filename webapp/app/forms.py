from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from flask import request


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')    

class SearchForm(FlaskForm):
    search = StringField('Search by Anime Name', validators=[DataRequired()])
    submit = SubmitField('Search')
    # def __init__(self, *args, **kwargs):
    #     if 'formdata' not in kwargs:
    #         kwargs['formdata'] = request.args
    #     if 'csrf_enabled' not in kwargs:
    #         kwargs['csrf_enabled'] = False
    #     super(SearchForm, self).__init__(*args, **kwargs)

class RatingForm(FlaskForm):
    choices = [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    rating = SelectField("Rate it!", choices = choices, validators=[DataRequired()])
    submit = SubmitField('Submit')
