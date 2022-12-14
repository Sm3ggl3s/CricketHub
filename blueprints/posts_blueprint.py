import os
from flask import abort, redirect, render_template, request, session, Blueprint

from src.models import Post, User, db, Comment,Post_like, Post_dislike, Comment_dislike, Comment_like



router = Blueprint('posts', __name__)


def calculate_ratio(posts: list[Post]) -> list[list[int, Post]]:
    ratio_post_pair=[]
    for post in posts:
        amt_likes = len(Post_like.query.filter_by(post_id = post.post_id).all())
        amt_dislikes = len(Post_dislike.query.filter_by(post_id = post.post_id).all())
        
        ratio = amt_likes - amt_dislikes
        ratio_post_pair.append([ratio, post])
    return ratio_post_pair

def calculate_comment_ratio(comments: list[Comment])-> list[list[int, Comment]]:
    ratio_comment_pair=[]
    for comment in comments:
        amt_likes = len(Comment_like.query.filter_by(comment_id = comment.comment_id).all())
        amt_dislikes = len(Comment_dislike.query.filter_by(comment_id = comment.comment_id).all())

        ratio = amt_likes - amt_dislikes
        ratio_comment_pair.append([ratio, comment])
    return ratio_comment_pair

@router.route('/post/<post_id>')
def view_post(post_id):
    post = Post.query.get(post_id)
    amt_likes = len(Post_like.query.filter_by(post_id = post.post_id).all())
    amt_dislikes = len(Post_dislike.query.filter_by(post_id = post.post_id).all())

    ratio=amt_likes-amt_dislikes
    comments = Comment.query.all()
    comment_pairs= calculate_comment_ratio(comments)

    return render_template('post.html', post=post,  user_id=session['user']['user_id'], username=session['user']['username'], ratio=ratio,  
    comment_pairs=comment_pairs)

@router.route('/create_post')
def create_post():
    return render_template('create_post.html')

@router.post('/createpost')
def create():
    post_title = request.form.get('post_title')
    post_body = request.form.get('post_body')
    poster_id = session['user']['user_id']

    if post_title is None or post_body is None or poster_id =='':
        abort(400)
    
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


@router.post('/post/<post_id>/create_comment')
def create_comment(post_id):
    post_id = post_id
    content = request.form.get('comment_body')
    commentor_id = session['user']['user_id']
    error_msg =''
    if content is None:
        error_msg = "Comment needs content"
        return abort(403)
    #how to create post id
    

    new_comment = Comment(content, post_id, commentor_id)

    db.session.add(new_comment)
    db.session.commit()

    return redirect(f'/post/{post_id}')


@router.post('/post/<int:post_id>/delete')
def delete_post(post_id):
    post_to_delete = Post.query.get_or_404(post_id)
    #delete_post_method = session.query(Post, Comment, Comment_like, Comment_dislike)
    if 'user' in session:
        user_id = session['user'].get('user_id')
        if post_to_delete.poster_id == user_id:
            Post_like.query.filter_by(post_id=post_id).delete()
            Post_dislike.query.filter_by(post_id=post_id).delete()

            # How to access the dislikes or likes tables foreign keys that are linked to like / dislike
            #Comment.filter_by(post_id).Comment_like
            Comment_like.query.filter_by(post_id=post_id).delete()
            Comment_dislike.query.filter_by(post_id=post_id).delete()
            Comment.query.filter_by(post_id=post_id).delete()

            db.session.delete(post_to_delete)
            db.session.commit()
    
    return redirect('/')    


@router.post('/post/<int:post_id>/delete/<int:comment_id>')
def delete_comm(post_id, comment_id):
    comment_to_delete = Comment.query.get_or_404(comment_id)
    if comment_to_delete.commentor_id == session['user']['user_id']:
        db.session.delete(comment_to_delete)
        db.session.commit()
        post_id = post_id
    return redirect('/post/{{post_id}}', )