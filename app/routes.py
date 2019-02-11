from flask import render_template, redirect, url_for, flash, session

from app import app
from app.forms import WelcomeScreenForm, CreateDataForm, DetailsForm, HistogramForm, \
    HistogramForm2, RandomForestForm, RandomForestForm2
from .static.utils import Utils
import pandas as pd
from plot_gen import PlotGenerator
from .modelling.model_generator import ModelGenerator
import numpy as np

df = pd.DataFrame()
model_name = ""
seasons = []



@app.route('/')
def nothing():
    return redirect(url_for('index'))


@app.route('/blog')
def blog():
    return render_template('blog.html', title="Blog")


@app.route('/index', methods=['GET', 'POST'])
def index():
    form = WelcomeScreenForm()
    if form.validate_on_submit():
        return redirect(url_for('create'))

    return render_template('index.html', title='Start', form=form)


@app.route('/create', methods=['GET', 'POST'])
def create():
    form = CreateDataForm()
    if form.validate_on_submit():
        try:
            since = form.seasons_since.data
            to = form.seasons_to.data
            seasons_data = Utils.convert_seasons(since=since, to=to)
            # TEN KOMENTARZ JEST TYLKO PO TO, ZEBY SZYBKO DZIALALO! DOCELOWQ DO ODKOMENTOWANIA!!!!
            Utils.get_snooker_data(seasons=seasons_data)
            return redirect(url_for('details'))
        except:
            flash("Download failed :( Refresh this website and try again.")
            print("Download failed.")

    return render_template('create.html', title="Create data",
                           form=form, url='static/images/histogram.png')


@app.route('/details', methods=['GET', 'POST'])
def details():
    form = DetailsForm()
    global df
    df = pd.read_csv("app/static/dataframes/snooker_data.csv", sep=";")
    df = df.set_index(df['Name'], drop=True)
    df = df.drop('Name', axis=1)
    df = df.replace(np.nan, 0)
    print(df.head())
    columns = df.columns
    col_count = len(columns)
    row_count = df.shape[0]

    # to trzeba przekazac z create, a nie tak wpisywac statycznie
    seasons = ['2015-2016', '2016-2017', '2017-2018']

    if form.validate_on_submit():
        return redirect(url_for('analyse'))

    return render_template('details.html', title="Details", form=form, columns=columns, df=df,
                           col_count=col_count, row_count=row_count, seasons=seasons)


@app.route('/analyse', methods=['GET', 'POST'])
def analyse():
    form = HistogramForm()
    form2 = HistogramForm2()
    global df

    path = "app/static/images/histogram.png"
    Utils().delete_file(path)
    print("Image deleted: " + path)
    is_file = False

    if form.validate_on_submit():
        try:
            column = form.variable.data
            bins = int(form.bins.data)
            normal_dist = form.normal_dist.data

            if form.bins.validate(form) is not True:
                flash('Wrong bin value. Enter value between 10 and 50.')
                return redirect(url_for('analyse'))
            gen = PlotGenerator(df[column], title=str(column))
            gen.plot_and_save_hist(bins, normal_dist=normal_dist)
            is_file = True
            return render_template('analyse.html', title="Analysis", form=form, form2=form2,
                                   url='static/images/histogram.png', is_file=is_file)
        except:
            flash('Something went completely wrong! :( Start again.')
            return redirect(url_for('analyse'))

    # TODO second button - the same form (not form2 like it's now)
    if form2.validate_on_submit():
        return redirect(url_for('random_forest_parameters'))

    return render_template('analyse.html', title="Analysis", form=form, form2=form2, is_file=is_file)


# @app.route('/model', methods=['GET', 'POST'])
# def model():
#     form = ModelForm()
#     global model_name
#
#     if form.validate_on_submit():
#         model_name = form.models.data
#         # CHANGE URL_FOR TO SPECIFIC SUBPAGES
#         if model_name == "randomForest":
#             return redirect(url_for('random_forest_parameters'))
#         elif model_name == "knn":
#             return redirect(url_for('train'))
#         elif model_name == "linearRegression":
#             return redirect(url_for('train'))
#
#     return render_template('model.html', title="Choose model", form=form)


@app.route('/randomForestParameters', methods=['GET', 'POST'])
def random_forest_parameters():
    form = RandomForestForm()
    form2 = RandomForestForm2()

    if form.validate_on_submit():
        session['params'] = "own"
        session['split'] = form.train_split.data
        session['n_estimators'] = form.n_estimators.data
        session['max_features'] = form.max_features.data
        session['max_depth'] = form.max_depth.data
        session['min_samples_split'] = form.min_samples_split.data
        session['min_samples_leaf'] = form.min_samples_leaf.data
        session['bootstrap'] = form.bootstrap.data
        return redirect(url_for('random_forest_scores'))

    if form2.validate_on_submit():
        session['params'] = "random"
        return redirect(url_for('random_forest_scores'))

    return render_template('models/randomForestParameters.html', title="Random Forest",
                           form=form, form2=form2)


@app.route('/randomForestScores', methods=['GET', 'POST'])
def random_forest_scores():
    global df
    path = "/static/images/predictions.png"
    hej = Utils().delete_file(path)
    print("HEEEEEEEEEJ: " + str(hej))
    is_file = False
    rf = ModelGenerator(df=df)
    imp = []
    if session.get('params', None) == "own":
        split = session.get('split', None)
        n_estimators = int(session.get('n_estimators', None))
        max_features = session.get('max_features', None)
        max_depth = int(session.get('max_depth', None))
        min_samples_split = int(session.get('min_samples_split', None))
        min_samples_leaf = int(session.get('min_samples_leaf', None))
        bootstrap = bool(session.get('bootstrap', None))

        rf_results = rf.perform_rf_own_params(split=split, n_estimators=n_estimators,
                                              max_features=max_features, max_depth=max_depth,
                                              min_samples_split=min_samples_split,
                                              min_samples_leaf=min_samples_leaf, bootstrap=bootstrap)
        imp = rf.get_importances()

    else:
        rf_results = rf.perform_rf_with_random_params()

    rf.create_graphs()
    is_file = True
    print(app.root_path)

    return render_template('models/randomForestScores.html', title="Random Forest",
                           rf_results=rf_results, is_file=is_file,
                           url='/static/images/predictions.png', imp=imp)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
