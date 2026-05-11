from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user import User
from app.models.post import Post
from app.routes.auth import login_required

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/<username>')
def profile(username):
    user = User.find_by_username(username)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('main.index'))
    
    page = int(request.args.get('page', 1))
    skip = (page - 1) * 10
    posts = Post.get_by_user(username, skip=skip, limit=10)
    
    current_username = session.get('username')
    is_following = False
    if current_username and current_username != username:
        is_following = User.is_following(current_username, username)
    
    follower_count = User.get_follower_count(username)
    following_count = User.get_following_count(username)
    
    return render_template('users/profile.html', 
                         user=user, 
                         posts=posts, 
                         page=page,
                         is_following=is_following,
                         follower_count=follower_count,
                         following_count=following_count)

@bp.route('/<username>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    current_username = session.get('username')
    if current_username != username:
        flash('You can only edit your own profile.', 'danger')
        return redirect(url_for('users.profile', username=username))
    
    user = User.find_by_username(username)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        bio = request.form.get('bio')
        avatar_url = request.form.get('avatar_url')
        
        try:
            User.update_profile(username, bio=bio, avatar_url=avatar_url)
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('users.profile', username=username))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
    
    return render_template('users/edit_profile.html', user=user)

@bp.route('/<username>/follow', methods=['POST'])
@login_required
def follow(username):
    current_username = session.get('username')
    if current_username == username:
        flash('You cannot follow yourself.', 'warning')
        return redirect(url_for('users.profile', username=username))
    
    try:
        User.follow(current_username, username)
        flash(f'You are now following {username}.', 'success')
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')
    
    return redirect(url_for('users.profile', username=username))

@bp.route('/<username>/unfollow', methods=['POST'])
@login_required
def unfollow(username):
    current_username = session.get('username')
    try:
        User.unfollow(current_username, username)
        flash(f'You have unfollowed {username}.', 'info')
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')
    
    return redirect(url_for('users.profile', username=username))

@bp.route('/<username>/followers')
def followers(username):
    user = User.find_by_username(username)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('main.index'))
    
    page = int(request.args.get('page', 1))
    skip = (page - 1) * 20
    followers = User.get_followers(username, skip=skip, limit=20)
    
    return render_template('users/followers.html', user=user, followers=followers, page=page)

@bp.route('/<username>/following')
def following(username):
    user = User.find_by_username(username)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('main.index'))
    
    page = int(request.args.get('page', 1))
    skip = (page - 1) * 20
    following = User.get_following(username, skip=skip, limit=20)
    
    return render_template('users/following.html', user=user, following=following, page=page)

@bp.route('/explore')
def explore():
    page = int(request.args.get('page', 1))
    skip = (page - 1) * 20
    users = User.get_all(skip=skip, limit=20)
    
    return render_template('users/explore.html', users=users, page=page)
