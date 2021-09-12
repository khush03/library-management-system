from flask_wtf import Form, FlaskForm

from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from flask_wtf.html5 import URLField
from wtforms.validators import DataRequired, url, Length, Email, EqualTo, Regexp, ValidationError
import models


class LoginForm(Form):
    username = StringField('Your Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3, 80),
                                                   Regexp('^[A-Za-z0-9_]{3,}$',
                                                          message='Username consist of numbers,letters and underscores.')])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Length(1, 120), Email()])
    contact = StringField('Contact', validators=[DataRequired(), Length(1, 10)])
    address = StringField('Address', validators=[DataRequired()])

    def validate_email(self, email_field):
        if models.User.query.filter_by(email=email_field.data).first():
            raise ValidationError('Email id already exists!!')

    def validate_username(self, username_field):
        if models.User.query.filter_by(username=username_field.data).first():
            raise ValidationError('Username already exists!!')
