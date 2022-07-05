from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, DateField, SubmitField
from wtforms.validators import DataRequired


class Register(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    re_password = PasswordField('Repeat Your Password', validators=[DataRequired()])


class Login(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

