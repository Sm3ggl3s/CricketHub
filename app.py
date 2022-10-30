from flask import Flask, redirect, render_template, request

app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')