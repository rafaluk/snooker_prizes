from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import numpy as np
import matplotlib.pyplot as plt


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class WelcomeScreenForm(FlaskForm):
    submit = SubmitField('Start')


class CreateDataForm(FlaskForm):
    submit = SubmitField('Create data')

    @staticmethod
    def generate_plot():
        x = np.arange(1, 100, 10)
        y = np.random.rand(10)
        plt.plot(x, y)
        plt.savefig('static/images/wykres.png')
        return