import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, abort
from security import bcrypt
from src.models import db,Post, Post_dislike, Post_like
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
    faq_listofQuestions = ["Why cricket in the US?", "Where can I play cricket?", "When is the next Cricket World Cup?", \
        "Who is the GOAT?","How did this page come into existence?", "I forgot my username and password?"]
    faq_listofAnswers = ["Cricket is an amazing sport! There is a huge niche of diverse students for example at UNC Charlotte. Everyday more and more are introduced to the game."  \
        ,"There’s a cricket club at UNC Charlotte.", "October 2023.", "Brian Lara, Sachin Tendulker, or Shane Warne don't @ me." \
            , "Through the work of college students." , "Check your email on record for original signup information."]  

    for i in range(6):
        faq_dictionary[faq_listofQuestions[i]] = faq_listofAnswers[i] 
    return render_template('about.html', about_active=True, faq_dictionary = faq_dictionary, username =session['user']['username'])

@app.get('/profile')
def prof():
    post_firstname = request.form.get('firstname-dis')
    post_lastname = request.form.get('lastname-dis')
    post_email = request.form.get('email')

    return render_template('profile.html', username =session['user']['username'])


@app.get('/secret')
def secret():
    if 'user' not in session:
        return redirect('/login')


#maybe for delete post we can have "on delete cascade or manually delete likes by id in the delete method, query on likes junction table"

#like dislike function
@app.post('/post/<post_id>/like')
def like(post_id):
    
    liked = session['user']['user_id']
    post_like_in_question = Post_like.query.filter_by(users_liked = liked, post_id = post_id).first()
    post_dislike_in_question = Post_dislike.query.filter_by(users_disliked = liked, post_id = post_id).first()
    if post_like_in_question:
        Post_like.query.filter_by(users_liked = liked, post_id = post_id).delete()
        
    else:
        if post_dislike_in_question:
            Post_dislike.query.filter_by(users_disliked = liked, post_id = post_id).delete()
        post_like = Post_like(post_id = post_id, users_liked = liked)
        db.session.add(post_like)
    db.session.commit()
    return redirect('/')
    

@app.post('/post/<post_id>/dislike')
def dislike(post_id):
    users_disliked = session['user']['user_id']
    
    post_dislike = Post_dislike(post_id = post_id, users_disliked= users_disliked)
    db.session.add(post_dislike)
    db.session.commit()
    return redirect('/')


#count likes dislikes, have a function that counts likes for a post, count dislikes for a specific post, likes - dislikes
#maybe write function that will calculate likes / dislike for the display


@app.post('/profile/edit')
def prof_edit():


    
    return redirect('/profile')  

