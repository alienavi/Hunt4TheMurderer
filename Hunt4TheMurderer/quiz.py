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

class quiz_form(FlaskForm, ):
    question = 'Question'
    input_field = 'Input'
    answer = HiddenField()