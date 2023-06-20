from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    IntegerField,
    DateField,
    TextAreaField
)

from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp, Optional
import email_validator
from flask_login import current_user
from wtforms import ValidationError, validators
from .models import User

class login_form(FlaskForm) :
    username = StringField(validators=[InputRequired(), Length(3,8)])
    password = PasswordField(validators=[InputRequired(), Length(8, 16)])
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
            Length(8,16),
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