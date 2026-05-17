import streamlit as st

import pandas as pd

import plotly.express as px

from sqlalchemy import create_engine


# =========================================================
# DATABASE
# =========================================================
DATABASE_URL = "sqlite:///krishimitra_logs.db"

engine = create_engine(
    DATABASE_URL
)


# =========================================================
# SHOW FARMER ANALYTICS
# =========================================================
def show_farmer_analytics():

    st.subheader(
        "Agricultural Intelligence Analytics"
    )

    try:

        # =================================================
        # LOAD DATABASE
        # =================================================
        query = """
        SELECT * FROM agriculture_logs
        """

        df = pd.read_sql(
            query,
            engine
        )

        # =================================================
        # EMPTY CHECK
        # =================================================
        if df.empty:

            st.warning(
                "No agricultural logs found."
            )

            return

        # =================================================
        # METRICS
        # =================================================
        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Queries",
                len(df)
            )

        with col2:

            st.metric(
                "Unique Crops",
                df["crop"].nunique()
            )

        with col3:

            st.metric(
                "States Covered",
                df["state"].nunique()
            )

        st.divider()

        # =================================================
        # MOST SEARCHED CROPS
        # =================================================
        crop_counts = (
            df["crop"]
            .value_counts()
            .reset_index()
        )

        crop_counts.columns = [
            "Crop",
            "Count"
        ]

        fig1 = px.bar(
            crop_counts,
            x="Crop",
            y="Count",
            title="Most Analyzed Crops"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

        # =================================================
        # HEAT RISK ANALYSIS
        # =================================================
        heat_counts = (
            df["heat_risk"]
            .value_counts()
            .reset_index()
        )

        heat_counts.columns = [
            "Heat Risk",
            "Count"
        ]

        fig2 = px.pie(
            heat_counts,
            names="Heat Risk",
            values="Count",
            title="Heat Risk Distribution"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        # =================================================
        # RAINFALL RISK ANALYSIS
        # =================================================
        rain_counts = (
            df["rainfall_risk"]
            .value_counts()
            .reset_index()
        )

        rain_counts.columns = [
            "Rainfall Risk",
            "Count"
        ]

        fig3 = px.pie(
            rain_counts,
            names="Rainfall Risk",
            values="Count",
            title="Rainfall Risk Distribution"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

        # =================================================
        # PREDICTION DISTRIBUTION
        # =================================================
        fig4 = px.histogram(
            df,
            x="prediction",
            nbins=20,
            title="Prediction Distribution"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

    except Exception as e:

        st.error(
            f"Analytics Error: {str(e)}"
        )