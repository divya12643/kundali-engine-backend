from flask import Flask, request, jsonify
from skyfield.api import load, Topos
from skyfield.framelib import ecliptic_frame

app = Flask(__name__)

ts = load.timescale()
load('de421.bsp')

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
        lon_ecl, lat_ecl, distance = astrometric.frame_latlon(ecliptic_frame)
        results[name] = lon_ecl.degrees % 360

    # Rahu / Ketu (node approx)
    moon_state = earth.at(t).observe(planets['moon']).apparent()
    lon_ecl, lat_ecl, distance = moon_state.frame_latlon(ecliptic_frame)
    rahu = (lon_ecl.degrees - 180) % 360
    ketu = (rahu + 180) % 360

    results["rahu"] = rahu
    results["ketu"] = ketu

    # Ascendant (simple LST method)
    observer = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)
    gmst = t.gmst
    lst = (gmst * 15 + lon) % 360
    ascendant = lst

    return jsonify({
        "planets": results,
        "ascendant": ascendant
    })
