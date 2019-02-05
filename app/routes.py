from flask import render_template, redirect, url_for, request
from app import app
from app.forms import LoginForm, WelcomeScreenForm, CreateDataForm
import numpy as np
import matplotlib.pyplot as plt


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
    x = np.arange(1, 100, 10)
    y = np.random.rand(10)
    plt.plot(x, y)
    plt.savefig('app/static/images/wykres.png')
    # if request.form['btn'] == "dupa":
    #     return redirect(url_for('index'))

    if form.validate_on_submit():
        x = np.arange(1, 100, 10)
        y = np.random.rand(10)
        plt.plot(x, y)
        plt.savefig('app/static/images/wykres.png')
        return redirect(url_for('index'))

    return render_template('create.html', title="Create data", form=form, url='static/images/wykres.png')




@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title="Sing in", form=form)


