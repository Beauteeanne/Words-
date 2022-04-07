from functools import wraps
from flask import Blueprint, current_app, redirect, render_template, request, url_for, flash
from .models import Job, Job_Category
from . import db
from flask_login import login_user, login_required, logout_user, current_user

admin_view = Blueprint('admin_view', __name__)

# , subdomain='dasboard'


def admin_required(user):
    """make sure user has this role"""
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            if not current_user.is_Admin(user):
                logout_user()
                return redirect("/")
            else:
                return func(*args, **kwargs)
        return wrapped_function
    return decorator


@admin_view.route('/admin/add-category', methods=['GET', 'POST'])
@login_required
@admin_required(user=current_user)
def add_category():
    if request.method == 'GET':
        return render_template('add_job_c.html')
    if request.method == 'POST':
        name = request.form.get('name')
        desc = request.form.get('message')

        if len(name) < 3:
            flash('name must be more than 3 characters.', category='error')
            return redirect(url_for('admin.root'))
        else:
            new_category = Job_Category(name=name, description=desc)

            db.session.add(new_category)
            db.session.commit()

            return redirect(url_for('admin.root'))

# @admin_view.route('/admin')
# @login_required
# @admin_required(user=current_user)
# def root():
#     return render_template('admin.html')