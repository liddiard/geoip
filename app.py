import os

import geoip2.webservice    
from flask import Flask, request
from flask_caching import Cache
from flask_cors import CORS
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
CORS(app, origins=[
    'https://cdpn.io' # codepen.io user code domain
])

# --- Flask-Caching configuration ---
cache = Cache(app, config={
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 60 * 60 * 24 * 30  # 30 days
})

ACCOUNT_ID = os.getenv("MAXMIND_ACCOUNT_ID")
LICENSE_KEY = os.getenv("MAXMIND_LICENSE_KEY")

if not ACCOUNT_ID or not LICENSE_KEY:
    raise RuntimeError("Set MAXMIND_ACCOUNT_ID and MAXMIND_LICENSE_KEY environment variables.")


def get_geo_info(ip_address):
    """
    Query MaxMind GeoLite/GeoIP web service for geolocation data.
    """
    # Using the GeoLite web service host. Change host="geoip.maxmind.com" for GeoIP.
    with geoip2.webservice.Client(ACCOUNT_ID, LICENSE_KEY, host="geolite.info") as client:
        try:
            response = client.city(ip_address)
            return {
                "ip": ip_address,
                "country_name": response.country.name,
                "country_iso_code": response.country.iso_code,
                "city_name": response.city.name,
                "latitude": response.location.latitude,
                "longitude": response.location.longitude
            }
        except:
            return {"error": f"IP address {ip_address} not found in GeoIP database."}


@app.route("/", methods=["GET"])
@cache.cached(make_cache_key=lambda: request.headers.get("X-Forwarded-For", request.remote_addr))
def index():
    """
    Returns geolocation info for the user's IP address like:
    {
        "city_name": "Brooklyn",
        "country_iso_code": "US",
        "country_name": "United States",
        "ip": "75.219.240.157",
        "latitude": 40.6462,
        "longitude": -73.9559
    }
    """
    user_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    geo_info = get_geo_info(user_ip)
    status_code = 200
    if "error" in geo_info:
        status_code = 400
    return geo_info, status_code



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)