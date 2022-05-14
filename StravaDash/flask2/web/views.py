# pages to navigate to in web app
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Activities
from . import db
import json

# Blueprint of routes/urls

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
#@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short, must be at least one character', category='error')
        else:
            new_activities = Activities(data=note, user_id=current_user.id)
            db.session.add(new_activities)
            db.session.commit()
            flash('New note added', category='success')

    return render_template('home.html', user=current_user)\


@views.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    return render_template('profile.html')

@views.route('/dash', methods=['POST', 'GET'])
@login_required
def dash():
    return render_template('dash.html')