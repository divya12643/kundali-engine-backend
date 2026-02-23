from flask import Flask, request, jsonify
from skyfield.api import load, Topos
from datetime import datetime

app = Flask(__name__)

ts = load.timescale()
planets = load('de440.bsp')

@app.route('/')
def home():
    return "Kundali Engine Running"

@app.route('/calculate')
def calculate():

    year = int(request.args.get('year'))
    month = int(request.args.get('month'))
    day = int(request.args.get('day'))
    hour = float(request.args.get('hour'))
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))

    t = ts.utc(year, month, day, hour)

    earth = planets['earth']
    moon = earth.at(t).observe(planets['moon']).apparent().ecliptic_latlon()
    sun = earth.at(t).observe(planets['sun']).apparent().ecliptic_latlon()

    return jsonify({
        "moon_longitude": moon[1].degrees,
        "sun_longitude": sun[1].degrees
    })
