from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import UpdateProfile
from ..request import get_quote
from ..models import User, Blog, Comment


@main.route('/')
def index():
    blogs = Blog.get_all_blogs()
    quote = get_quote()

    return render_template('index.html', blogs = blogs, quote = quote)

@main.route('/blog/new')
def new_blog():

    return render_template('new_blog.html')