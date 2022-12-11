import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, abort
from security import bcrypt
from src.models import Team, User, db,Post, Post_dislike, Post_like, favorite_team
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

