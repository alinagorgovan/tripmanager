from flask import Flask, jsonify, request
import mysql.connector


app = Flask(__name__)

class dbConnection():
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="db",
            port="3306",
            user="root",
            passwd="root",
            database="trip_manager"
        )
        self.db_cursor = self.mydb.cursor()
    
    def register(self, email, firstname, lastname, passwd):
        args = [email, firstname, lastname, passwd]
        print(args)
        ret = self.db_cursor.callproc('Register', args)
        return self.login(email, passwd)

    def login(self, email, passwd):
        ret = self.db_cursor.callproc('LogIn', [email, passwd])
        for result in self.db_cursor.stored_results():
            t = result.fetchall()[0]
            return {'id' : t[0],
                    'email' : t[1],
                    'firstname' : t[2],
                    'lastname' : t[3]}
        
        return None
        
    def get_users(self):
        self.db_cursor.callproc('get_users')
        users = []
        for result in self.db_cursor.stored_results():
            for t in result.fetchall():
                users.append( {'id' : t[0],
                        'email' : t[1],
                        'firstname' : t[2],
                        'lastname' : t[3]})
        
        return users


    def add_trip(self, user_id, country, city, departure_date, return_date):
        args = [user_id, country, city, departure_date, return_date]
        ret = self.db_cursor.callproc('add_trip', args)
        print(ret)
        for result in self.db_cursor.stored_results():
            return result.fetchall()[0][0]
        
        return None

    def add_flight(self, trip_id, flight_number, departure_time, arrival_time, from_city, to_city):
        args = [trip_id, flight_number, departure_time, arrival_time, from_city, to_city]
        self.db_cursor.callproc('add_flight', args)

    def add_picture(self, trip_id, path):
        args = [trip_id, path]
        self.db_cursor.callproc('add_photo', args)

    def log(self, message):
        self.db_cursor.callproc('add_log', [message])

    def get_trips(self, user_id):
        self.db_cursor.callproc('GetTrips', [user_id])
        trips = []
        for result in self.db_cursor.stored_results():
            for t in result.fetchall():
                trips.append([t[0], t[2], t[3], t[5], t[6]])
        
        return trips

    def get_trips_country(self, user_id, country):
        self.db_cursor.callproc('GetTripsCountry', [user_id, country])
        trips = []
        for result in self.db_cursor.stored_results():
            for t in result.fetchall():
                print(t)
                trips.append([t[0], t[2], t[3], t[5], t[6]])
        return trips

    def get_trips_date(self, user_id, date):
        self.db_cursor.callproc('GetTripsDate', [user_id, date])
        trips = []
        for result in self.db_cursor.stored_results():
            for t in result.fetchall():
                trips.append([t[0], t[2], t[3], t[5], t[6]])
        
        return trips

    def get_flights_user(self, user_id):
        self.db_cursor.callproc('GetFlightsUser', [user_id])
        flights = []
        for result in self.db_cursor.stored_results():
            for t in result.fetchall():
                flights.append([t[0], t[1], t[2], t[3], t[4], t[5], t[6]])
        return flights

    def get_flights_trip(self, trip_id):
        self.db_cursor.callproc('GetFlightsTrip', [trip_id])
        flights = []
        for result in self.db_cursor.stored_results():
            for t in result.fetchall():
                flights.append([t[0], t[1], t[2], t[3], t[4], t[5], t[6]])
        return flights

    def get_flights_filter(self, user_id, from_city, to_city):
        self.db_cursor.callproc('GetFlightsFromTo', [user_id, from_city, to_city])
        flights = []
        for result in self.db_cursor.stored_results():
            for t in result.fetchall():
                flights.append([t[0], t[1], t[2], t[3], t[4], t[5], t[6]])
        return flights

    def get_next_trips(self, user_id):
        self.db_cursor.callproc('NextTrips', [user_id])
        trips = []
        for result in self.db_cursor.stored_results():
            for t in result.fetchall():
                trips.append([t[0], t[2], t[3], t[5], t[6]])
        
        return trips

    def get_previous_trips(self, user_id):
        self.db_cursor.callproc('PreviousTrips', [user_id])
        trips = []
        for result in self.db_cursor.stored_results():
            for t in result.fetchall():
                trips.append([t[0], t[2], t[3], t[5], t[6]])
        
        return trips
    
    def get_most_visited_countries(self):
        self.db_cursor.callproc('MostVisitedCountries')
        countries = {}
        for result in self.db_cursor.stored_results():
            for t in result.fetchall():
                countries[t[0]] = t[1]
        
        return countries

    def get_top_rated_trips(self, user_id):
        self.db_cursor.callproc('TopRatedTrips', [user_id])
        trips = []
        for result in self.db_cursor.stored_results():
            for t in result.fetchall():
                trips.append([t[0], t[2], t[3], t[5], t[6]])
        
        return trips

    def get_trip_choices(self, user_id):
        self.db_cursor.callproc('GetTrips', [user_id])
        trips = []
        for result in self.db_cursor.stored_results():
            for t in result.fetchall():
                trips.append((t[0], t[6] + ", " + t[5] + "  "  + t[2].strftime("%m/%d/%Y")))
        
        return trips

    def get_pictures(self, trip_id):
        self.db_cursor.callproc('GetPictures', [trip_id])
        photos = []
        for result in self.db_cursor.stored_results():
            for t in result.fetchall():
                photos.append([t[0], t[1], t[2]])
        
        return photos
        
    def delete_user(self, user_id):
        sql_delete_query = f"delete from users where user_id = {user_id};"
        self.db_cursor.execute(sql_delete_query)
        self.mydb.commit()


def init():
    mydb = mysql.connector.connect(
        host="db",
        port="3306",
        user="root",
        passwd="root",
        database="trip_manager",
        autocommit=True
    )

    db_cursor = mydb.cursor()

    r = db_cursor.execute(
        """
        create database if not exists trip_manager;
        use trip_manager;
        drop table if exists log;
        drop table if exists pictures;
        drop table if exists plane_tickets;
        drop table if exists trips;
        drop table if exists users;


        create table if not exists log (
            message text,
            log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );

        create table if not exists users (
            user_id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(50) UNIQUE,
            firstname VARCHAR(30) NOT NULL,
            lastname VARCHAR(30) NOT NULL,
            passwd varchar(30) NOT NULL
        );

        create table if not exists trips (
            trip_id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            user_id INT(6) UNSIGNED,
            departure_date DATE,
            return_date DATE,
            rating INT UNSIGNED,
            country VARCHAR(20) NOT NULL,
            city VARCHAR(20) NOT NULL,
            foreign key (user_id) references users(user_id) ON DELETE SET NULL
        );

        create table if not exists plane_tickets (
            ticket_id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            trip_id INT(6) UNSIGNED,
            filght_number varchar(20),
            departure_time DATETIME,
            arrival_time DATETIME,
            from_city varchar(100) not null,
            to_city varchar(100) not null,
            foreign key (trip_id) references trips(trip_id) ON DELETE SET NULL
        );

        create table if not exists pictures (
            picture_id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            trip_id INT(6) UNSIGNED,
            path varchar(50),
            foreign key (trip_id) references trips(trip_id) ON DELETE SET NULL
        );


        DROP PROCEDURE IF EXISTS LogIn;
        DROP PROCEDURE IF EXISTS GetTrips;
        DROP PROCEDURE IF EXISTS GetPictures;
        DROP PROCEDURE IF EXISTS GetFlightsUser;
        DROP PROCEDURE IF EXISTS GetFlightsTrip;
        DROP FUNCTION IF EXISTS no_of_trips;
        DROP FUNCTION IF EXISTS no_of_flights;
        DROP PROCEDURE IF EXISTS NextTrips;
        DROP PROCEDURE IF EXISTS PreviousTrips;
        DROP PROCEDURE IF EXISTS MostVisitedCountries;
        DROP PROCEDURE IF EXISTS Register;
        DROP PROCEDURE IF EXISTS TopRatedTrips;
        DROP PROCEDURE IF EXISTS add_trip;
        DROP PROCEDURE IF EXISTS add_flight;
        DROP PROCEDURE IF EXISTS add_log;
        DROP PROCEDURE IF EXISTS add_photo;
        DROP PROCEDURE IF EXISTS GetFlightsFromTo;
        DROP PROCEDURE IF EXISTS GetTripsCountry;
        DROP PROCEDURE IF EXISTS GetTripsDate;
        DROP PROCEDURE IF EXISTS get_users;

        CREATE PROCEDURE LogIn(
            IN email_p varchar(100),
            IN passwd_p varchar(100))
        BEGIN
            SELECT * from users where users.email=email_p and users.passwd=passwd_p;
        END;
        
        CREATE PROCEDURE get_users()
        BEGIN
            SELECT * from users;
        END;

        CREATE PROCEDURE GetTrips(
            IN user_id_p INT(6))
        BEGIN
            SELECT * from trips where user_id=user_id_p;
        END;

        CREATE PROCEDURE GetPictures(
            IN trip_id_p INT(6))
        BEGIN
            SELECT * from pictures where trip_id=trip_id_p;
        END;

        CREATE PROCEDURE GetFlightsUser(
            IN user_id_p INT(6))
        BEGIN
            SELECT * from plane_tickets p inner join trips t on t.trip_id=p.trip_id where t.user_id=user_id_p;
        END;

        CREATE PROCEDURE GetFlightsTrip(
            IN trip_id_p INT(6))
        BEGIN
            SELECT * from plane_tickets where trip_id=trip_id_p;
        END;

        CREATE FUNCTION no_of_trips(user_id_p INT) RETURNS int
        BEGIN
            DECLARE result int;
            Select count(*) into result from trips where user_id=user_id_p;
            RETURN result;
        END;

        CREATE FUNCTION no_of_flights(user_id_p INT) RETURNS int
        BEGIN
            DECLARE result int;
            Select count(*) into result from plane_tickets p inner join trips t on p.trip_id=t.trip_id where t.user_id=user_id_p;
            RETURN result;
        END;

        CREATE PROCEDURE NextTrips(
            IN user_id_p INT(6))
        BEGIN
            SELECT * from trips where user_id=user_id_p and departure_date > CURDATE();
        END;

        CREATE PROCEDURE PreviousTrips(
            IN user_id_p INT(6))
        BEGIN
            SELECT * from trips where user_id=user_id_p and departure_date < CURDATE();
        END;

        CREATE PROCEDURE MostVisitedCountries()
        BEGIN
            SELECT country, count(*) as c from trips
            group by country
            order by c DESC;
        END;

        CREATE PROCEDURE TopRatedTrips(
            IN user_id_p INT(6))
        BEGIN
            SELECT * from trips where user_id=user_id_p order by rating;
        END;


        CREATE PROCEDURE Register (
            email varchar(50),
            firstname varchar(30),
            lastname varchar(30),
            passwd varchar(30))
        BEGIN
            start transaction;
            insert into users (email, firstname, lastname, passwd) values (email, firstname, lastname, passwd);
            commit;
        END;

        CREATE PROCEDURE add_trip (
            user_id INT,
            country varchar(20),
            city varchar(20),
            departure_date DATE,
            return_date DATE)
        BEGIN
            start transaction;
            insert into trips (user_id, country, city, departure_date, return_date) values (user_id, country, city, departure_date, return_date);
            commit;
            SELECT LAST_INSERT_ID() as 'trip_id' from trips;
        END;

        CREATE PROCEDURE add_flight (
            trip_id INT,
            flight_number varchar(20),
            departure_time DATETIME,
            arrival_time DATETIME,
            from_city varchar(100),
            to_city varchar(100))
        BEGIN
            start transaction;
            insert into plane_tickets (trip_id, filght_number, departure_time, arrival_time, from_city, to_city)
                values (trip_id, flight_number, departure_time, arrival_time, from_city, to_city);
            commit;
        END;

        CREATE PROCEDURE add_log (
            message TEXT)
        BEGIN
            start transaction;
            insert into log (message) values (message);
            commit;
        END;

        CREATE PROCEDURE add_photo (
            trip_id INT,
            path varchar(255))
        BEGIN
            start transaction;
            insert into pictures (trip_id, path) values (trip_id, path);
            commit;
        END;

        CREATE PROCEDURE GetTripsCountry(
            IN user_id_p INT(6), country_p varchar(100))
        BEGIN
            SELECT * from trips where user_id=user_id_p and country=country_p;
        END;

        CREATE PROCEDURE GetTripsDate(
            IN user_id_p INT(6), dep_date DATE)
        BEGIN
            SELECT * from trips where user_id=user_id_p and departure_date > dep_date;
        END;

        CREATE PROCEDURE GetFlightsFromTo(
            IN user_id_p INT(6), from_city_p varchar(100), to_city_p varchar(100))
        BEGIN
            SELECT * from plane_tickets p inner join trips t on t.trip_id=p.trip_id where t.user_id=user_id_p and p.from_city=from_city_p
            and p.to_city=to_city_p;
        END;

        DROP TRIGGER IF EXISTS log_info;
        DROP TRIGGER IF EXISTS log_info_user;
        DROP TRIGGER IF EXISTS log_info_flight;


        CREATE TRIGGER log_info BEFORE INSERT ON trips
        FOR EACH ROW
            INSERT INTO log (message) values (concat("New trip added to ", NEW.city,",", NEW.country));

        CREATE TRIGGER log_info_user BEFORE INSERT ON users
        FOR EACH ROW
            INSERT INTO log (message) values (concat("New user added ", NEW.email));

        CREATE TRIGGER log_info_flight BEFORE INSERT ON plane_tickets
        FOR EACH ROW
            INSERT INTO log (message) values (concat("New plane ticket added ", NEW.filght_number));

        insert into users (email, passwd, firstname, lastname) values ("alina.gorgovan98@gmail.com", "parola1", "Alina", "Gorgovan");
        insert into users (email, passwd, firstname, lastname) values ("alina.valentina98@gmail.com", "parola2", "Alina", "Gorgovan");
        insert into trips (user_id, country, city, departure_date, return_date) values (1, "France", "Nice", "2020-01-01", "2020-01-05");
        insert into trips (user_id, country, city, departure_date, return_date) values (1, "France", "Paris", "2020-01-01", "2020-01-05");
        insert into trips (user_id, country, city, departure_date, return_date) values (1, "Spain", "Barcelona", "2020-05-02", "2020-05-06");
        insert into trips (user_id, country, city, departure_date, return_date) values (1, "Romania", "Cluj-Napoca", "2020-07-30", "2020-08-02");
        insert into trips (user_id, country, city, departure_date, return_date) values (1, "Romania", "Vama Veche", "2020-07-10", "2020-07-15");
        insert into plane_tickets (trip_id, filght_number, departure_time, arrival_time, from_city, to_city)
                values (2, "KLM1234", "2020-01-01 07:30:00", "2020-01-01 11:30:00", "Bucharest", "Paris");
        insert into plane_tickets (trip_id, filght_number, departure_time, arrival_time, from_city, to_city)
                values (2, "Tarom1234", "2020-01-05 13:30:00", "2020-01-05 16:30:00", "Paris", "Bucharest");
        insert into plane_tickets (trip_id, filght_number, departure_time, arrival_time, from_city, to_city)
                values (4, "KLM1111", "2020-05-02 07:30:00", "2020-05-02 11:30:00", "Bucharest", "Barcelona");
        insert into plane_tickets (trip_id, filght_number, departure_time, arrival_time, from_city, to_city)
                values (4, "KLM2222", "2020-05-06 13:30:00", "2020-05-06 16:30:00", "Barcelona", "Bucharest");


        """,
        multi=True)
    for result in r:
        if result.with_rows:
            print("Rows produced by statement '{}':".format(result.statement))
            print(result.fetchall())
        else:
            print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
    mydb.commit()
    db_cursor.close()
    mydb.close()


db_conn = dbConnection()


@app.route("/register", methods=["POST"])
def register():

    print(request.json)

    email = request.json['email']
    password = request.json['password']
    firstname = request.json['firstname']
    lastname = request.json['lastname']

    result = db_conn.register(email, firstname, lastname, password)

    return jsonify({
        'status' : 'Success',
        'reason' : 'Ok',
        'data' : result
    })

@app.route("/login", methods=["POST"])
def login():

    email = request.json['email']
    password = request.json['password']

    result = db_conn.login(email, password)

    return jsonify({
        'status' : 'Success',
        'reason' : 'Ok',
        'data' : result
    })

@app.route("/newtrip", methods=["POST"])
def add_trip():
    
    data = request.json

    result = db_conn.add_trip(data['user_id'], data['city'], data['country'], data['departure_date'], data['return_date'])
    
    if not result:
            return jsonify({
            'status' : 'Error',
            'reason' : 'Server error'
        }) 

    return jsonify({
        'status' : 'Success',
        'reason' : 'Ok',
        'data' : result
    })
    
@app.route("/newflight", methods=["POST"])
def add_flight():
    data = request.json

    db_conn.add_flight(data['trip_id'], data['flight_no'], data['departure_time'], data['arrival_time'], data['from_city'], data['to_city'])

    return jsonify({
        'status' : 'Success',
        'reason' : 'Ok',
    })
@app.route("/add_picture", methods=["POST"])
def add_picture():
        
    data = request.json

    db_conn.add_picture(data['trip_id'], data['path'])

    return jsonify({
        'status' : 'Success',
        'reason' : 'Ok',
    })

@app.route('/trips', methods={'GET', 'POST'})
def trips():
    trips = db_conn.get_trips(request.json['user_id'])
    for trip in trips:
        trip.append(db_conn.get_flights_trip(trip[0]))
        
    return jsonify({
        'status' : 'Success',
        'reason' : 'Ok',
        'trips' : trips
    })  
    
@app.route('/get_trip_choices', methods={'GET', 'POST'})
def get_trip_choices():
    trips = db_conn.get_trip_choices(request.json['user_id'])
        
    return jsonify({
        'status' : 'Success',
        'reason' : 'Ok',
        'trips' : trips
    }) 
    
@app.route('/flights', methods={'GET', 'POST'})
def flights():
    flights = db_conn.get_flights_user(request.json['user_id'])
        
    return jsonify({
        'status' : 'Success',
        'reason' : 'Ok',
        'flights' : flights
    })

@app.route('/statistics', methods={'GET'})
def statistics():
    stat = db_conn.get_most_visited_countries()
        
    return jsonify({
        'status' : 'Success',
        'reason' : 'Ok',
        'statistics' : stat
    })
    
@app.route('/users', methods={'GET'})
def users():
    result = db_conn.get_users()
        
    return jsonify({
        'status' : 'Success',
        'reason' : 'Ok',
        'users' : result
    }) 

@app.route('/delete_user', methods={'POST'})
def delete_user():
    db_conn.delete_user(request.json['user_id'])
        
    return jsonify({
        'status' : 'Success',
        'reason' : 'Ok',
    }) 
    

if __name__ == "__main__":
    init()
    app.run(host='0.0.0.0', port=5001, debug=True)

