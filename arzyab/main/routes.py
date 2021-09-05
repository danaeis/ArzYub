from flask import render_template, url_for, Blueprint, request
from flask_login import login_user, current_user, logout_user, login_required

main = Blueprint('main', __name__)



@main.route("/")
@main.route("/dashboard")
@login_required
def dashboard():

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    
    return render_template('dashboard.html', image_file=image_file)

@main.route("/about")
def about():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('about.html', title='About', image_file=image_file)
