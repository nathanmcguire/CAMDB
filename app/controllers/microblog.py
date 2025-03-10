# app/controllers/index.py

from flask import Blueprint, render_template

# Create a Blueprint for the index controller
microblog_bp = Blueprint('microblog', __name__)

# Route for the home page
@microblog_bp.route('/microblog')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('microblog/index.html', title='Home', posts=posts)