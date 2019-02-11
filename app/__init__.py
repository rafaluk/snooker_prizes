from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
import dominate
from dominate.tags import img

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

nav = Nav()
branding = img(src='static/images/logo.png', width=30, height=30)


@nav.navigation()
def mynavbar():
    return Navbar(
        branding,
        View('Home', 'index'),
        View('My blog', 'blog')
    )


nav.init_app(app)

from app import routes
