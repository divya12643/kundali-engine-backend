from flask import Flask, request, jsonify
import swisseph as swe

app = Flask(__name__)

swe.set_sid_mode(swe.SIDM_LAHIRI)

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

    jd = swe.julday(year, month, day, hour)

    planets = {}

    ids = {
        "sun": swe.SUN,
        "moon": swe.MOON,
        "mars": swe.MARS,
        "mercury": swe.MERCURY,
        "venus": swe.VENUS,
        "jupiter": swe.JUPITER,
        "saturn": swe.SATURN,
        "rahu": swe.TRUE_NODE
    }

    for name, pid in ids.items():
        lon_val = swe.calc_ut(jd, pid, swe.FLG_SIDEREAL)[0][0]
        planets[name] = lon_val % 360

    planets["ketu"] = (planets["rahu"] + 180) % 360

    # Correct Ascendant
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SIDEREAL)
    ascendant = ascmc[0] % 360

    return jsonify({
        "planets": planets,
        "ascendant": ascendant
    })

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
