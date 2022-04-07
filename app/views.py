from flask import Blueprint, current_app, redirect, render_template, request, url_for, flash
# werkzeug for ecryting passwords
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .models import Job_Category, Job

# create a blueprint alternative to app eg @app.route since app == Flask name, views == flask name
# app = Flask(__name__)
# app.route('/<route name>)


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "GET":
        category = Job_Category.query.all()
        return render_template('index.html', category=category)
    if request.method == "POST":
        search = request.form.get('search')
        category = request.form.get('category')
        search_jobs = Job.query.filter(Job.title.contains(f'{search}')).all()
        print(search_jobs)
        # return render_template('search.html', search_jobs=search_jobs)
        return redirect(url_for('views.search', search_jobs=search_jobs))

@views.route('/contact')
def contact():
    return render_template('contact.html')

@views.route('/about')
def about():
    return render_template('about.html')


@views.route('/blog')
def blog():
    return render_template('blog.html')


@views.route('/blog/blog')
def single_blog():
    return render_template('single-blog.html')

@views.route('/search')
def search():
    return render_template('search.html')

