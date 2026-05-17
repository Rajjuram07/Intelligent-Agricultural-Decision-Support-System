# =========================================================
# DASHBOARD
# =========================================================

import streamlit as st

import pandas as pd

import plotly.express as px

from rag_workspace.query_history import (
    load_query_history
)


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    layout="wide"
)


# =========================================================
# LOAD DATASET
# =========================================================
@st.cache_data
def load_dashboard_data():

    from rag_workspace.config import (
        DATASET_PATH
    )

    df = pd.read_csv(
        DATASET_PATH
    )

    return df


# =========================================================
# KPI CARD
# =========================================================
def metric_card(

    title,

    value,

    color
):

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(
                135deg,
                #111827,
                #1F2937
            );
            padding:22px;
            border-radius:18px;
            border-top:5px solid {color};
            box-shadow:0px 0px 18px rgba(0,0,0,0.35);
            margin-bottom:8px;
        ">

        <p style="
            color:#9CA3AF;
            font-size:15px;
            margin-bottom:5px;
        ">
            {title}
        </p>

        <h1 style="
            color:white;
            margin-top:0;
            font-size:32px;
        ">
            {value}
        </h1>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# GLASS CONTAINER
# =========================================================
def glass_container_start():

    st.markdown(
        """
        <div style="
            background: rgba(17,24,39,0.75);
            border:1px solid rgba(255,255,255,0.08);
            border-radius:18px;
            padding:18px;
            margin-bottom:20px;
            backdrop-filter: blur(8px);
        ">
        """,
        unsafe_allow_html=True
    )


def glass_container_end():

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# SHOW DASHBOARD
# =========================================================
def show_dashboard():

    df = load_dashboard_data()

    history = load_query_history()

    # =====================================================
    # HEADER
    # =====================================================
    st.markdown(
        """
        <h1 style='margin-bottom:0px;'>
        🌾 AI Agricultural Intelligence Dashboard
        </h1>

        <p style='color:#9CA3AF; margin-top:5px;'>
        Real-time agricultural analytics,
        climate intelligence,
        and AI-powered insights.
        </p>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # QUICK AI SUMMARY STRIP
    # =====================================================
    total_queries = len(history)

    highest_rainfall = round(
        df["annual_rainfall"].max(),
        2
    )

    top_state = (
        df.groupby("state")
        ["production"]
        .sum()
        .idxmax()
    )

    top_crop = (
        df.groupby("crop")
        ["production"]
        .sum()
        .idxmax()
    )

    st.info(
        f"""
        📈 Top Crop: {top_crop}
        | 📍 Highest Production State: {top_state}
        | ☔ Maximum Rainfall: {highest_rainfall} mm
        | 🤖 AI Queries Processed: {total_queries}
        """
    )

    # =====================================================
    # KPI METRICS
    # =====================================================
    total_records = len(df)

    total_states = df["state"].nunique()

    total_crops = df["crop"].nunique()

    avg_rainfall = round(
        df["annual_rainfall"].mean(),
        2
    )

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:

        metric_card(
            "Crop Records",
            f"{total_records:,}",
            "#10B981"
        )

    with k2:

        metric_card(
            "States",
            total_states,
            "#3B82F6"
        )

    with k3:

        metric_card(
            "Crop Types",
            total_crops,
            "#F59E0B"
        )

    with k4:

        metric_card(
            "Avg Rainfall",
            f"{avg_rainfall} mm",
            "#06B6D4"
        )

    with k5:

        metric_card(
            "AI Queries",
            total_queries,
            "#8B5CF6"
        )

    # =====================================================
    # FILTER CONTAINER
    # =====================================================
    glass_container_start()

    st.markdown(
        "## Agricultural Intelligence Filters"
    )

    f1, f2, f3 = st.columns(3)

    with f1:

        selected_state = st.selectbox(

            "Select State",

            ["All"] + sorted(
                df["state"].dropna().unique().tolist()
            )
        )

    with f2:

        selected_crop = st.selectbox(

            "Select Crop",

            ["All"] + sorted(
                df["crop"].dropna().unique().tolist()
            )
        )

    with f3:

        rainfall_range = st.slider(

            "Rainfall Range",

            float(df["annual_rainfall"].min()),

            float(df["annual_rainfall"].max()),

            (
                float(df["annual_rainfall"].min()),
                float(df["annual_rainfall"].max())
            )
        )

    glass_container_end()

    # =====================================================
    # FILTER DATAFRAME
    # =====================================================
    filtered_df = df.copy()

    if selected_state != "All":

        filtered_df = filtered_df[
            filtered_df["state"] == selected_state
        ]

    if selected_crop != "All":

        filtered_df = filtered_df[
            filtered_df["crop"] == selected_crop
        ]

    filtered_df = filtered_df[
        (
            filtered_df["annual_rainfall"] >= rainfall_range[0]
        )
        &
        (
            filtered_df["annual_rainfall"] <= rainfall_range[1]
        )
    ]

    # =====================================================
    # TABS
    # =====================================================
    tab1, tab2, tab3 = st.tabs([

        "📊 Overview",

        "☔ Climate",

        "🤖 AI Insights"
    ])

    # =====================================================
    # OVERVIEW TAB
    # =====================================================
    with tab1:

        c1, c2 = st.columns(2)

        # =================================================
        # TOP CROPS
        # =================================================
        with c1:

            glass_container_start()

            st.markdown(
                "### Top Crop Production"
            )

            top_crop_df = (
                filtered_df.groupby("crop")
                ["production"]
                .sum()
                .sort_values(
                    ascending=False
                )
                .head(10)
                .reset_index()
            )

            fig1 = px.bar(

                top_crop_df,

                x="crop",

                y="production",

                height=380
            )

            fig1.update_layout(

                template="plotly_dark",

                paper_bgcolor="#111827",

                plot_bgcolor="#111827",

                margin=dict(
                    l=10,
                    r=10,
                    t=30,
                    b=10
                )
            )

            st.plotly_chart(
                fig1,
                use_container_width=True
            )

            glass_container_end()

        # =================================================
        # STATE ANALYTICS
        # =================================================
        with c2:

            glass_container_start()

            st.markdown(
                "### State Production Analysis"
            )

            state_df = (
                filtered_df.groupby("state")
                ["production"]
                .sum()
                .sort_values(
                    ascending=False
                )
                .head(15)
                .reset_index()
            )

            fig2 = px.line(

                state_df,

                x="state",

                y="production",

                markers=True,

                height=380
            )

            fig2.update_layout(

                template="plotly_dark",

                paper_bgcolor="#111827",

                plot_bgcolor="#111827",

                margin=dict(
                    l=10,
                    r=10,
                    t=30,
                    b=10
                )
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

            glass_container_end()

    # =====================================================
    # CLIMATE TAB
    # =====================================================
    with tab2:

        glass_container_start()

        st.markdown(
            "### Rainfall Distribution"
        )

        fig3 = px.histogram(

            filtered_df,

            x="annual_rainfall",

            nbins=40,

            height=450
        )

        fig3.update_layout(

            template="plotly_dark",

            paper_bgcolor="#111827",

            plot_bgcolor="#111827",

            margin=dict(
                l=10,
                r=10,
                t=30,
                b=10
            )
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

        glass_container_end()

    # =====================================================
    # AI INSIGHTS TAB
    # =====================================================
    with tab3:

        glass_container_start()

        st.markdown(
            "### AI Agricultural Insights"
        )

        if not filtered_df.empty:

            highest_crop = (
                filtered_df.groupby("crop")
                ["production"]
                .sum()
                .idxmax()
            )

            highest_state = (
                filtered_df.groupby("state")
                ["production"]
                .sum()
                .idxmax()
            )

            highest_rainfall = round(
                filtered_df["annual_rainfall"].max(),
                2
            )

            avg_yield = round(
                filtered_df["yield"].mean(),
                2
            )

        else:

            highest_crop = "Unavailable"

            highest_state = "Unavailable"

            highest_rainfall = 0

            avg_yield = 0

        st.success(
            f"""
            🌾 Highest production crop:
            {highest_crop}

            📍 Top agricultural state:
            {highest_state}

            ☔ Maximum rainfall observed:
            {highest_rainfall} mm

            🌱 Average yield:
            {avg_yield}

            🤖 Total AI agricultural queries:
            {total_queries}
            """
        )

        st.markdown("---")

        st.markdown(
            "### Agricultural Alerts"
        )

        if highest_rainfall > 1400:

            st.warning(
                "⚠ High rainfall conditions detected in selected regions."
            )

        if avg_yield < 1.0:

            st.error(
                "⚠ Low agricultural yield detected. Crop efficiency risk may exist."
            )

        if avg_yield >= 1.0:

            st.success(
                "✅ Agricultural productivity is stable in selected regions."
            )

        glass_container_end()