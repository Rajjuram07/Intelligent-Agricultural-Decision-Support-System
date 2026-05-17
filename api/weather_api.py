import requests

from utils.config import (
    WEATHER_API_KEY
)


# =========================================================
# GET CURRENT WEATHER
# =========================================================
def get_weather(city):

    try:

        url = (
            "http://api.weatherapi.com/v1/current.json"
        )

        params = {

            "key": WEATHER_API_KEY,

            "q": city,

            "aqi": "yes"
        }

        response = requests.get(

            url,

            params=params
        )

        data = response.json()

        # =============================================
        # ERROR HANDLING
        # =============================================
        if "error" in data:

            return {
                "error": data["error"]["message"]
            }

        current = data["current"]

        location = data["location"]

        return {

            "city": location["name"],

            "country": location["country"],

            "temperature": current["temp_c"],

            "humidity": current["humidity"],

            "wind_speed": current["wind_kph"],

            "weather": current["condition"]["text"],

            "air_quality": current.get(
                "air_quality",
                {}
            )
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# =========================================================
# GENERATE WEATHER ADVISORY
# =========================================================
def generate_weather_advisory(weather):

    try:

        temperature = weather[
            "temperature"
        ]

        humidity = weather[
            "humidity"
        ]

        condition = weather[
            "weather"
        ]

        advisory = f"""

        Current Weather Analysis:

        - Temperature:
        {temperature}°C

        - Humidity:
        {humidity}%

        - Condition:
        {condition}

        Agricultural Advisory:

        """

        # =============================================
        # HEAT ANALYSIS
        # =============================================
        if temperature > 40:

            advisory += """
            - Extreme heat conditions detected.
            - Increase irrigation frequency.
            - Avoid fertilizer spraying during daytime.
            """

        elif temperature > 30:

            advisory += """
            - Warm conditions are suitable for many crops.
            - Maintain adequate soil moisture.
            """

        else:

            advisory += """
            - Temperature conditions are stable.
            """

        # =============================================
        # HUMIDITY ANALYSIS
        # =============================================
        if humidity > 80:

            advisory += """
            - High humidity may increase fungal disease risk.
            """

        return advisory

    except Exception as e:

        return f"""
        Advisory generation failed:
        {str(e)}
        """