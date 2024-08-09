#!/usr/bin/env python3

from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def main():
    return '''
     <form action="/echo_user_input" method="POST">
        <label for="start_date">Start Date:</label>
        <input type="date" id="start_date" name="start_date" required>
        
        <label for="city">City:</label>
        <input type="text" id="city" name="city" required>
        
        <input type="submit" value="Submit!">
     </form>
     '''


@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    input_date = request.form.get("start_date", "")
    input_city = request.form.get("city", "")
    return "Your flight date is " + input_date + " and the city you are flying out of is " + input_city
