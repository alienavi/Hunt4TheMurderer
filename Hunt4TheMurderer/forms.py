from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    IntegerField,
    DateField,
    TextAreaField,
    HiddenField,
    SubmitField
)

from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp, Optional
import email_validator
from flask_login import current_user
from wtforms import ValidationError, validators
from .models import User

class login_form(FlaskForm) :
    username = StringField(validators=[
        InputRequired(message='Username is required'),
        Length(min=3, max=32, message='Username must be between 3 and 32 characters')
    ])
    password = PasswordField(validators=[
        InputRequired(message='Password is required'),
        Length(min=6, max=32, message='Password must be between 6 and 32 characters')
    ])
    remember = BooleanField('Remember me')

class register_form(FlaskForm) :
    username = StringField(
        validators=[
            InputRequired(),
            Length(3,8, message='Please enter your username'),
            Regexp(
                '^[A-Za-z][A-Za-z0-9_.]*$',
                0,
                'Username must only have letters, numbers, dots or underscores',
            )
        ]
    )
    password = PasswordField(validators=[InputRequired(), Length(8,16)])
    confirm_pwd = PasswordField(
        validators=[
            InputRequired(),
            Length(6,16),
            EqualTo('password', message='Passwords must match!')
        ]
    )
    admin = BooleanField(
        validators=[
            Optional(),
        ]
    )
    def validate_uname(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Username Already Exists!')

class delete_form(FlaskForm):
    user_id = HiddenField('User ID')
    delete_btn = SubmitField('Delete')