from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectField, MultipleFileField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email
import pycountry


class CountrySelectField(SelectField):
    def __init__(self, *args, **kwargs):
        super(CountrySelectField, self).__init__(*args, **kwargs)
        self.choices = [('1', 'Pick a country')]
        self.choices += [(country.name, country.name) for country in pycountry.countries]

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class FilterFlightsForm(FlaskForm):
    from_city = StringField('From City', validators=[DataRequired()])
    to_city = StringField('To City', validators=[DataRequired()])
    submit = SubmitField('Search')

class TripsCountryForm(FlaskForm):
    country = StringField('Country', render_kw={"placeholder": "Enter the country"})
    submit1 = SubmitField('Search by country')

class TripsDateForm(FlaskForm):
    date = DateField('Return', format='%Y-%m-%d')
    submit2 = SubmitField('Search by date')

class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Register')

class NewTripForm(FlaskForm):
    country = CountrySelectField('Country', validators=[DataRequired()], default="1")
    city = StringField('City', validators=[DataRequired()], render_kw={"placeholder": "Enter the destination city"})
    reason = RadioField('Type', choices=[('business', 'Business'), ('leisure', 'Leisure')], validators=[DataRequired()])
    departure_date = DateField('Departure', format='%Y-%m-%d')
    return_date = DateField('Return', format='%Y-%m-%d')
    photos = MultipleFileField('Photos')
    submit = SubmitField('Add trip')

class NewFlightTicketForm(FlaskForm):
    trip = SelectField('Associated trip', coerce=int)
    flight_no = StringField('Flight Number', validators=[DataRequired()], render_kw={"placeholder": "Enter the flight number"})
    departure_date = DateField('Departure date', format='%Y-%m-%d')
    departure_hour = StringField('Departure hour', validators=[DataRequired()], render_kw={"placeholder": "hh:mm"})
    arrival_date = DateField('Arrival date', format='%Y-%m-%d')
    arrival_hour = StringField('Arrival hour', validators=[DataRequired()], render_kw={"placeholder": "hh:mm"})
    from_city = StringField('From airport', validators=[DataRequired()])
    to_city = StringField('To airport', validators=[DataRequired()])
    submit = SubmitField('Add ticket')