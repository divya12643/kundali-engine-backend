from flask import Flask, request, jsonify
from skyfield.api import load, Topos
from skyfield.framelib import ecliptic_frame
import numpy as np

app = Flask(__name__)

ts = load.timescale()
planets = load('de440.bsp')

@app.route('/')
def home():
    return "Professional Kundali Engine Running"

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

   bodies = {
    "sun": planets['sun'],
    "moon": planets['moon'],
    "mars": planets['mars barycenter'],
    "mercury": planets['mercury barycenter'],
    "venus": planets['venus barycenter'],
    "jupiter": planets['jupiter barycenter'],
    "saturn": planets['saturn barycenter']
}

    results = {}

    for name, body in bodies.items():
        astrometric = earth.at(t).observe(body).apparent()
        lon, lat_ecl, distance = astrometric.frame_latlon(ecliptic_frame)
        results[name] = lon.degrees % 360

    # True Node (Rahu) approximation using Moon node
    moon_orbit = planets['moon']
    moon_state = earth.at(t).observe(moon_orbit).apparent()
    lon, lat_ecl, distance = moon_state.frame_latlon(ecliptic_frame)
    rahu = (lon.degrees - 180) % 360
    ketu = (rahu + 180) % 360

    results["rahu"] = rahu
    results["ketu"] = ketu

    # Ascendant
    observer = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)
    astrometric = observer.at(t).observe(planets['sun'])
    alt, az, distance = astrometric.apparent().altaz()

    # Local Sidereal Time
    gst = t.gmst
    lst = (gst * 15 + lon) % 360
    ascendant = lst % 360

    return jsonify({
        "planets": results,
        "ascendant": ascendant
    })
