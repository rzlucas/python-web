from flask import Blueprint, render_template
from .forms import LoginForm

page = Blueprint('page', __name__)


@page.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@page.route('/')
def index():
    return render_template('index.html', title='Index')

@page.route ('/login')
def login():
    form = LoginForm()

    return render_template('auth/login.html', title='Login', form=form)


