import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for, session, abort
from security import bcrypt
from src.models import db,User,Post, Comment, Post_like, Post_dislike
from blueprints.session_blueprint import router as session_router

load_dotenv()


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = os.getenv('APP_SECRET_KEY')

db.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(session_router)

faq_dictionary = {}

def calculate_ratio(posts: list[Post]) -> list[list[int, Post]]:
    ratio_post_pair=[]
    for post in posts:
        amt_likes = len(Post_like.query.filter_by(post_id = post.post_id).all())
        amt_dislikes = len(Post_dislike.query.filter_by(post_id = post.post_id).all())
        
        ratio = amt_likes - amt_dislikes
        ratio_post_pair.append([ratio, post])
    return ratio_post_pair


@app.route('/')
def index():
    if 'user' not in session:
        return redirect('/login')

    posts = Post.query.all()
    #calculate likes dislikes
    post_pairs = calculate_ratio(posts)
    #results = Livescore.results_of_matches
    return render_template('index.html', home_active=True, loged_in = True, username =session['user']['username'], post_pairs = post_pairs)

@app.route('/create_post')
def create_post():
    return render_template('create_post.html')

@app.post('/createpost')
def create():
    
    post_title = request.form.get('post_title')
    post_body = request.form.get('post_body')
    poster_id = session['user']['user_id']
    new_post = Post(post_title, post_body, poster_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect('/')
#maybe modify, /post/<post_id>/edit
@app.route('/edit_post')
def edit_post():
    return render_template('edit_post.html')

@app.route('/post/<post_id>')
def view_post(post_id):
    post = Post.query.get(post_id)
    all_comments = Comment.query.filter_by(post_id=post_id).all()
    return render_template('post.html', post=post, all_comments=all_comments)


@app.post('/post/<post_id>/create_comment')
def create_comment(post_id):

    content = request.form.get('comment_body')
    error_msg =''
    if content is None:
        error_msg = "Comment needs content"
        return abort(403)
    #how to create post id
    commentor_id = session['user']['user_id']

    new_comment = Comment(content=content, post_id=post_id, commentor_id=commentor_id)

    db.session.add(new_comment)
    db.session.commit()

    return redirect(f'/post/{post_id}')

#add like and dislike

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/rules')
def rules():
    return render_template('rules.html', rules_active=True)


@app.route('/about')
def info():
    faq_listofQuestions = ["Why cricket in the US?", "Where can I play cricket?", "When is the next Cricket World Cup?", \
        "Who is the GOAT?","How did this page come into existence?", "I forgot my username and password?"]
    faq_listofAnswers = ["Cricket is an amazing sport! There is a huge niche of diverse students for example at UNC Charlotte. Everyday more and more are introduced to the game."  \
        ,"There’s a cricket club at UNC Charlotte.", "October 2023.", "Brian Lara, Sachin Tendulker, or Shane Warne don't @ me." \
            , "Through the work of college students." , "Check your email on record for original signup information."]  

    for i in range(6):
        faq_dictionary[faq_listofQuestions[i]] = faq_listofAnswers[i] 
    return render_template('about.html', about_active=True, faq_dictionary = faq_dictionary)

@app.get('/profile')
def prof():
    post_firstname = request.form.get('firstname-dis')
    post_lastname = request.form.get('lastname-dis')
    post_email = request.form.get('email')

    return render_template('profile.html')


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


@app.post('/profile/edit')
def prof_edit():
    return redirect('/profile')  

