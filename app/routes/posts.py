from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models.post import Post
from app.routes.auth import login_required

bp = Blueprint('posts', __name__, url_prefix='/posts')

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        content = request.form.get('content')
        image_url = request.form.get('image_url')
        
        if not content:
            flash('Post content is required.', 'danger')
            return render_template('posts/create.html')
        
        username = session.get('username')
        try:
            Post.create(username, content, image_url=image_url)
            flash('Post created successfully!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
    
    return render_template('posts/create.html')

@bp.route('/<post_id>')
def view(post_id):
    result = Post.find_by_id(post_id)
    if not result:
        flash('Post not found.', 'danger')
        return redirect(url_for('main.index'))
    
    post = result['p']
    author = result['u']
    comments = Post.get_comments(post_id)
    like_count = Post.get_like_count(post_id)
    
    current_username = session.get('username')
    is_liked = False
    if current_username:
        is_liked = Post.is_liked_by(post_id, current_username)
    
    return render_template('posts/view.html', 
                         post=post, 
                         author=author, 
                         comments=comments,
                         like_count=like_count,
                         is_liked=is_liked)

@bp.route('/<post_id>/delete', methods=['POST'])
@login_required
def delete(post_id):
    username = session.get('username')
    try:
        Post.delete(post_id, username)
        flash('Post deleted successfully.', 'success')
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')
    
    return redirect(url_for('users.profile', username=username))

@bp.route('/<post_id>/like', methods=['POST'])
@login_required
def like(post_id):
    username = session.get('username')
    try:
        Post.like(post_id, username)
        like_count = Post.get_like_count(post_id)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'like_count': like_count})
        
        flash('Post liked!', 'success')
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': str(e)}), 400
        flash(f'An error occurred: {str(e)}', 'danger')
    
    return redirect(request.referrer or url_for('main.index'))

@bp.route('/<post_id>/unlike', methods=['POST'])
@login_required
def unlike(post_id):
    username = session.get('username')
    try:
        Post.unlike(post_id, username)
        like_count = Post.get_like_count(post_id)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'like_count': like_count})
        
        flash('Post unliked.', 'info')
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': str(e)}), 400
        flash(f'An error occurred: {str(e)}', 'danger')
    
    return redirect(request.referrer or url_for('main.index'))

@bp.route('/<post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    content = request.form.get('content')
    if not content:
        flash('Comment content is required.', 'danger')
        return redirect(url_for('posts.view', post_id=post_id))
    
    username = session.get('username')
    try:
        Post.add_comment(post_id, username, content)
        flash('Comment added!', 'success')
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')
    
    return redirect(url_for('posts.view', post_id=post_id))
