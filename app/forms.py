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


class HistogramForm(FlaskForm):
    df = pd.read_csv("app/static/dataframes/snooker_data.csv", sep=";", index_col=0)
    columns = df.columns
    del df
    col_list = [(x, x) for x in columns][:-1]
    variable = SelectField('Choose variable', choices=col_list)
    bins = IntegerField('Bins number', default=30, validators=[NumberRange(10, 50)])
    normal_dist = BooleanField('Show line of normal distribution')
    submit = SubmitField('Generate plot')


class HistogramForm2(FlaskForm):
    submit = SubmitField('Next')


class ModelForm(FlaskForm):
    choices = [('randomForest', 'Random Forest'),
               ('knn', 'K Nearest Neighbors'),
               ('linearRegression', 'LinearRegression')]
    models = SelectField('Choose variable', choices=choices)
    submit = SubmitField('Next')

# n_estimators = number of trees in the foreset
# max_features = max number of features considered for splitting a node
# max_depth = max number of levels in each decision tree
# min_samples_split = min number of data points placed in a node before the node is split
# min_samples_leaf = min number of data points allowed in a leaf node
# bootstrap = method for sampling data points (with or without replacement)

class RandomForestForm(FlaskForm):
    n_estimators = IntegerField(default=30, validators=[NumberRange(10, 50)])
    max_features = IntegerField()
    max_depth = IntegerField()
    min_samples_split = IntegerField()
    min_samples_leaf = IntegerField()
    bootstrap = BooleanField("Include bootstrap?") # check if default=True works

    submit = SubmitField('Next')


class TrainForm(FlaskForm):

    submit = SubmitField('Next')
