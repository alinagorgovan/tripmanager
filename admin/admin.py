from flask import Flask, render_template, flash, redirect, request, session
from flask_bootstrap import Bootstrap
from forms import *
import requests
import os

app = Flask(__name__, static_folder='static')

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

bootstrap = Bootstrap(app)


DB_ADAPTER_URL = 'http://db_adapter:5001'

admin_users = {
    "admin" : "admin"
}

@app.route('/')
@app.route('/index')
def index():
    if 'user' not in session:
        session['user'] = None
    return render_template('index.html', user=session['user'])

@app.route('/login', methods={'GET', 'POST'})
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username in admin_users and admin_users[username] == password:       
            session['user'] = username
            return redirect('/index')
    return render_template('login.html', form=form, user=session['user'])

@app.route('/logout', methods={'GET', 'POST'})
def logout():
    session['user'] = None
    return redirect('/index')
    
    
@app.route('/statistics', methods={'GET', 'POST'})
def statistics():
    r = requests.get(url=DB_ADAPTER_URL + '/statistics')
    countries = r.json()['statistics']
    return render_template('statistics.html', user=session['user'], countries=countries)

@app.route('/users', methods={'GET'})
def users():
    r = requests.get(url=DB_ADAPTER_URL + '/users')
    result = r.json()['users']
    return render_template('users.html', users=result, user=session['user'])
    
@app.route('/delete_user/<int:user_id>', methods={'GET'})
def delete_user(user_id):
    requests.post(url=DB_ADAPTER_URL + '/delete_user', json={'user_id': user_id})
    return redirect('/users')
    

    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003, debug=True)