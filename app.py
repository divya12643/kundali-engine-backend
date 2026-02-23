from flask import Flask, request, jsonify
from skyfield.api import load, Topos
from skyfield.framelib import ecliptic_frame

app = Flask(__name__)

ts = load.timescale()
planets = None  # Delay loading

def get_planets():
    global planets
    if planets is None:
        planets = load('de421.bsp')
    return planets

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

    eph = get_planets()
    earth = eph['earth']

    bodies = {
        "sun": eph['sun'],
        "moon": eph['moon'],
        "mars": eph['mars'],
        "mercury": eph['mercury'],
        "venus": eph['venus'],
        "jupiter": eph['jupiter barycenter'],
        "saturn": eph['saturn barycenter']
    }

    results = {}

    for name, body in bodies.items():
        astrometric = earth.at(t).observe(body).apparent()
        lon_ecl, lat_ecl, distance = astrometric.frame_latlon(ecliptic_frame)
        results[name] = lon_ecl.degrees % 360

    # Rahu / Ketu (node approx)
    moon_state = earth.at(t).observe(eph['moon']).apparent()
    lon_ecl, lat_ecl, distance = moon_state.frame_latlon(ecliptic_frame)
    rahu = (lon_ecl.degrees - 180) % 360
    ketu = (rahu + 180) % 360

    results["rahu"] = rahu
    results["ketu"] = ketu

    # Ascendant (LST)
    gmst = t.gmst
    lst = (gmst * 15 + lon) % 360
    ascendant = lst

    return jsonify({
        "planets": results,
        "ascendant": ascendant
    })
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
