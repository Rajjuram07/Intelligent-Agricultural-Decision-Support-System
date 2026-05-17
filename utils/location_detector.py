import geocoder


# =========================================================
# DETECT USER LOCATION
# =========================================================
def detect_location():

    try:

        g = geocoder.ip("me")

        city = g.city

        state = g.state

        country = g.country

        latitude = g.latlng[0]

        longitude = g.latlng[1]

        return {

            "city": city,

            "state": state,

            "country": country,

            "latitude": latitude,

            "longitude": longitude
        }

    except Exception:

        return {
            "city": "Unknown",
            "state": "Unknown",
            "country": "Unknown",
            "latitude": None,
            "longitude": None
        }