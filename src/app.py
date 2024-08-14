#!/usr/bin/env python3
import os
import requests
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Construct the path for the SQLite database file
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'Flights.sqlite3')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db = SQLAlchemy(app)


# Define the database model to store Flights data
class Flights(db.Model):
    datetime = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow())
    prices = db.Column(db.Integer, nullable=False)


# # Define a route for the home page with a form
@app.route("/")
def home():
    return '''
     <form action="/get_flights" method="POST">
         <label for="city">Departure Airport Code (3-letter code i.e-AUS):</label>
         <input name="city" id="city" required>
         <label for="arr_city">Arrival Airport Code (3-letter code i.e-CDG):</label>
         <input name="arr_city" id="arr_city" required>
         <label for="departure_date">Departure Date:</label>
         <input type="date" name="departure_date" id="departure_date" required>
         <label for="return_date">Return Date:</label>
         <input type="date" name="return_date" id="return_date" required>
         <input type="submit" value="Submit!">
     </form>
     '''


# Helper function to get flight data using the API
def fetch_flights(city, arr_city, departure_date, return_date):
    # Reformat the dates to YYYY-MM-DD
    departure_date = datetime.strptime(departure_date, "%Y-%m-%d").strftime("%Y-%m-%d")
    return_date = datetime.strptime(return_date, "%Y-%m-%d").strftime("%Y-%m-%d")

    try:
        response = requests.get(
            f"https://serpapi.com/search.json?engine=google_flights&departure_id={city}&arrival_id={arr_city}&outbound_date={departure_date}&return_date={return_date}&currency=USD&hl=en&api_key=cc91e78a02a72c54e7a74408269f81ba7cca55d5c32605079e41023081b8bc0d")
        json_data = response.json()

        if "best_flights" in json_data and json_data["best_flights"]:
            best_flight = json_data["best_flights"][0]
            price = best_flight["price"]
            return price
        else:
            return "No flights available"
    except requests.RequestException as e:
        return f"API request error: {str(e)}"


# Define a route to handle the form submission and display the flight details
@app.route("/get_flights", methods=["POST"])
def get_flights():
    city = request.form.get("city")
    arr_city = request.form.get("arr_city")
    departure_date = request.form.get("departure_date")
    return_date = request.form.get("return_date")

    flight_cost = fetch_flights(city, arr_city, departure_date, return_date)
    departure_date_obj = datetime.strptime(departure_date, "%Y-%m-%d")

    # Append database
    with app.app_context():
        db.create_all()
        new_entry = Flights(datetime=departure_date_obj, prices=flight_cost)
        db.session.add(new_entry)
        db.session.commit()

    return f"Best flight out from {city} to {arr_city} on {departure_date} costs ${flight_cost}!"


# Run the app
if __name__ == "__main__":
    get_flights()
