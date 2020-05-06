from flask import Flask, render_template, flash, redirect, request, session
from flask_bootstrap import Bootstrap
from forms import *
import requests
import os

app = Flask(__name__, static_folder='static')

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

bootstrap = Bootstrap(app)


DB_ADAPTER_URL = 'http://db_adapter:5001'

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
        json = {
            'email': form.email.data,
            'password': form.password.data
        }
        r = requests.post(url=DB_ADAPTER_URL + '/login', json=json)
        session['user'] = r.json()['data']
        return redirect('/index')
    return render_template('login.html', form=form, user=session['user'])

@app.route('/register', methods={'GET', 'POST'})
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        json = {
            'email': form.email.data,
            'firstname': form.firstname.data,
            'lastname': form.lastname.data,
            'password': form.password.data,
        }
        r = requests.post(url=DB_ADAPTER_URL + '/register', json=json)
        session['user'] = r.json()['data']
        return redirect('/index')
    return render_template('register.html', form=form, user=session['user'])

@app.route('/logout', methods={'GET', 'POST'})
def logout():
    session['user'] = None
    return redirect('/index')

@app.route('/newtrip', methods={'GET', 'POST'})
def newtrip():
    if not session['user']:
        return redirect('/index')
    form = NewTripForm()
    if form.validate_on_submit():
        json = {
            'user_id': session['user']['id'],
            'country': form.country.data,
            'city': form.city.data,
            'departure_date': str(form.departure_date.data),
            'return_date': str(form.return_date.data)
        }
        print(json)
        requests.post(url=DB_ADAPTER_URL + '/newtrip', json=json)

        return redirect('/trips')
    return render_template('newtrip.html', form=form, user=session['user'])

@app.route('/newflight', methods={'GET', 'POST'})
def newflight():
    form = NewFlightTicketForm()
    r = requests.post(url=DB_ADAPTER_URL + '/get_trip_choices', json={'user_id': session['user']['id']})
    form.trip.choices = r.json()['trips']
    if form.validate_on_submit():
        departure_time = str(form.departure_date.data) + " " + form.departure_hour.data + ":00"
        arrival_time = str(form.arrival_date.data) + " " + form.arrival_hour.data + ":00"
        json = {
            'trip_id': int(form.trip.data),
            'flight_no': form.flight_no.data,
            'departure_time': departure_time,
            'arrival_time': arrival_time,
            'from_city': form.from_city.data,
            'to_city': form.to_city.data
        }
        requests.post(url=DB_ADAPTER_URL + '/newflight', json=json)
        return redirect('/flights')
    return render_template('newflight.html', form=form, user=session['user'])


@app.route('/trips', methods={'GET', 'POST'})
def trips():
    r = requests.post(url=DB_ADAPTER_URL + '/trips', json={'user_id': session['user']['id']})
    trips = r.json()['trips']
    print(trips)
    return render_template('trips.html', user=session['user'], trips=trips)

@app.route('/flights', methods={'GET', 'POST'})
def flights():
    r = requests.post(url=DB_ADAPTER_URL + '/flights', json={'user_id': session['user']['id']})
    flights = r.json()['flights']
    return render_template('flights.html', user=session['user'], flights=flights)

# @app.route('/statistics', methods={'GET', 'POST'})
# def statistics():
#     countries = db_conn.get_most_visited_countries(session['user']['id'])
#     print(countries)
#     return render_template('statistics.html', user=session['user'], countries=countries)


@app.route('/trip_photos', methods={'GET'})
def trip_photos():
    photos = []
    return render_template('trip_photos.html', user=session['user'], photos=photos)
    
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)