from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username', validators=[
            DataRequired(), Length(min=2, max=20)
        ]
    )

    email = StringField(
        'Email', validators=[
            DataRequired(), Email()
        ]
    )

    address = StringField(
        'Address', validators=[
            DataRequired()
        ]
    )

    phone = StringField(
        'Phone number', validators=[
            DataRequired()
        ]
    )

    password = PasswordField(
        'Password', validators=[
            DataRequired()
        ]
    )

    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField(
        'Email', validators=[
            DataRequired(), Email()
        ]
    )

    password = PasswordField(
        'Password', validators=[
            DataRequired()
        ]
    )

    submit = SubmitField('Login')


class ProductForm(FlaskForm):
    title = StringField(
        'Title', validators=[
            DataRequired()
        ]
    )

    content = TextAreaField(
        'Content', validators=[
            DataRequired()
        ]
    )

    price = StringField(
        'Price', validators=[
            DataRequired()
        ]
    )

    submit = SubmitField('Submit product')