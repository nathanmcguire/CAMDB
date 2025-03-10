from flask import render_template, request, redirect, url_for, Blueprint

from app import db
from app.models.posts import Post

# Create a Blueprint for controls
posts_bp = Blueprint('posts', __name__)

# Route for displaying all controls
@posts_bp.route('/posts')
#@login_required
def list():
    all_posts = Post.query.all()
    return render_template('posts/list.html', posts=all_posts)