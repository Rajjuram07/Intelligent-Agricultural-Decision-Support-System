import streamlit as st

from streamlit_option_menu import option_menu

from rag.qa_chain import (
    generate_response
)

from visualization.dashboard import (
    show_dashboard
)

from visualization.agriculture_insights import (
    show_agriculture_insights
)

from visualization.model_analytics import (
    show_model_analytics
)

from database.history import (
    save_message,
    load_chat_history,
    clear_chat_history
)

from database.agriculture_logs import (
    save_agriculture_log
)

from visualization.farmer_analytics import (
    show_farmer_analytics
)

from utils.pdf_generator import (
    generate_agriculture_report
)

from utils.weather_query_parser import (
    extract_weather_location
)

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="KrishiMitra AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

from rag_workspace.rag_engine import (

    initialize_rag_system,

    generate_rag_response
)

from rag_workspace.query_history import (

    load_query_history,

    save_query_history
)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.title("KrishiMitra AI")

    selected = option_menu(
        menu_title=None,
        options=[
            "Dashboard",
            "AI Assistant",
            "RAG Intelligence",
            "Analytics",
            "Predictions",
            "Weather Intelligence",
            "Settings"
        ],
        icons=[
            "speedometer2",
            "robot",
            "database",
            "bar-chart",
            "graph-up",
            "cloud-sun",
            "gear"
        ],
        default_index=0
    )

# =========================================================
# MAIN HEADER
# =========================================================
st.title("KrishiMitra AI")

st.subheader(
    "Intelligent Agricultural Decision Support System"
)

st.divider()


# =========================================================
# DASHBOARD
# =========================================================
if selected == "Dashboard":

    show_dashboard()


# =========================================================
# AI ASSISTANT
# =========================================================
elif selected == "AI Assistant":

    st.header(
        "AI Agricultural Intelligence Assistant"
    )

    # =====================================================
    # RESPONSE MODE
    # =====================================================
    response_mode = st.selectbox(

        "Select Advisory Mode",

        [
            "Quick Advice",
            "Detailed Analysis",
            "Expert Mode"
        ]
    )

    col1, col2 = st.columns([8, 1])

    with col2:

        if st.button("Clear Chat"):

            clear_chat_history()

            st.session_state.messages = []

            if "latest_analysis" in st.session_state:

                del st.session_state[
                    "latest_analysis"
                ]

            st.rerun()

    # =====================================================
    # LOAD CHAT HISTORY
    # =====================================================
    if "messages" not in st.session_state:

        chats = load_chat_history()

        st.session_state.messages = []

        for chat in chats:

            st.session_state.messages.append(
                {
                    "role": chat.role,
                    "content": chat.message
                }
            )

    # =====================================================
    # WELCOME MESSAGE
    # =====================================================
    if not st.session_state.messages:

        st.info(
            """
            Ask agricultural questions naturally.

            Examples:

            - Will wheat cultivation perform well in Bihar?
            - Which crop is suitable for high rainfall?
            - How does rainfall affect rice production?
            - Analyze agricultural trends in Assam.
            - Will high temperature affect wheat farming?
            """
        )

    # =====================================================
    # DISPLAY CHAT HISTORY
    # =====================================================
    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

    # =====================================================
    # USER INPUT
    # =====================================================
    prompt = st.chat_input(
        "Ask your agricultural question"
    )

    if prompt:

        # =================================================
        # STORE USER MESSAGE
        # =================================================
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        save_message(
            "user",
            prompt
        )

        # =================================================
        # DISPLAY USER MESSAGE
        # =================================================
        with st.chat_message("user"):

            st.markdown(prompt)

        # =================================================
        # AI RESPONSE
        # =================================================
        with st.chat_message("assistant"):

            with st.spinner(
                "Analyzing agricultural intelligence..."
            ):

                try:

                    response, analysis = (
                        generate_response(
                            question=prompt,
                            response_mode=response_mode
                        )
                    )

                    # =====================================
                    # SAVE ANALYSIS
                    # =====================================
                    st.session_state[
                        "latest_analysis"
                    ] = analysis

                    # =====================================
                    # DISPLAY RESPONSE
                    # =====================================
                    st.markdown(response)

                    # =====================================
                    # PDF REPORT
                    # =====================================
                    try:

                        pdf_path = (
                            generate_agriculture_report(

                                question=prompt,

                                response=response,

                                prediction=analysis.get(
                                    "prediction"
                                ),

                                forecast_weather=analysis.get(
                                    "forecast_weather"
                                )
                            )
                        )

                        with open(
                            pdf_path,
                            "rb"
                        ) as pdf_file:

                            st.download_button(

                                label=(
                                    "Download Agricultural Report"
                                ),

                                data=pdf_file,

                                file_name=(
                                    "KrishiMitra_Report.pdf"
                                ),

                                mime="application/pdf"
                            )

                    except Exception:

                        pass

                    # =====================================
                    # SAVE LOGS
                    # =====================================
                    try:

                        save_agriculture_log(

                            question=prompt,

                            response=response,

                            crop=analysis.get(
                                "crop"
                            ),

                            state=analysis.get(
                                "state"
                            ),

                            prediction=(
                                analysis.get(
                                    "prediction"
                                )
                                if analysis.get(
                                    "prediction"
                                )
                                else 0
                            ),

                            heat_risk=(
                                analysis.get(
                                    "forecast_weather",
                                    {}
                                ).get(
                                    "heat_risk",
                                    "Unknown"
                                )
                            ),

                            rainfall_risk=(
                                analysis.get(
                                    "forecast_weather",
                                    {}
                                ).get(
                                    "rainfall_risk",
                                    "Unknown"
                                )
                            )
                        )

                    except Exception:

                        pass

                except Exception as e:

                    response = (
                        f"System Error: {str(e)}"
                    )

                    st.error(response)

        # =================================================
        # SAVE CHAT RESPONSE
        # =================================================
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        save_message(
            "assistant",
            response
        )

    # =====================================================
    # PERSISTENT DASHBOARD
    # =====================================================
    if "latest_analysis" in st.session_state:

        analysis = st.session_state[
            "latest_analysis"
        ]

        forecast_weather = analysis.get(
            "forecast_weather"
        )

        if forecast_weather:

            st.divider()

            show_agriculture_insights(

                analysis.get(
                    "prediction"
                ),

                forecast_weather
            )

# =========================================================
# RAG INTELLIGENCE WORKSPACE
# =========================================================
elif selected == "RAG Intelligence":

    st.header(
        "RAG Intelligence Workspace"
    )

    st.markdown(
        """
        Retrieval-Augmented Generation system
        for agricultural and climate intelligence.

        Ask questions related to:

        - Crop production
        - Rainfall analysis
        - Agricultural yield
        - Climate trends
        - District-level farming insights
        - State-wise crop statistics
        - Historical agricultural intelligence
        """
    )

    st.divider()

    # =====================================================
    # QUERY INPUT
    # =====================================================
    query = st.text_input(
        "Ask agricultural or climate question"
    )

    # =====================================================
    # SETTINGS
    # =====================================================
    col1, col2 = st.columns(2)

    with col1:

        top_k = st.slider(

            "Top-K Documents",

            1,

            10,

            5
        )

    with col2:

        temperature = st.slider(

            "AI Temperature",

            0.0,

            1.0,

            0.5
        )

    st.divider()

    # =====================================================
    # RAG INITIALIZATION
    # =====================================================
    st.sidebar.subheader(
        "RAG System Control"
    )

    if st.sidebar.button(
        "Initialize RAG System"
    ):

        with st.spinner(
            "Initializing RAG Workspace..."
        ):

            try:

                st.session_state.rag_system = (
                    initialize_rag_system()
                )

                st.sidebar.success(
                    """
                    RAG System Initialized Successfully
                    """
                )

            except Exception as e:

                st.sidebar.error(
                    f"""
                    Initialization Failed:

                    {str(e)}
                    """
                )

    # =====================================================
    # SEARCH HISTORY
    # =====================================================
    st.sidebar.divider()

    st.sidebar.subheader(
        "Search History"
    )

    history = load_query_history()

    if len(history) == 0:

        st.sidebar.info(
            "No searches yet."
        )

    else:

        for item in reversed(history[-10:]):

            with st.sidebar.expander(

                item["query"]

            ):

                st.markdown(

                    item["answer"]
                )

                st.caption(

                    item["timestamp"]
                )

    st.divider()
    
    # =====================================================
    # ASK BUTTON
    # =====================================================
    if st.button(
        "Ask RAG System"
    ):

        # =================================================
        # CHECK INITIALIZATION
        # =================================================
        if "rag_system" not in st.session_state:

            st.warning(
                """
                Please initialize the RAG system first
                using the sidebar.
                """
            )

            st.stop()

        # =================================================
        # EMPTY QUERY CHECK
        # =================================================
        if query.strip() == "":

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Retrieving agricultural intelligence..."
            ):

                # =============================================
                # GENERATE RAG RESPONSE
                # =============================================
                result = generate_rag_response(

                    query,

                    st.session_state.rag_system,

                    top_k,

                    temperature
                )

                # =============================================
                # SAVE QUERY HISTORY
                # =============================================
                save_query_history(

                    query,

                    result["answer"]
                )

                # =============================================
                # ANSWER
                # =============================================
                st.subheader(
                    "AI Answer"
                )

                st.markdown(
                    result["answer"]
                )

                st.divider()

                # =============================================
                # STATISTICS
                # =============================================
                st.subheader(
                    "Statistical Summary"
                )

                stats = result["statistics"]

                st.markdown(
                    f"""
                    ### Production Statistics

                    - Average:
                    {stats["production"]["average"]}

                    - Maximum:
                    {stats["production"]["maximum"]}

                    - Minimum:
                    {stats["production"]["minimum"]}

                    ---

                    ### Yield Statistics

                    - Average:
                    {stats["yield"]["average"]}

                    - Maximum:
                    {stats["yield"]["maximum"]}

                    - Minimum:
                    {stats["yield"]["minimum"]}

                    ---

                    ### Rainfall Statistics

                    - Average:
                    {stats["rainfall"]["average"]}

                    - Maximum:
                    {stats["rainfall"]["maximum"]}

                    - Minimum:
                    {stats["rainfall"]["minimum"]}
                    """
                )

                st.divider()

                # =============================================
                # SOURCE DOCUMENTS
                # =============================================
                st.subheader(
                    "Source Documents"
                )

                for i, doc in enumerate(

                    result["retrieved_docs"],

                    start=1
                ):

                    metadata = doc["metadata"]

                    with st.expander(

                        f"""
                        Source {i}
                        | Similarity:
                        {doc["similarity"]}
                        """
                    ):

                        st.markdown(
                            doc["text"]
                        )

                        st.markdown(
                            f"""
                            **State:** {metadata["state"]}

                            **District:** {metadata["district"]}

                            **Year:** {metadata["year"]}

                            **Crop:** {metadata["crop"]}
                            """
                        )

# =========================================================
# ANALYTICS
# =========================================================
elif selected == "Analytics":

    st.header(
        "Agricultural Analytics"
    )

    show_model_analytics()

    st.divider()

    show_farmer_analytics()

    st.info(
        """
        Analytics dashboard for:

        - Model benchmarking
        - Feature importance
        - Agricultural trend analysis
        - Yield intelligence
        - Performance evaluation
        """
    )


# =========================================================
# PREDICTIONS
# =========================================================
elif selected == "Predictions":

    # =====================================================
    # IMPORTS
    # =====================================================
    import pandas as pd

    import plotly.express as px

    from rag_workspace.config import (
        DATASET_PATH
    )

    # =====================================================
    # LOAD DATASET
    # =====================================================
    @st.cache_data
    def load_prediction_data():

        df = pd.read_csv(
            DATASET_PATH
        )

        return df

    df = load_prediction_data()

    # =====================================================
    # PAGE HEADER
    # =====================================================
    st.markdown(
        """
        <div style="
            margin-bottom:25px;
        ">

        <h1 style="
            margin-bottom:5px;
            color:white;
            font-size:42px;
            font-weight:700;
        ">
            AI Agricultural Predictions
        </h1>

        <p style="
            color:#9CA3AF;
            font-size:17px;
        ">
            Retrieval-driven agricultural forecasting
            and predictive intelligence using
            historical crop and climate records.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # =====================================================
    # FILTER SECTION
    # =====================================================
    st.markdown(
        """
        <div style="
            background:#111827;
            padding:22px;
            border-radius:18px;
            border:1px solid rgba(255,255,255,0.06);
            margin-bottom:25px;
        ">
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "### Prediction Controls"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        selected_state = st.selectbox(

            "State",

            sorted(
                df["state"]
                .dropna()
                .unique()
                .tolist()
            )
        )

    filtered_state_df = df[
        df["state"] == selected_state
    ]

    with c2:

        selected_district = st.selectbox(

            "District",

            sorted(
                filtered_state_df["district"]
                .dropna()
                .unique()
                .tolist()
            )
        )

    filtered_district_df = filtered_state_df[
        filtered_state_df["district"]
        == selected_district
    ]

    with c3:

        selected_crop = st.selectbox(

            "Crop",

            sorted(
                filtered_district_df["crop"]
                .dropna()
                .unique()
                .tolist()
            )
        )

    crop_df = filtered_district_df[
        filtered_district_df["crop"]
        == selected_crop
    ]

    with c4:

        selected_year = st.selectbox(

            "Prediction Year",

            sorted(
                crop_df["year_cleaned"]
                .dropna()
                .unique()
                .tolist()
            )
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    # =====================================================
    # GENERATE PREDICTION
    # =====================================================
    if st.button(
        "Generate Agricultural Prediction",
        use_container_width=True
    ):

        # =================================================
        # FILTER FINAL DATA
        # =================================================
        prediction_df = crop_df[
            crop_df["year_cleaned"]
            <= selected_year
        ]

        latest_record = prediction_df.sort_values(

            by="year_cleaned",

            ascending=False

        ).iloc[0]

        # =================================================
        # METRICS
        # =================================================
        avg_production = round(

            prediction_df["production"]
            .mean(),

            2
        )

        avg_yield = round(

            prediction_df["yield"]
            .mean(),

            2
        )

        avg_rainfall = round(

            prediction_df["annual_rainfall"]
            .mean(),

            2
        )

        latest_production = round(

            latest_record["production"],

            2
        )

        # =================================================
        # KPI CARDS
        # =================================================
        k1, k2, k3, k4 = st.columns(4)

        with k1:

            st.metric(

                "Average Production",

                avg_production
            )

        with k2:

            st.metric(

                "Average Yield",

                avg_yield
            )

        with k3:

            st.metric(

                "Average Rainfall",

                f"{avg_rainfall} mm"
            )

        with k4:

            st.metric(

                "Latest Production",

                latest_production
            )

        st.divider()

        # =================================================
        # CHART SECTION
        # =================================================
        chart1, chart2 = st.columns(2)

        # ================================================
        # PRODUCTION TREND
        # ================================================
        with chart1:

            st.markdown(
                "### Production Trend"
            )

            production_trend = (

                prediction_df.groupby(
                    "year_cleaned"
                )["production"]

                .mean()

                .reset_index()
            )

            fig1 = px.line(

                production_trend,

                x="year_cleaned",

                y="production",

                markers=True
            )

            fig1.update_layout(

                template="plotly_dark",

                paper_bgcolor="#0B1120",

                plot_bgcolor="#0B1120",

                height=400,

                margin=dict(
                    l=20,
                    r=20,
                    t=30,
                    b=20
                )
            )

            st.plotly_chart(
                fig1,
                use_container_width=True
            )

        # ================================================
        # RAINFALL TREND
        # ================================================
        with chart2:

            st.markdown(
                "### Rainfall Trend"
            )

            rainfall_trend = (

                prediction_df.groupby(
                    "year_cleaned"
                )["annual_rainfall"]

                .mean()

                .reset_index()
            )

            fig2 = px.bar(

                rainfall_trend,

                x="year_cleaned",

                y="annual_rainfall"
            )

            fig2.update_layout(

                template="plotly_dark",

                paper_bgcolor="#0B1120",

                plot_bgcolor="#0B1120",

                height=400,

                margin=dict(
                    l=20,
                    r=20,
                    t=30,
                    b=20
                )
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

        st.divider()

        # =================================================
        # AI FORECAST SECTION
        # =================================================
        st.markdown(
            """
            <div style="
                background:#111827;
                padding:25px;
                border-radius:18px;
                border:1px solid rgba(255,255,255,0.06);
            ">
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            "### AI Agricultural Forecast"
        )

        production_change = (
            prediction_df["production"]
            .pct_change()
            .mean()
        )

        rainfall_change = (
            prediction_df["annual_rainfall"]
            .pct_change()
            .mean()
        )

        # ================================================
        # DYNAMIC INSIGHTS
        # ================================================
        insights = []

        if production_change > 0:

            insights.append(
                "Production trend shows gradual improvement."
            )

        else:

            insights.append(
                "Production variability detected across years."
            )

        if rainfall_change > 0:

            insights.append(
                "Rainfall conditions are showing positive movement."
            )

        else:

            insights.append(
                "Rainfall fluctuations may affect crop stability."
            )

        if avg_yield > prediction_df["yield"].median():

            insights.append(
                "Agricultural yield remains above historical median."
            )

        else:

            insights.append(
                "Yield efficiency may require monitoring."
            )

        # ================================================
        # DISPLAY INSIGHTS
        # ================================================
        for insight in insights:

            st.success(
                insight
            )

        st.markdown(
            "---"
        )

        st.markdown(
            f"""
            **Prediction Summary**

            Based on historical agricultural
            records for **{selected_crop}**
            in **{selected_district}**,
            **{selected_state}**:

            - Average production:
              {avg_production}

            - Average rainfall:
              {avg_rainfall} mm

            - Average yield:
              {avg_yield}

            The agricultural intelligence
            system identified meaningful
            historical production and
            climate patterns from retrieved
            records.
            """
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# =========================================================
# WEATHER INTELLIGENCE
# =========================================================
elif selected == "Weather Intelligence":

    st.header(
        "Weather Intelligence"
    )

    # =====================================================
    # IMPORTS
    # =====================================================
    from api.weather_api import (
        get_weather,
        generate_weather_advisory
    )

    from api.advanced_weather import (
        get_weather_forecast
    )

    # =====================================================
    # CITY INPUT
    # =====================================================
    weather_query = st.text_input(
        "Enter weather query or city",
        value=""
    )
    
    # =====================================================
    # EXTRACT CITY FROM QUERY
    # =====================================================
    parsed_city = extract_weather_location(
        weather_query
    )
    
    # =====================================================
    # FINAL CITY
    # =====================================================
    if parsed_city:
    
        city = parsed_city
    
    else:
    
        city = weather_query

    # =====================================================
    # GET WEATHER
    # =====================================================
    if st.button("Get Weather"):

        current_weather = get_weather(
            city
        )

        forecast_weather = (
            get_weather_forecast(
                city
            )
        )

        # =================================================
        # ERROR HANDLING
        # =================================================
        if "error" in current_weather:

            st.error(
                current_weather["error"]
            )

        else:

            # =============================================
            # WEATHER METRICS
            # =============================================
            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Temperature",
                    f"{current_weather['temperature']} °C"
                )

                st.metric(
                    "Humidity",
                    f"{current_weather['humidity']}%"
                )

                st.metric(
                    "Condition",
                    current_weather["weather"]
                )

            with col2:

                st.metric(
                    "Wind Speed",
                    f"{current_weather['wind_speed']} km/h"
                )

                st.metric(
                    "Heat Risk",
                    forecast_weather[
                        "heat_risk"
                    ]
                )

                st.metric(
                    "Rainfall Risk",
                    forecast_weather[
                        "rainfall_risk"
                    ]
                )

            with col3:

                st.metric(
                    "Max Forecast Temp",
                    f"""
                    {
                        forecast_weather.get(
                            'max_forecast_temperature',
                            0
                        )
                    } °C
                    """
                )

                st.metric(
                    "Expected Rainfall",
                    f"""
                    {
                        forecast_weather.get(
                            'total_forecast_rainfall',
                            0
                        )
                    } mm
                    """
                )

                st.metric(
                    "Humidity Risk",
                    forecast_weather.get(
                        "humidity_risk",
                        "Unknown"
                    )
                )

            st.success(
                f"""
                Weather intelligence generated
                for {city.title()}
                """
            )

            # =============================================
            # AI WEATHER ADVISORY
            # =============================================
            st.divider()

            st.subheader(
                "AI Agricultural Advisory"
            )

            with st.spinner(
                "Generating climate advisory..."
            ):

                advisory = (
                    generate_weather_advisory(
                        current_weather
                    )
                )

                st.markdown(
                    advisory
                )

            # =============================================
            # SMART ALERTS
            # =============================================
            st.divider()

            st.subheader(
                "Smart Agricultural Alerts"
            )

            if forecast_weather.get(
                "heat_risk"
            ) == "High":

                st.error(
                    """
                    Extreme heat alert detected.
                    Crop stress risk is high.
                    """
                )

            if forecast_weather.get(
                "rainfall_risk"
            ) == "High":

                st.warning(
                    """
                    Heavy rainfall expected.
                    Flooding risk possible.
                    """
                )

            if forecast_weather.get(
                "total_forecast_rainfall",
                0
            ) < 2:

                st.info(
                    """
                    Low rainfall forecast.
                    Additional irrigation
                    may be required.
                    """
                )

            # =============================================
            # AGRICULTURAL DASHBOARD
            # =============================================
            st.divider()

            show_agriculture_insights(

                "Weather Intelligence",

                forecast_weather
            )

    # =====================================================
    # WEATHER INFO
    # =====================================================
    st.info(
        """
        Real-time climate intelligence powered by:

        - WeatherAPI Forecast Intelligence
        - Gemini AI
        - Agricultural advisory system
        """
    )


# =========================================================
# SETTINGS
# =========================================================
elif selected == "Settings":

    st.header(
        "System Settings"
    )

    st.info(
        """
        Application configuration,
        AI model settings,
        system preferences,
        multilingual support,
        and future enterprise controls
        will appear here.
        """
    )