from rag.retriever import (
    retrieve_context
)

from ml_models.advanced_predictor import (
    predict_crop_yield
)

from rag.entity_extractor import (
    extract_entities
)

from api.weather_api import (
    get_weather
)

from api.advanced_weather import (
    get_weather_forecast
)


# =========================================================
# GENERATE AGRICULTURAL INSIGHTS
# =========================================================
def generate_agriculture_insights(
    prediction,
    current_weather,
    crop,
    season
):

    insights = []

    # =====================================================
    # YIELD INSIGHTS
    # =====================================================
    if prediction:

        if prediction >= 4:

            insights.append(
                "High productivity conditions detected."
            )

        elif prediction >= 2:

            insights.append(
                "Moderate agricultural productivity expected."
            )

        else:

            insights.append(
                "Lower yield conditions detected."
            )

    # =====================================================
    # CURRENT WEATHER INSIGHTS
    # =====================================================
    if current_weather:

        try:

            temperature = current_weather.get(
                "temperature"
            )

            humidity = current_weather.get(
                "humidity"
            )

            if temperature:

                if temperature > 35:

                    insights.append(
                        "High temperature stress may affect crops."
                    )

                elif temperature < 10:

                    insights.append(
                        "Low temperatures may slow crop growth."
                    )

            if humidity:

                if humidity > 80:

                    insights.append(
                        "High humidity may increase disease risk."
                    )

        except Exception:

            pass

    # =====================================================
    # SEASON INSIGHTS
    # =====================================================
    if season:

        if season.lower() == "kharif":

            insights.append(
                "Rainfall management is important during Kharif season."
            )

        elif season.lower() == "rabi":

            insights.append(
                "Irrigation planning is important during Rabi season."
            )

    # =====================================================
    # CROP INSIGHTS
    # =====================================================
    if crop:

        insights.append(
            f"{crop} cultivation analysis completed."
        )

    return insights


# =========================================================
# GENERATE WEATHER SUMMARY
# =========================================================
def generate_weather_summary(
    current_weather,
    forecast_weather
):

    summary = []

    # =====================================================
    # CURRENT WEATHER
    # =====================================================
    if current_weather:

        try:

            temperature = current_weather.get(
                "temperature"
            )

            humidity = current_weather.get(
                "humidity"
            )

            condition = current_weather.get(
                "weather"
            )

            summary.append(
                f"Current temperature is "
                f"{temperature}°C with "
                f"{condition} conditions."
            )

            summary.append(
                f"Current humidity level is "
                f"{humidity}%."
            )

        except Exception:

            pass

    # =====================================================
    # FORECAST WEATHER
    # =====================================================
    if forecast_weather:

        try:

            heat_risk = forecast_weather.get(
                "heat_risk"
            )

            rainfall_risk = forecast_weather.get(
                "rainfall_risk"
            )

            humidity_risk = forecast_weather.get(
                "humidity_risk"
            )

            max_temperature = (
                forecast_weather.get(
                    "max_forecast_temperature"
                )
            )

            total_rainfall = (
                forecast_weather.get(
                    "total_forecast_rainfall"
                )
            )

            summary.append(
                f"Maximum forecast temperature "
                f"may reach {max_temperature}°C."
            )

            summary.append(
                f"Expected rainfall over the "
                f"next 7 days is "
                f"{total_rainfall} mm."
            )

            if heat_risk == "High":

                summary.append(
                    "High heat stress conditions "
                    "are expected."
                )

            if rainfall_risk == "High":

                summary.append(
                    "Heavy rainfall conditions "
                    "may affect cultivation."
                )

            if humidity_risk == "High":

                summary.append(
                    "High humidity may increase "
                    "crop disease risk."
                )

        except Exception:

            pass

    return summary


# =========================================================
# AGRICULTURAL ANALYSIS ENGINE
# =========================================================
def intelligent_agriculture_analysis(
    question
):

    # =====================================================
    # EXTRACT ENTITIES
    # =====================================================
    entities = extract_entities(
        question
    )

    # =====================================================
    # ENTITY VALUES
    # =====================================================
    state = entities["state"]

    district = entities["district"]

    crop = entities["crop"]

    crop_type = (
        entities["crop_type"]
        or "Cereals"
    )

    season = (
        entities["season"]
        or "Kharif"
    )

    year = (
        entities["year"]
        or 2023
    )

    # =====================================================
    # DEFAULT VALUES
    # =====================================================
    area = 1000

    production = 5000

    prediction = None

    current_weather = None

    forecast_weather = None

    # =====================================================
    # RAG CONTEXT
    # =====================================================
    context = retrieve_context(
        question
    )

    # =====================================================
    # CURRENT WEATHER
    # =====================================================
    if state:

        try:

            current_weather = get_weather(
                state
            )

        except Exception:

            current_weather = None

    # =====================================================
    # FORECAST WEATHER
    # =====================================================
    if state:

        try:

            forecast_weather = get_weather_forecast(
                state
            )

        except Exception:

            forecast_weather = None

    # =====================================================
    # ML PREDICTION
    # =====================================================
    if state and crop:

        try:

            prediction = predict_crop_yield(
                year=year,
                state=state,
                district=district or "Unknown",
                crop=crop,
                crop_type=crop_type,
                season=season,
                area=area,
                production=production
            )

        except Exception:

            prediction = None

    # =====================================================
    # GENERATE INSIGHTS
    # =====================================================
    insights = generate_agriculture_insights(
        prediction,
        current_weather,
        crop,
        season
    )

    # =====================================================
    # WEATHER SUMMARY
    # =====================================================
    weather_summary = generate_weather_summary(
        current_weather,
        forecast_weather
    )

    # =====================================================
    # RETURN RESULTS
    # =====================================================
    return {
        "context": context,
        "prediction": prediction,
        "state": state,
        "district": district,
        "crop": crop,
        "crop_type": crop_type,
        "season": season,
        "year": year,
        "current_weather": current_weather,
        "forecast_weather": forecast_weather,
        "weather_summary": weather_summary,
        "insights": insights
    }