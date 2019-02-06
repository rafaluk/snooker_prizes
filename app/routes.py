from flask import render_template, redirect, url_for, flash
from app import app
from app.forms import LoginForm, WelcomeScreenForm, CreateDataForm
from .static.utils import Utils
import pandas as pd
from DataPrepare import DataPrepare


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
    path = "app/static/images/wykresso.png"
    is_deleted = Utils().delete_file(path)

    if is_deleted:
        print("Image deleted: " + path)
        is_file = False
    else:
        print("There's no such file: " + path)
        is_file = False

    if form.validate_on_submit():
        try:
            # TEN KOMENTARZ JEST TYLKO PO TO, ZEBY SZYBKO DZIALALO! DOCELOWQ DO ODKOMENTOWANIA!!!!
            # Utils.get_snooker_data(seasons=seasons)
            return redirect(url_for('details'))
        except:
            flash("Download failed :( Refresh this website and try again.")
            print("Download failed.")

        # gen = PlotGenerator()
        # gen.plot_and_save()
        # is_file = True

    return render_template('create.html', title="Create data",
                           form=form, url='static/images/wykresso.png', is_file=is_file)


@app.route('/details')
def details():
    df = pd.read_csv("app/static/dataframes/snooker_data.csv", sep=";")
    col_count = len(df.columns)
    row_count = df.shape[0]
    columns = df.columns
    # to trzeba przekazac z create
    seasons = ['2015-2016', '2016-2017', '2017-2018']
    return render_template('details.html', title="Details", columns=columns, df=df,
                           col_count=col_count, row_count=row_count, seasons=seasons)


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

