import requests

from utils.config import (
    WEATHER_API_KEY
)


# =========================================================
# GET ADVANCED WEATHER FORECAST
# =========================================================
def get_weather_forecast(city):

    url = (
        f"http://api.weatherapi.com/v1/forecast.json"
        f"?key={WEATHER_API_KEY}"
        f"&q={city},India"
        f"&days=7"
        f"&aqi=yes"
        f"&alerts=yes"
    )

    try:

        response = requests.get(url)

        data = response.json()

        # =============================================
        # BASIC CURRENT WEATHER
        # =============================================
        current = data["current"]

        location = data["location"]

        forecast_days = data["forecast"]["forecastday"]

        # =============================================
        # AGRICULTURAL ANALYSIS
        # =============================================
        rainfall_risk = "Low"

        heat_risk = "Low"

        humidity_risk = "Low"

        total_rainfall = 0

        max_temperature = 0

        avg_humidity = 0

        humidity_count = 0

        for day in forecast_days:

            day_data = day["day"]

            rainfall = day_data["totalprecip_mm"]

            total_rainfall += rainfall

            temp = day_data["maxtemp_c"]

            if temp > max_temperature:

                max_temperature = temp

            humidity = day_data["avghumidity"]

            avg_humidity += humidity

            humidity_count += 1

        # =============================================
        # AVERAGES
        # =============================================
        avg_humidity = (
            avg_humidity / humidity_count
        )

        # =============================================
        # RAIN ANALYSIS
        # =============================================
        if total_rainfall > 50:

            rainfall_risk = "High"

        elif total_rainfall > 20:

            rainfall_risk = "Moderate"

        # =============================================
        # HEAT ANALYSIS
        # =============================================
        if max_temperature > 38:

            heat_risk = "High"

        elif max_temperature > 32:

            heat_risk = "Moderate"

        # =============================================
        # HUMIDITY ANALYSIS
        # =============================================
        if avg_humidity > 85:

            humidity_risk = "High"

        elif avg_humidity > 70:

            humidity_risk = "Moderate"

        # =============================================
        # RETURN CLEAN DATA
        # =============================================
        return {

            "city": location["name"],

            "region": location["region"],

            "country": location["country"],

            "temperature": current["temp_c"],

            "condition": current["condition"]["text"],

            "humidity": current["humidity"],

            "wind_speed": current["wind_kph"],

            "air_quality_index":
            current["air_quality"]["us-epa-index"],

            "total_forecast_rainfall":
            round(total_rainfall, 2),

            "max_forecast_temperature":
            max_temperature,

            "average_humidity":
            round(avg_humidity, 2),

            "rainfall_risk":
            rainfall_risk,

            "heat_risk":
            heat_risk,

            "humidity_risk":
            humidity_risk
        }

    except Exception as e:

        return {
            "error": str(e)
        }