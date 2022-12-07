import os
from flask import abort, redirect, render_template, request, session, Blueprint

from src.models import Post, db, Comment



router = Blueprint('posts', __name__)

@router.route('/create_post')
def create_post():
    return render_template('create_post.html')

@router.route('/post/<post_id>')
def view_post(post_id):
    post = Post.query.get(post_id)
    all_comments = Comment.query.filter_by(post_id=post_id).all()
    return render_template('post.html', post=post, all_comments=all_comments)

@router.post('/createpost')
def add_post():
    post_title = request.form.get('post_title')
    post_body = request.form.get('post_body')
    poster_id = session['user']['user_id']
    new_post = Post(post_title, post_body, poster_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect('/')

@router.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post_to_update = Post.query.get(post_id)
    if request.method == "POST":
        post_to_update.post_title = request.form['title']
        post_to_update.post_body = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return abort(400)
    else:
        return render_template('edit_post.html', post_to_update= post_to_update)




@router.post('/deletepost/<int:post_id>')
def delete_post(post_id):
    post_to_delete = Post.query.get_or_404(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()

    return redirect('/')
