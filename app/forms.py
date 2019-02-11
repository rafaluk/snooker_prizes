from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange
import pandas as pd


class WelcomeScreenForm(FlaskForm):
    submit = SubmitField('Start')


class CreateDataForm(FlaskForm):

    choices_since = [("2014", "2014"), ("2015", "2015"),
                     ("2016", "2016"), ("2017", "2017")]
    choices_to = [("2018", "2018")]

    seasons_since = SelectField(label="Since", choices=choices_since)
    seasons_to = SelectField(label="To", choices=choices_to)

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


class RandomForestForm(FlaskForm):
    features_list = [('auto', 'auto'), ('sqrt', 'sqrt')]
    split_list = [("2", "2"), ("5", "5"), ("10", "10")]
    leaf_list = [("1", "1"), ("2", "2"), ("4", "4")]
    train_split_list = [("15", "15%"), ("25", "25%"), ("35", "35%")]

    train_split = SelectField(
        label="Train split: what part of data will be used for training",
        choices=train_split_list)

    n_estimators = IntegerField(
        label="Estimators: number of trees in the forest",
        default=30, validators=[NumberRange(10, 50)])

    max_features = SelectField(
        label="Max features:  max number of features considered for splitting a node",
        choices=features_list)

    max_depth = IntegerField(
        label="Max depth max number of levels in each decision tree",
        validators=[NumberRange(10, 50)], default=20)

    min_samples_split = SelectField(
        label="Min samples split: min number of data points placed in a node before the node is split",
        choices=split_list, validators=None)

    min_samples_leaf = SelectField(
        label="Min samples leaf: min number of data points allowed in a leaf node",
        choices=leaf_list, validators=None)

    bootstrap = BooleanField(
        label="Bootstrap: method for sampling data points (with or without replacement)") # check if default=True works

    my_parameters = SubmitField('Proceed with my parameters')


class RandomForestForm2(FlaskForm):
    random_parameters = SubmitField("I want to choose the parameters randomly by an algorithm")
