import streamlit as st

import plotly.graph_objects as go

import plotly.express as px

import pandas as pd


# =========================================================
# SHOW AGRICULTURAL INSIGHTS
# =========================================================
def show_agriculture_insights(
    prediction,
    forecast_weather
):

    # =====================================================
    # SAFETY CHECK
    # =====================================================
    if not forecast_weather:

        st.warning(
            "Weather intelligence unavailable."
        )

        return

    # =====================================================
    # HEADER
    # =====================================================
    st.subheader(
        "Agricultural Intelligence Dashboard"
    )

    # =====================================================
    # EXTRACT WEATHER DATA
    # =====================================================
    heat_risk = forecast_weather.get(
        "heat_risk",
        "Unknown"
    )

    rainfall_risk = forecast_weather.get(
        "rainfall_risk",
        "Unknown"
    )

    humidity_risk = forecast_weather.get(
        "humidity_risk",
        "Unknown"
    )

    rainfall = float(
        forecast_weather.get(
            "total_forecast_rainfall",
            0
        )
    )

    temperature = float(
        forecast_weather.get(
            "max_forecast_temperature",
            0
        )
    )

    humidity = float(
        forecast_weather.get(
            "average_humidity",
            0
        )
    )

    # =====================================================
    # ADVANCED CROP HEALTH SCORE
    # =====================================================
    crop_health_score = 100

    # =====================================================
    # HEAT RISK IMPACT
    # =====================================================
    if heat_risk == "High":

        crop_health_score -= 30

    elif heat_risk == "Moderate":

        crop_health_score -= 15

    # =====================================================
    # RAINFALL RISK IMPACT
    # =====================================================
    if rainfall_risk == "High":

        crop_health_score -= 25

    elif rainfall_risk == "Moderate":

        crop_health_score -= 10

    # =====================================================
    # HUMIDITY RISK IMPACT
    # =====================================================
    if humidity_risk == "High":

        crop_health_score -= 15

    elif humidity_risk == "Moderate":

        crop_health_score -= 5

    # =====================================================
    # TEMPERATURE STRESS
    # =====================================================
    if temperature > 42:

        crop_health_score -= 15

    elif temperature > 36:

        crop_health_score -= 8

    # =====================================================
    # FINAL HEALTH NORMALIZATION
    # =====================================================
    crop_health_score = max(
        0,
        min(
            100,
            crop_health_score
        )
    )

    # =====================================================
    # HEALTH STATUS
    # =====================================================
    if crop_health_score >= 80:

        health_status = "Excellent"

    elif crop_health_score >= 60:

        health_status = "Good"

    elif crop_health_score >= 40:

        health_status = "Moderate"

    else:

        health_status = "Critical"

    # =====================================================
    # IRRIGATION NEED
    # =====================================================
    if rainfall < 5:

        irrigation_need = "Very High"

    elif rainfall < 20:

        irrigation_need = "High"

    elif rainfall < 50:

        irrigation_need = "Moderate"

    else:

        irrigation_need = "Low"

    # =====================================================
    # FLOOD RISK
    # =====================================================
    if rainfall > 120:

        flood_risk = "Severe"

    elif rainfall > 70:

        flood_risk = "High"

    elif rainfall > 30:

        flood_risk = "Moderate"

    else:

        flood_risk = "Low"

    # =====================================================
    # YIELD CLASSIFICATION
    # =====================================================
    try:

        prediction_value = float(
            prediction
        )

        if prediction_value >= 4:

            yield_status = "Excellent"

        elif prediction_value >= 2:

            yield_status = "Good"

        else:

            yield_status = "Low"

    except Exception:

        yield_status = "Moderate"

    # =====================================================
    # TOP METRICS
    # =====================================================
    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Crop Health",
            f"{crop_health_score}%"
        )

    with col2:

        st.metric(
            "Yield Outlook",
            yield_status
        )

    with col3:

        st.metric(
            "Flood Risk",
            flood_risk
        )

    with col4:

        st.metric(
            "Irrigation Need",
            irrigation_need
        )

    st.divider()

    # =====================================================
    # GAUGE CHART
    # =====================================================
    gauge = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=crop_health_score,

            title={
                "text": "Crop Health Score"
            },

            gauge={

                "axis": {
                    "range": [0, 100]
                },

                "bar": {
                    "thickness": 0.35
                },

                "steps": [

                    {
                        "range": [0, 40],
                        "color": "red"
                    },

                    {
                        "range": [40, 70],
                        "color": "orange"
                    },

                    {
                        "range": [70, 100],
                        "color": "green"
                    }
                ]
            }
        )
    )

    gauge.update_layout(
        height=500
    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

    # =====================================================
    # CLIMATE DATAFRAME
    # =====================================================
    climate_df = pd.DataFrame({

        "Metric": [

            "Temperature",
            "Humidity",
            "Rainfall"
        ],

        "Value": [

            temperature,
            humidity,
            rainfall
        ]
    })

    # =====================================================
    # BAR CHART
    # =====================================================
    st.subheader(
        "Agricultural Climate Analysis"
    )

    bar_fig = px.bar(

        climate_df,

        x="Metric",

        y="Value",

        text="Value"
    )

    bar_fig.update_layout(
        height=450
    )

    st.plotly_chart(
        bar_fig,
        use_container_width=True
    )

    # =====================================================
    # CLIMATE SUMMARY
    # =====================================================
    st.subheader(
        "Climate Intelligence Summary"
    )

    st.info(
        f"""
        Maximum Forecast Temperature:
        {temperature}°C

        Expected Rainfall:
        {rainfall} mm

        Average Humidity:
        {humidity}%

        Heat Risk Level:
        {heat_risk}

        Rainfall Risk Level:
        {rainfall_risk}

        Humidity Risk Level:
        {humidity_risk}

        Crop Health Status:
        {health_status}
        """
    )

    # =====================================================
    # ADVANCED RECOMMENDATIONS
    # =====================================================
    st.subheader(
        "Smart Agricultural Recommendations"
    )

    recommendations = []

    # =====================================================
    # HEAT RECOMMENDATIONS
    # =====================================================
    if heat_risk == "High":

        recommendations.append(
            """
            Extreme heat conditions detected.
            Increase irrigation frequency.
            """
        )

        recommendations.append(
            """
            Avoid fertilizer spraying
            during daytime.
            """
        )

    # =====================================================
    # FLOOD RECOMMENDATIONS
    # =====================================================
    if flood_risk in ["High", "Severe"]:

        recommendations.append(
            """
            Heavy rainfall expected.
            Ensure proper drainage systems.
            """
        )

    # =====================================================
    # HUMIDITY RECOMMENDATIONS
    # =====================================================
    if humidity_risk == "High":

        recommendations.append(
            """
            High fungal disease risk detected.
            Monitor crop infection carefully.
            """
        )

    # =====================================================
    # IRRIGATION RECOMMENDATIONS
    # =====================================================
    if irrigation_need in [
        "Very High",
        "High"
    ]:

        recommendations.append(
            """
            Additional irrigation
            may be required.
            """
        )

    # =====================================================
    # GOOD CONDITIONS
    # =====================================================
    if crop_health_score >= 80:

        recommendations.append(
            """
            Agricultural conditions are
            highly favorable for cultivation.
            """
        )

    # =====================================================
    # FALLBACK
    # =====================================================
    if not recommendations:

        recommendations.append(
            """
            Agricultural conditions
            currently appear stable.
            """
        )

    # =====================================================
    # DISPLAY RECOMMENDATIONS
    # =====================================================
    for rec in recommendations:

        st.success(rec)

    # =====================================================
    # FINAL STATUS
    # =====================================================
    st.divider()

    if crop_health_score >= 80:

        st.success(
            "Excellent agricultural conditions detected."
        )

    elif crop_health_score >= 60:

        st.info(
            "Agricultural conditions are stable."
        )

    elif crop_health_score >= 40:

        st.warning(
            "Moderate agricultural risk detected."
        )

    else:

        st.error(
            "Critical agricultural conditions detected."
        )