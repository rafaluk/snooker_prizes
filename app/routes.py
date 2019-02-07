from flask import render_template, redirect, url_for, flash, request, session, json
from app import app
from app.forms import LoginForm, WelcomeScreenForm, CreateDataForm, DetailsForm, HistogramForm, \
    HistogramForm2, ModelForm, TrainForm, RandomForestForm
from .static.utils import Utils
import pandas as pd
from plot_gen import PlotGenerator


df = pd.DataFrame()
model_name = ""

@app.route('/')
def nothing():
    return redirect(url_for('index'))


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
            # TEN KOMENTARZ JEST TYLKO PO TO, ZEBY SZYBKO DZIALALO! DOCELOWQ DO ODKOMENTOWANIA!!!!
            # Utils.get_snooker_data(seasons=seasons)
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
    # print(df.head())
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
        return redirect(url_for('model'))

    return render_template('analyse.html', title="Analysis", form=form, form2=form2, is_file=is_file)


@app.route('/model', methods=['GET', 'POST'])
def model():
    form = ModelForm()
    global model_name

    if form.validate_on_submit():
        model_name = form.models.data
        # CHANGE URL_FOR TO SPECIFIC SUBPAGES
        if model_name == "randomForest":
            return redirect(url_for('randomForest'))
        elif model_name == "knn":
            return redirect(url_for('train'))
        elif model_name == "linearRegression":
            return redirect(url_for('train'))

    return render_template('model.html', title="Choose model", form=form)


@app.route('/models/randomForest', methods=['GET', 'POST'])
def randomForest():
    form = RandomForestForm()

    if form.validate_on_submit():
        # TODO redirect and performing random forest
        if form.my_parameters.data:
            print("todo")
            # performing random forest calculations, new class probably
        elif form.random_parameters.data:
            print("todo")

    return render_template('models/randomForest.html', title="Random Forest", form=form)


@app.route('/train')
def train():
    global model_name
    form = TrainForm()

    return render_template('train.html', title="Train", model_name=model_name)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title="Sing in", form=form)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

