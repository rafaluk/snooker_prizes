from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange
import pandas as pd


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class WelcomeScreenForm(FlaskForm):
    submit = SubmitField('Start')


class CreateDataForm(FlaskForm):
    submit = SubmitField('Create data')


class DetailsForm(FlaskForm):
    submit = SubmitField('Analyse data')


class ExampleForm(FlaskForm):
    df = pd.read_csv("app/static/dataframes/snooker_data.csv", sep=";", index_col=0)
    columns = df.columns
    del df
    col_list = [(x, x) for x in columns][:-1]
    variable = SelectField('Choose variable',
                           choices=col_list)
    bins = IntegerField('Bins number', default=30, validators=[NumberRange(10, 50)])
    normal_dist = BooleanField('Show line of normal distribution')
    submit = SubmitField('Generate plot')
