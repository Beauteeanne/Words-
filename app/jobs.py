import base64
from flask import Blueprint, current_app, redirect, render_template, request, url_for, flash
# werkzeug for ecryting passwords
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from .models import Job, Job_Category
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# create a blueprint alternative to app eg @app.route since app == Flask name, views == flask name
# app = Flask(__name__)
# app.route('/<route name>)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
  
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

ROWS_PER_PAGE = 5

jobs = Blueprint('jobs', __name__)


@jobs.route('/jobs')
def job_listing():
    page = request.args.get('page', 1, type=int)
    categories = Job_Category.query.all()

    all_jobs = Job.query.paginate(page=page, per_page=ROWS_PER_PAGE)

    return render_template('job_listing.html', all_jobs=all_jobs, categories=categories)

@jobs.route('/jobs/job/<id>')
def job_detials(id):
    job = Job.query.options(db.joinedload(Job.category)).filter_by(id=id).all()
    return render_template('job_details.html', job=job)

@jobs.route('/add-job', methods=['GET', 'POST'])
def add_job():
    if request.method == 'GET':
        categories = Job_Category.query.all()

        return render_template('add_jobs.html', categories=categories)

    if request.method == 'POST':    
        title = request.form.get('title')
        price = request.form.get('price')
        desc = request.form.get('message')
        category = request.form.get('category')
        created_by = current_user
        accepted_by = None
        image = request.files['image']

        print(category)

        category = Job_Category.query.filter_by(id=int(category)).first()

        if image and allowed_file(image.filename):
            # image = base64.b64encode(image.read())
            image = request.files['image'].read()
            image = base64.b64encode(image)
            image = image.decode("utf-8")

            new_job = Job(title=title, price=price, description=desc, image=image, owner=created_by, freelancer=accepted_by, category=category)
            print(new_job)
            db.session.add(new_job)
            db.session.commit()
            return redirect(url_for('jobs.my_job_listing'))
        else:
            flash('file is not allowed', category='error')
            return redirect(url_for('jobs.add_job'))

        # print(image)

        # print(image)
        # return redirect(url_for('jobs.add_job'))
        # return f'<img src="data:image/png; base64, {image}"/>'
        # return '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAABmJLR0QA/wD/AP+gvaeTAAABDElEQVRoge3ZXQqCQBSG4a8WUdIWbbmBtRq70A8kxBw9fzOc96oukvOg6QwCWZZlLdUD6LyHwDRDf/THTwAjgAG+mG6eYZxnKu4G4DUf4APgITba/u6LGd5nZvDEiCGYB0YcwSwxaghmgVFHME2MGYJpYMwRTBLjhmASGHcEO4MJg2BHMOEQrAQTFsH2YMIj2BamGgRbw1SHYMs9xPDzOcJGrajlmVE/E1etAwO4/PleRU1cWmt/7Ajb5qK27k7VYPbcYsNjSp4TYTFHHnbhMGee2GEwEssOd4zk2skNo7EANMdormLNMBZLcXWM5X5CDeOxKRLHeO7sxDARtqcimGZevQGNvAzNsiyL1xcbE8X3wv0coQAAAABJRU5ErkJggg=="/>'
        # print(image.decode('utf-8'))
        # return f'<img src="data:image/png;base64,{image}"/>'


@jobs.route('/my-jobs')
def my_job_listing():

    # Set the pagination configuration
    page = request.args.get('page', 1, type=int)

    my_jobs = Job.query.paginate(page=page, per_page=ROWS_PER_PAGE)

    return render_template('my_job_listing.html', my_jobs=my_jobs)