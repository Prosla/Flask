from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, InputRequired

class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[InputRequired(), Length(min=4, max=15)]
    )
    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min=8, max=80)]
    )
    remember = BooleanField('Remember me')

class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[InputRequired(), Length(min=4, max=15)]
    )
    email = EmailField(
        'Email',
        validators=[DataRequired(), Length(max=50)]
    )
    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min=8, max=80)]
    )


class GenerateDataForm(FlaskForm):
    submit = SubmitField('Generate')


class NameForm(FlaskForm):
    name = StringField(
        'What is your name?',
        validators=[DataRequired(), Length(3, 100)],
        render_kw={'placeholder': 'Full name'}
    )
    email = EmailField(
        'What is your email?',
        validators=[DataRequired(), Length(10, 150)],
        render_kw={'placeholder': 'Email'}
    )
    submit = SubmitField('Add')
