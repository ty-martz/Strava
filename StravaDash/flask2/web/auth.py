from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

# login/out and signup

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, try again', category='error')
        else:
            flash('email does not exist', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required # can only access route if logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if User.query.filter_by(email=email).first():
            flash('Email already in use. Please use another email', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(firstname) < 1:
            flash('First name must be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 4:
            flash("Password must be greater than 4 characters", category='error')
        else:
            # add user to DB
            new_user = User(email=email, first_name=firstname, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)

            flash('Account created', category='success')
            return redirect(url_for('views.home'))

    return render_template('signup.html', user=current_user)
