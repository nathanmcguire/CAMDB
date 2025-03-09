# app/controllers/index.py

from flask import Blueprint, render_template

# Create a Blueprint for the index controller
index_bp = Blueprint('index', __name__)

# Route for the home page
@index_bp.route('/')
def index():
    # Any data you want to pass to the template
    title = "Welcome to Flask CMDB"
    return render_template('index.html', title=title)