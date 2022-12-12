from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, ValidationError, length, equal_to, Email

from wizapp.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), length(max=20, min=2)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_Password', validators=[DataRequired(), equal_to('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exits, please choose a different username!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exits, please choose a different email!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(" There's no account with this email. Please register.")


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), length(min=5, max=20)])
    confirm_password = PasswordField('confirm Password', validators=[DataRequired(), equal_to('password')])
    submit = SubmitField('Reset Password')
