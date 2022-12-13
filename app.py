import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, abort
from security import bcrypt
from src.models import db,Post, Post_dislike, Post_like, Team, User, favorite_team, Comment, Comment_dislike, Comment_like
from blueprints.session_blueprint import router as session_router
from blueprints.posts_blueprint import router as posts_router
from blueprints.posts_blueprint import calculate_ratio
from src.livescore import all_matches

load_dotenv()


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = os.getenv('APP_SECRET_KEY')

db.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(session_router)
app.register_blueprint(posts_router)

faq_dictionary = {}


@app.route('/')
def index():
    if 'user' not in session:
        return redirect('/login')

    posts = Post.query.all()
    results = all_matches["match_data"][:20]
    #calculate likes dislikes
    post_pairs = calculate_ratio(posts)
    return render_template('index.html', home_active=True, loged_in = True, username =session['user']['username'], user_id=session['user']['user_id'], post_pairs = post_pairs, results = results)


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/rules')
def rules():
    return render_template('rules.html', rules_active=True, username =session['user']['username'])


@app.route('/about')
def info():
    faq_listofQuestions = ["Does CricketHub plan to expand any further? ", "Does my light or dark mode preference work even if I close the browser?", "How do I comment on a post?", \
        "How strong is CricketHub's security?","Is there a way that I can add a preference for my favorite team?", "Unable to use the search?"]
    faq_listofAnswers = ["POSSIBLY. 🤔"  \
        ,"Yes, we store your preference as a cookie.", "Click on the post, and press the red comment button on the top right.", "It's as strong as Facebook selling your data." \
            , "Not at the moment but our team is working hard to have that feature soon." , "That's because it doesn't work yet."]  

    for i in range(6):
        faq_dictionary[faq_listofQuestions[i]] = faq_listofAnswers[i] 
    return render_template('about.html', about_active=True, faq_dictionary = faq_dictionary, username =session['user']['username'])

@app.get('/profile/<int:user_id>')
def profile(user_id):
    profile = User.query.get(user_id)
    user_id = session['user']['user_id']
    return render_template('profile.html',user_id = user_id ,username = session['user']['username'], user_profile = profile)

@app.get('/profile/<int:user_id>/edit')
def profile_edit(user_id):
    profile = User.query.get(user_id)
    user_id = session['user']['user_id']
    return render_template('profile_edit.html', user_profile=profile, username = session['user']['username'], user_id= user_id)

@app.post('/update_profile/<int:user_id>')
def edit_profile(user_id):
    user_to_update = User.query.get(user_id)
    user_id = session['user']['user_id']
    user_to_update.username= request.form['username']
    user_to_update.name = request.form['name']
    user_to_update.email = request.form['email']

    db.session.commit()
    profile = User.query.get(user_id)
    return render_template('profile.html',user_id = user_id ,username = session['user']['username'], user_profile = profile)

@app.post('/delete_profile/<int:user_id>')
def delete_profile(user_id):
    user_to_delete = User.query.get(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()

    return redirect('/login')

@app.get('/secret')
def secret():
    if 'user' not in session:
        return redirect('/login')


#maybe for delete post we can have "on delete cascade or manually delete likes by id in the delete method, query on likes junction table"

#like dislike function
@app.post('/post/<post_id>/like')
def like(post_id):
    
    user = session['user']['user_id']
    post_like_in_question = Post_like.query.filter_by(users_liked = user, post_id = post_id).first()
    post_dislike_in_question = Post_dislike.query.filter_by(users_disliked = user, post_id = post_id).first()
    if post_like_in_question and post_dislike_in_question:
        Post_like.query.filter_by(users_liked = user, post_id = post_id).delete()
        Post_dislike.query.filter_by(users_disliked= user, post_id = post_id).delete()
        post_like = Post_like(post_id = post_id, users_liked = user)
        db.session.add(post_like)

    elif post_like_in_question:
        Post_like.query.filter_by(users_liked = user, post_id = post_id).delete()
    else:
        if post_dislike_in_question:
            Post_dislike.query.filter_by(users_disliked = user, post_id = post_id).delete()
        post_like = Post_like(post_id = post_id, users_liked = user)
        db.session.add(post_like)
    db.session.commit()
    return redirect('/')
    
#
@app.post('/post/<post_id>/dislike')
def dislike(post_id):
    user = session['user']['user_id']

    post_like_in_question = Post_like.query.filter_by(users_liked = user, post_id = post_id).first()
    post_dislike_in_question = Post_dislike.query.filter_by(users_disliked = user, post_id = post_id).first()
    #stops after first if since it passes
    if post_dislike_in_question and post_like_in_question:
        Post_dislike.query.filter_by(users_disliked = user, post_id = post_id).delete()
        Post_like.query.filter_by(users_liked = user, post_id = post_id).delete()
        post_dislike = Post_dislike(post_id = post_id, users_disliked= user)
        db.session.add(post_dislike)
    elif post_dislike_in_question:
        Post_dislike.query.filter_by(users_disliked = user, post_id = post_id).delete()
    else:
        if post_like_in_question:
            Post_like.query.filter_by(users_liked= user, post_id = post_id).delete
        post_dislike = Post_dislike(post_id = post_id, users_disliked= user)
        db.session.add(post_dislike)

    db.session.commit()
    return redirect('/')

@app.post('/post/<post_id>/<comment_id>/like')
def like_comment(post_id, comment_id):
    user = session['user']['user_id']

    comment_like_in_question = Comment_like.query.filter_by(users_liked = user, comment_id = comment_id).first()
    comment_dislike_in_question = Comment_dislike.query.filter_by(users_disliked = user, comment_id = comment_id).first()

    if comment_like_in_question and comment_dislike_in_question:
        Comment_like.query.filter_by(users_liked = user, comment_id = comment_id).delete()
        Comment_dislike.query.filter_by(users_disliked = user, comment_id = comment_id).delete()
        comment_like = Comment_like(comment_id= comment_id, users_liked= user, post_id = post_id)
        db.session.add(comment_like)
    elif comment_like_in_question:
        Comment_like.query.filter_by(users_liked = user, comment_id = comment_id).delete()
    else:
        if comment_dislike_in_question:
            Comment_dislike.query.filter_by(users_disliked = user, comment_id = comment_id).delete()
        comment_like = Comment_like(comment_id= comment_id, users_liked= user, post_id = post_id)
        db.session.add(comment_like)
    db.session.commit()
    return redirect(f'/post/{post_id}')

@app.post('/post/<post_id>/<comment_id>/dislike')
def dislike_comment(comment_id, post_id):
    user = session['user']['user_id']

    comment_like_in_question = Comment_like.query.filter_by(users_liked = user, comment_id = comment_id).first()
    comment_dislike_in_question = Comment_dislike.query.filter_by(users_disliked = user, comment_id = comment_id).first()
    
    if comment_like_in_question and comment_dislike_in_question:
        Comment_like.query.filter_by(users_liked = user, comment_id = comment_id).delete()
        Comment_dislike.query.filter_by(users_disliked = user, comment_id = comment_id).delete()
        comment_dislike= Comment_dislike(comment_id= comment_id, users_liked= user, post_id = post_id)
        db.session.add(comment_dislike)
    elif comment_dislike_in_question:
        Comment_dislike.query.filter_by(users_disliked = user, comment_id = comment_id).delete()
    else:
        if Comment_like.query.filter_by(users_liked = user, comment_id = comment_id).delete():
            Comment_like.query.filter_by(users_liked = user, comment_id = comment_id).delete()
        comment_dislike= Comment_dislike(comment_id= comment_id, users_disliked= user, post_id = post_id)
        db.session.add(comment_dislike)
    db.session.commit()
    return redirect(f'/post/{post_id}')

@app.post('/profile/edit')
def prof_edit():
    return redirect('/profile')  

