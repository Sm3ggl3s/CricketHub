import os

# from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for

from src.models import db, User

# load_dotenv()


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

faq_dictionary = {}

@app.route('/')
def index():

    return render_template('index.html', home_active=True)

@app.route('/create_post')
def create_post():

    return render_template('create_post.html')

@app.route('/edit_post')
def edit_post():
    return render_template('edit_post.html')

@app.route('/login')
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    return render_template('login.html')

@app.route('/signup')
def signup():
    username = request.form.get('username')
    password = request.form.get('password')

    existing_user = User.query.filter_by(username=username).first()

    return render_template('signup.html')


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

@app.route('/profile')
def prof():

    return render_template('profile.html')