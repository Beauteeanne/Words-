import re
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    # return 'logout'
    return redirect(url_for('views.home'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "GET":
        return render_template('adduser.html')
    if request.method == "POST":
        name = request.form.get('name')
        name = re.split(r'\s+', name)
        _fname = name[0]
        _lname = name[1]
        _email = request.form.get('email')
        _tel = request.form.get('tel')
        _pwrd = request.form.get('pwrd')
        _pwrd2 = request.form.get('pwrd2')
        
        user = User.query.filter_by(email=_email).first()
        print(user)

        if user:
            flash('Email already exists.', category='error')
            return redirect(url_for('auth.sign_up'))
        elif len(_fname or _lname) < 2:
            flash('each name must be more than 3 characters.', category='error')
            return redirect(url_for('auth.sign_up'))
        elif _pwrd != _pwrd2:
            flash('password don\'t match.', category='error')
            return redirect(url_for('auth.sign_up'))
        elif len(_pwrd) < 7:
            flash('password must be more than 7 characters.', category='error')
            return redirect(url_for('auth.sign_up'))
        else:
            new_user = User(first_name=_fname, last_name=_lname, email=_email, phone=_tel, password=generate_password_hash(_pwrd, method='sha256'), image='', cv=None)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))

    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pass')

        user = User.query.filter_by(email=email).first()

        if user:
            print(password)
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                current_user=user
                
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
                return render_template('login.html')
        else:
            flash('Email does not exist.', category='error')
            return render_template('login.html')

    return render_template('login.html', current_user=user)


