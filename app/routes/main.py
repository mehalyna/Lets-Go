from flask import Blueprint, render_template, session, request
from app.models.post import Post

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    username = session.get('username')
    page = int(request.args.get('page', 1))
    skip = (page - 1) * 10
    
    if username:
        # Show feed from followed users
        posts = Post.get_feed(username, skip=skip, limit=10)
    else:
        # Show all posts
        posts = Post.get_all(skip=skip, limit=10)
    
    return render_template('main/index.html', posts=posts, page=page)

@bp.route('/about')
def about():
    return render_template('main/about.html')
