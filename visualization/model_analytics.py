import streamlit as st

import pandas as pd

import plotly.express as px

import joblib


def show_model_analytics():

    st.header(
        "Machine Learning Analytics"
    )

    # LOAD MODEL RESULTS
    df = pd.read_csv(
        "ml_models/model_comparison.csv"
    )

    st.subheader(
        "Model Comparison"
    )

    st.dataframe(df)

    st.divider()

    # R2 SCORE
    st.subheader(
        "R² Score Comparison"
    )

    fig_r2 = px.bar(
        df,
        x="Model",
        y="R2 Score",
        text="R2 Score"
    )

    st.plotly_chart(
        fig_r2,
        use_container_width=True
    )

    st.divider()

    # MAE
    st.subheader(
        "MAE Comparison"
    )

    fig_mae = px.bar(
        df,
        x="Model",
        y="MAE",
        text="MAE"
    )

    st.plotly_chart(
        fig_mae,
        use_container_width=True
    )

    st.divider()

    # RMSE
    st.subheader(
        "RMSE Comparison"
    )

    fig_rmse = px.bar(
        df,
        x="Model",
        y="RMSE",
        text="RMSE"
    )

    st.plotly_chart(
        fig_rmse,
        use_container_width=True
    )

    st.divider()

    # FEATURE IMPORTANCE
    st.subheader(
        "Feature Importance"
    )

    model = joblib.load(
        "ml_models/crop_yield_model.pkl"
    )

    features = [
        "state",
        "crop",
        "annual_rainfall"
    ]

    importance_df = pd.DataFrame(
        {
            "Feature": features,
            "Importance": model.feature_importances_
        }
    )

    fig_importance = px.bar(
        importance_df,
        x="Feature",
        y="Importance",
        text="Importance"
    )

    st.plotly_chart(
        fig_importance,
        use_container_width=True
    )

    st.success(
        "Analytics generated successfully."
    )