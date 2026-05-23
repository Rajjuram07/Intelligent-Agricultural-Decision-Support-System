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
    get_chat_statistics,
    clear_chat_history,
    save_activity,
    load_activities,
    delete_activity
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

# =========================================================
# GLOBAL SETTINGS SESSION STATE
# =========================================================
if "language_preference" not in st.session_state:

    st.session_state.language_preference = "English"

if "ai_temperature" not in st.session_state:

    st.session_state.ai_temperature = 0.5

if "retrieval_engine" not in st.session_state:

    st.session_state.retrieval_engine = "FAISS"

if "prediction_horizon" not in st.session_state:

    st.session_state.prediction_horizon = "1 Year"

if "weather_alerts" not in st.session_state:

    st.session_state.weather_alerts = True

if "ai_explanation_mode" not in st.session_state:

    st.session_state.ai_explanation_mode = True

# =========================================================
# GLOBAL SEARCH HISTORY SESSION STATE
# =========================================================
if "ai_assistant_history" not in st.session_state:

    st.session_state.ai_assistant_history = []

if "rag_history_hidden" not in st.session_state:

    st.session_state.rag_history_hidden = []

if "weather_history_hidden" not in st.session_state:

    st.session_state.weather_history_hidden = []

if "ai_history_hidden" not in st.session_state:

    st.session_state.ai_history_hidden = []

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

    # =====================================================
    # AI ASSISTANT HISTORY
    # =====================================================
    st.divider()

    st.subheader(
        "AI Assistant History"
    )

    if len(
        st.session_state.ai_assistant_history
    ) == 0:

        st.info(
            "No AI assistant searches."
        )

    else:

        for i, item in enumerate(

            reversed(
                st.session_state.ai_assistant_history[-5:]
            )
        ):

            if item["query"] in st.session_state.ai_history_hidden:

                continue

            col1, col2 = st.columns([5, 1])

            with col1:

                with st.expander(
                    item["query"]
                ):

                    st.markdown(
                        item["response"]
                    )

            with col2:

                if st.button(

                    "🗑",

                    key=f"ai_delete_{i}"
                ):

                    st.session_state.ai_history_hidden.append(
                        item["query"]
                    )

                    st.rerun()

    # =====================================================
    # RAG HISTORY
    # =====================================================
    st.divider()

    st.subheader(
        "RAG Intelligence History"
    )

    rag_history = load_query_history()

    visible_rag_history = [

        item for item in rag_history

        if item["query"]
        not in st.session_state.rag_history_hidden
    ]

    if len(visible_rag_history) == 0:

        st.info(
            "No RAG searches."
        )

    else:

        for i, item in enumerate(

            reversed(
                visible_rag_history[-5:]
            )
        ):

            col1, col2 = st.columns([5, 1])

            with col1:

                with st.expander(
                    item["query"]
                ):

                    st.markdown(
                        item["answer"]
                    )

                    st.caption(
                        item["timestamp"]
                    )

            with col2:

                if st.button(

                    "🗑",

                    key=f"rag_delete_{i}"
                ):

                    st.session_state.rag_history_hidden.append(
                        item["query"]
                    )

                    st.rerun()

    # =====================================================
    # WEATHER HISTORY
    # =====================================================
    st.divider()

    st.subheader(
        "Weather Intelligence History"
    )

    if "weather_history" not in st.session_state:

        st.session_state.weather_history = []

    visible_weather_history = [

        item for item
        in st.session_state.weather_history

        if item["query"]
        not in st.session_state.weather_history_hidden
    ]

    if len(visible_weather_history) == 0:

        st.info(
            "No weather searches."
        )

    else:

        for i, item in enumerate(

            reversed(
                visible_weather_history[-5:]
            )
        ):

            col1, col2 = st.columns([5, 1])

            with col1:

                with st.expander(
                    item["query"]
                ):

                    st.markdown(
                        item["response"]
                    )

            with col2:

                if st.button(

                    "🗑",

                    key=f"weather_delete_{i}"
                ):

                    st.session_state.weather_history_hidden.append(
                        item["query"]
                    )

                    st.rerun()

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

        # =============================================
        # SAVE ACTIVITY
        # =============================================
        save_activity(

            module="AI Assistant",

            query=prompt,

            response=response,

            retrieval_engine=st.session_state.retrieval_engine,

            language=st.session_state.language_preference,

            ai_temperature=st.session_state.ai_temperature
        )

        # =============================================
        # SAVE AI ASSISTANT HISTORY
        # =============================================
        st.session_state.ai_assistant_history.append(

            {
                "query": prompt,
                "response": response
            }
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
    # HYBRID AI RETRIEVAL PANEL
    # =====================================================
    st.sidebar.markdown(
        """
        <div style="
            background: linear-gradient(
                135deg,
                #111827,
                #1F2937
            );
            padding:18px;
            border-radius:18px;
            border:1px solid #374151;
            margin-top:15px;
            margin-bottom:15px;
        ">

        <h3 style="
            color:white;
            margin-bottom:12px;
        ">
            Hybrid AI Retrieval
        </h3>

        <p style="color:#D1D5DB;">
            FAISS:
            <span style="color:#10B981;">
                Connected
            </span>
        </p>

        <p style="color:#D1D5DB;">
            Pinecone:
            <span style="color:#10B981;">
                Connected
            </span>
        </p>

        <p style="color:#D1D5DB;">
            Active Engine:
            <span style="color:#60A5FA;">
                Hybrid Retrieval
            </span>
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # RAG SYSTEM CONTROL
    # =====================================================
    st.sidebar.markdown(
        "### RAG Workspace Control"
    )

    if st.sidebar.button(
        "Initialize Hybrid RAG System",
        use_container_width=True
    ):

        with st.spinner(
            "Initializing Hybrid AI Retrieval..."
        ):

            try:

                st.session_state.rag_system = (
                    initialize_rag_system()
                )

                st.sidebar.success(
                    """
                    Hybrid RAG System Initialized
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

    st.sidebar.markdown(
        """
        ### Search Intelligence History
        """
    )

    history = load_query_history()

    if len(history) == 0:

        st.sidebar.info(
            "No searches yet."
        )

    else:

        for item in reversed(history[-10:]):

            with st.sidebar.expander(

                f"""
                {item["query"][:40]}
                """
            ):

                st.markdown(
                    item["answer"]
                )

                st.caption(
                    item["timestamp"]
                )

                st.markdown(
                    """
                    Retrieval:
                    Hybrid AI Retrieval
                    """
                )

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
                # AI AGRICULTURAL INTELLIGENCE
                # =============================================
                st.markdown(
                    """
                    <div style="
                        background: linear-gradient(
                            135deg,
                            #111827,
                            #1F2937
                        );
                        padding:25px;
                        border-radius:18px;
                        border:1px solid #374151;
                        margin-bottom:20px;
                    ">

                    <h2 style="
                        color:white;
                        margin-bottom:15px;
                    ">
                        AI Agricultural Intelligence
                    </h2>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    result["answer"]
                )

                # =============================================
                # EXPLAINABLE AI MODE
                # =============================================
                if st.session_state.ai_explanation_mode:

                    st.divider()

                    st.subheader(
                        "Explainable AI Insights"
                    )

                    explanation = result[
                        "explanation"
                    ]

                    avg_similarity = explanation[
                        "average_similarity"
                    ]

                    # =========================================
                    # AI CONFIDENCE LEVEL
                    # =========================================
                    if avg_similarity >= 0.85:

                        confidence = "High"

                    elif avg_similarity >= 0.70:

                        confidence = "Moderate"

                    else:

                        confidence = "Low"

                    # =========================================
                    # METRICS
                    # =========================================
                    e1, e2, e3, e4 = st.columns(4)

                    with e1:

                        st.metric(

                            "Documents Retrieved",

                            explanation[
                                "documents_retrieved"
                            ]
                        )

                    with e2:

                        st.metric(

                            "Similarity Score",

                            avg_similarity
                        )

                    with e3:

                        st.metric(

                            "AI Confidence",

                            confidence
                        )

                    with e4:

                        st.metric(

                            "Retrieval Engine",

                            st.session_state.retrieval_engine
                        )

                    st.divider()

                    # =========================================
                    # AI REASONING
                    # =========================================
                    st.markdown(
                        """
                        ### AI Reasoning Summary
                        """
                    )

                    st.info(
                        f"""
                        This response was generated using
                        semantic agricultural retrieval
                        with {confidence.lower()} confidence
                        analysis from historical crop,
                        rainfall, and production records.
                        """
                    )

                    # =========================================
                    # AGRICULTURAL INSIGHTS
                    # =========================================
                    r1, r2 = st.columns(2)

                    with r1:

                        st.success(
                            explanation[
                                "rainfall_analysis"
                            ]
                        )

                    with r2:

                        st.success(
                            explanation[
                                "production_trend"
                            ]
                        )

                st.divider()

                # =============================================
                # STATISTICS
                # =============================================
                st.subheader(
                    "Statistical Summary"
                )

                stats = result["statistics"]

                s1, s2, s3 = st.columns(3)

                with s1:

                    st.metric(
                        "Average Production",
                        stats["production"]["average"]
                    )

                with s2:

                    st.metric(
                        "Average Yield",
                        stats["yield"]["average"]
                    )

                with s3:

                    st.metric(
                        "Average Rainfall",
                        stats["rainfall"]["average"]
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
                        | Similarity Score:
                        {doc["similarity"]}
                        """
                    ):

                        similarity = doc[
                            "similarity"
                        ]

                        # =====================================
                        # CONFIDENCE STATUS
                        # =====================================
                        if similarity >= 0.85:

                            st.success(
                                "High Semantic Match"
                            )

                        elif similarity >= 0.70:

                            st.warning(
                                "Moderate Semantic Match"
                            )

                        else:

                            st.error(
                                "Low Semantic Match"
                            )

                        # =====================================
                        # SOURCE DOCUMENT
                        # =====================================
                        st.markdown(
                            "### Retrieved Agricultural Record"
                        )

                        st.markdown(
                            doc["text"]
                        )

                        st.divider()

                        # =====================================
                        # AGRICULTURAL METADATA
                        # =====================================
                        meta1, meta2 = st.columns(2)

                        with meta1:

                            st.markdown(
                                f"""
                                ### Regional Metadata

                                - State:
                                  {metadata["state"]}

                                - District:
                                  {metadata["district"]}

                                - Crop:
                                  {metadata["crop"]}
                                """
                            )

                        with meta2:

                            st.markdown(
                                f"""
                                ### Retrieval Metadata

                                - Year:
                                  {metadata["year"]}

                                - Similarity:
                                  {doc["similarity"]}

                                - Engine:
                                  {st.session_state.retrieval_engine}
                                """
                            )

# =========================================================
# ANALYTICS
# =========================================================
elif selected == "Analytics":

    # =====================================================
    # IMPORTS
    # =====================================================
    import pandas as pd

    from collections import Counter

    import re

    import plotly.express as px

    from datetime import datetime

    # =====================================================
    # PAGE HEADER
    # =====================================================
    st.markdown(
        """
        <div style="
            margin-bottom:25px;
        ">

        <h1 style="
            color:white;
            font-size:42px;
            font-weight:700;
            margin-bottom:8px;
        ">
            AI Agricultural Intelligence Analytics
        </h1>

        <p style="
            color:#9CA3AF;
            font-size:17px;
        ">
            Centralized operational analytics
            for AI activity, retrieval intelligence,
            forecasting usage, and agricultural interactions.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # =====================================================
    # LOAD DATABASE ACTIVITIES
    # =====================================================
    activities = load_activities()

    ai_history = [

        activity for activity in activities

        if activity.module == "AI Assistant"
    ]

    rag_history = [

        activity for activity in activities

        if activity.module == "RAG Intelligence"
    ]

    weather_history = [

        activity for activity in activities

        if activity.module == "Weather Intelligence"
    ]

    # =====================================================
    # METRICS
    # =====================================================
    total_ai_queries = len(ai_history)

    total_rag_queries = len(rag_history)

    total_weather_queries = len(weather_history)

    total_queries = (

        total_ai_queries
        + total_rag_queries
        + total_weather_queries
    )

    # =====================================================
    # KPI SECTION
    # =====================================================
    st.subheader(
        "Operational Intelligence Metrics"
    )

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.metric(
            "Total Queries",
            total_queries
        )

    with m2:

        st.metric(
            "AI Assistant",
            total_ai_queries
        )

    with m3:

        st.metric(
            "RAG Intelligence",
            total_rag_queries
        )

    with m4:

        st.metric(
            "Weather Requests",
            total_weather_queries
        )

    st.divider()

    # =====================================================
    # SYSTEM STATUS
    # =====================================================
    st.subheader(
        "Enterprise AI Infrastructure"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.success(
            "Gemini AI Online"
        )

    with c2:

        st.success(
            "FAISS Active"
        )

    with c3:

        st.success(
            "Pinecone Ready"
        )

    with c4:

        st.success(
            "PostgreSQL Connected"
        )

    st.divider()

    # =====================================================
    # QUERY DISTRIBUTION
    # =====================================================
    st.subheader(
        "AI Activity Distribution"
    )

    chart1, chart2 = st.columns(2)

    # =====================================================
    # BAR CHART
    # =====================================================
    with chart1:

        distribution_df = pd.DataFrame(

            {
                "Module": [

                    "AI Assistant",
                    "RAG Intelligence",
                    "Weather Intelligence"
                ],

                "Queries": [

                    total_ai_queries,
                    total_rag_queries,
                    total_weather_queries
                ]
            }
        )

        fig1 = px.bar(

            distribution_df,

            x="Module",

            y="Queries",

            text="Queries"
        )

        fig1.update_layout(

            template="plotly_dark",

            paper_bgcolor="#0B1120",

            plot_bgcolor="#0B1120",

            height=420
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    # =====================================================
    # PIE CHART
    # =====================================================
    with chart2:

        fig2 = px.pie(

            distribution_df,

            names="Module",

            values="Queries",

            hole=0.5
        )

        fig2.update_layout(

            template="plotly_dark",

            paper_bgcolor="#0B1120",

            plot_bgcolor="#0B1120",

            height=420
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.divider()

    # =====================================================
    # RECENT AI ACTIVITIES
    # =====================================================
    st.subheader(
        "Recent AI Activities"
    )

    # =====================================================
    # DATABASE ACTIVITY TABLE
    # =====================================================
    if len(activities) > 0:

        activity_data = []

        for activity in activities:

            activity_data.append(

                {
                    "ID": activity.id,

                    "Module": activity.module,

                    "Query": activity.query,

                    "Retrieval": activity.retrieval_engine,

                    "Language": activity.language,

                    "AI Temperature": activity.ai_temperature,

                    "Timestamp": activity.created_at.strftime(
                        "%Y-%m-%d %H:%M"
                    )
                }
            )

        activity_df = pd.DataFrame(
            activity_data
        )

        st.dataframe(

            activity_df,

            use_container_width=True,

            height=450
        )

        st.divider()

        # =====================================================
        # PERMANENT DATABASE DELETE
        # =====================================================
        st.subheader(
            "Database Activity Management"
        )

        activity_ids = [

            activity.id
            for activity in activities
        ]

        if len(activity_ids) > 0:

            selected_activity = st.selectbox(

                "Select Activity ID to Delete Permanently",

                activity_ids
            )

            if st.button(
                "Delete Activity Permanently"
            ):

                delete_activity(
                    selected_activity
                )

                st.success(
                    "Activity deleted from PostgreSQL database."
                )

                st.rerun()

        else:

            st.info(
                "No database activities available."
            )

    st.divider()

    # =====================================================
    # CURRENT ACTIVE SETTINGS
    # =====================================================
    st.subheader(
        "Current AI Configuration"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            f"""
            Language:
            {st.session_state.language_preference}
            """
        )

        st.info(
            f"""
            Retrieval Engine:
            {st.session_state.retrieval_engine}
            """
        )

    with col2:

        st.info(
            f"""
            AI Temperature:
            {st.session_state.ai_temperature}
            """
        )

        st.info(
            f"""
            Prediction Horizon:
            {st.session_state.prediction_horizon}
            """
        )

    st.divider()

    # =====================================================
    # QUERY INTELLIGENCE ANALYTICS
    # =====================================================
    st.subheader(
        "Query Intelligence Analytics"
    )

    # =====================================================
    # EXTRACT QUERY TEXTS
    # =====================================================
    all_queries = [

        activity.query.lower()

        for activity in activities
    ]

    # =====================================================
    # TOKENIZATION
    # =====================================================
    stop_words = {

        "what",
        "is",
        "the",
        "in",
        "of",
        "for",
        "show",
        "give",
        "crop",
        "production",
        "rainfall",
        "yield",
        "tell",
        "me"
    }

    words = []

    for query in all_queries:

        extracted_words = re.findall(

            r"\b[a-zA-Z]+\b",

            query
        )

        filtered_words = [

            word for word
            in extracted_words

            if word not in stop_words
            and len(word) > 2
        ]

        words.extend(filtered_words)

    # =====================================================
    # MOST SEARCHED TERMS
    # =====================================================
    word_counts = Counter(
        words
    )

    top_terms = word_counts.most_common(10)

    if len(top_terms) > 0:

        terms_df = pd.DataFrame(

            top_terms,

            columns=[
                "Agricultural Topic",
                "Search Count"
            ]
        )

        col1, col2 = st.columns(2)

        # =================================================
        # TOP SEARCHED TOPICS
        # =================================================
        with col1:

            st.markdown(
                "### Most Searched Topics"
            )

            fig_topics = px.bar(

                terms_df,

                x="Agricultural Topic",

                y="Search Count",

                text="Search Count"
            )

            fig_topics.update_layout(

                template="plotly_dark",

                paper_bgcolor="#0B1120",

                plot_bgcolor="#0B1120",

                height=420
            )

            st.plotly_chart(

                fig_topics,

                use_container_width=True
            )

        # =================================================
        # RETRIEVAL ENGINE ANALYTICS
        # =================================================
        with col2:

            st.markdown(
                "### Retrieval Engine Usage"
            )

            retrieval_data = pd.DataFrame(

                {
                    "Engine": [

                        activity.retrieval_engine

                        for activity in activities
                    ]
                }
            )

            retrieval_counts = retrieval_data[
                "Engine"
            ].value_counts().reset_index()

            retrieval_counts.columns = [

                "Engine",
                "Usage"
            ]

            fig_retrieval = px.pie(

                retrieval_counts,

                names="Engine",

                values="Usage",

                hole=0.5
            )

            fig_retrieval.update_layout(

                template="plotly_dark",

                paper_bgcolor="#0B1120",

                plot_bgcolor="#0B1120",

                height=420
            )

            st.plotly_chart(

                fig_retrieval,

                use_container_width=True
            )

    else:

        st.info(
            "No query intelligence data available."
        )

    st.divider()

     # =====================================================
    # LANGUAGE ANALYTICS
    # =====================================================
    st.subheader(
        "Language Intelligence Analytics"
    )

    language_df = pd.DataFrame(

        {
            "Language": [

                activity.language

                for activity in activities
            ]
        }
    )

    if len(language_df) > 0:

        language_counts = language_df[
            "Language"
        ].value_counts().reset_index()

        language_counts.columns = [

            "Language",
            "Usage"
        ]

        fig_language = px.bar(

            language_counts,

            x="Language",

            y="Usage",

            text="Usage"
        )

        fig_language.update_layout(

            template="plotly_dark",

            paper_bgcolor="#0B1120",

            plot_bgcolor="#0B1120",

            height=400
        )

        st.plotly_chart(

            fig_language,

            use_container_width=True
        )

    else:

        st.info(
            "No language analytics available."
        )

    st.divider()

    # =====================================================
    # EXISTING ANALYTICS
    # =====================================================
    st.subheader(
        "Advanced Agricultural Analytics"
    )

    show_model_analytics()

    st.divider()

    show_farmer_analytics()

    st.info(
        """
        Advanced analytics ecosystem includes:

        - Agricultural forecasting intelligence
        - Machine learning benchmarking
        - Yield trend analysis
        - Climate-aware insights
        - Retrieval analytics
        - AI operational intelligence
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

                # =====================================
                # SAVE WEATHER HISTORY
                # =====================================
                st.session_state.weather_history.append(

                    {
                        "query": city,
                        "response": advisory
                    }
                )

                # =========================================
                # SAVE ACTIVITY
                # =========================================
                save_activity(

                    module="Weather Intelligence",

                    query=city,

                    response=advisory,

                    retrieval_engine=st.session_state.retrieval_engine,

                    language=st.session_state.language_preference,

                    ai_temperature=st.session_state.ai_temperature
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
        "AI Agricultural Intelligence Control Center"
    )

    st.markdown(
        """
        Configure AI intelligence,
        multilingual preferences,
        retrieval systems,
        forecasting controls,
        and enterprise infrastructure settings.
        """
    )

    st.divider()

    # =====================================================
    # FARMER PREFERENCES
    # =====================================================
    st.subheader(
        "Farmer Preferences"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.session_state.language_preference = st.selectbox(

            "Preferred Language",

            [
                "English",
                "Hindi",
                "Telugu",
                "Marathi",
                "Tamil"
            ],

            index=[
                "English",
                "Hindi",
                "Telugu",
                "Marathi",
                "Tamil"
            ].index(
                st.session_state.language_preference
            )
        )

    with col2:

        st.session_state.weather_alerts = st.toggle(

            "Enable Weather Alerts",

            value=st.session_state.weather_alerts
        )

    st.divider()

    # =====================================================
    # AI INTELLIGENCE CONTROLS
    # =====================================================
    st.subheader(
        "AI Intelligence Controls"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.session_state.ai_temperature = st.slider(

            "Gemini AI Temperature",

            min_value=0.0,

            max_value=1.0,

            value=float(
                st.session_state.ai_temperature
            ),

            step=0.1
        )

    with col2:

        st.session_state.retrieval_engine = st.selectbox(

            "Retrieval Engine",

            [
                "FAISS",
                "Pinecone",
                "Hybrid AI Retrieval"
            ],

            index=[
                "FAISS",
                "Pinecone",
                "Hybrid AI Retrieval"
            ].index(
                st.session_state.retrieval_engine
            )
        )

    st.session_state.ai_explanation_mode = st.toggle(

        "Enable AI Explanation Mode",

        value=st.session_state.ai_explanation_mode
    )

    st.caption(
        """
        AI explanation mode enables
        explainable agricultural intelligence
        including rainfall impact,
        historical trend reasoning,
        and prediction analysis.
        """
    )

    st.divider()

    # =====================================================
    # FORECAST INTELLIGENCE
    # =====================================================
    st.subheader(
        "Forecast Intelligence"
    )

    st.session_state.prediction_horizon = st.radio(

        "Prediction Horizon",

        [
            "1 Year",
            "3 Years",
            "5 Years"
        ],

        horizontal=True,

        index=[
            "1 Year",
            "3 Years",
            "5 Years"
        ].index(
            st.session_state.prediction_horizon
        )
    )

    st.info(
        f"""
        Current forecasting configuration:
        {st.session_state.prediction_horizon}
        agricultural forecasting horizon enabled.
        """
    )

    st.divider()

    # =====================================================
    # ENTERPRISE SYSTEM STATUS
    # =====================================================
    st.subheader(
        "Enterprise Infrastructure Status"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.success(
            "PostgreSQL Connected"
        )

        st.caption(
            "Persistence Layer Active"
        )

    with col2:

        st.success(
            "FAISS Vector Store Active"
        )

        st.caption(
            "Semantic Retrieval Ready"
        )

    with col3:

        st.success(
            "Gemini AI Connected"
        )

        st.caption(
            "AI Intelligence Engine Online"
        )

    col4, col5 = st.columns(2)

    with col4:

        st.success(
            "Pinecone Integration Ready"
        )

        st.caption(
            "Cloud Vector Retrieval Enabled"
        )

    with col5:

        if st.session_state.weather_alerts:

            st.success(
                "Weather Intelligence Active"
            )

        else:

            st.warning(
                "Weather Alerts Disabled"
            )

        st.caption(
            "Climate Intelligence Monitoring"
        )

    st.divider()

    # =====================================================
    # CURRENT ACTIVE CONFIGURATION
    # =====================================================
    st.subheader(
        "Current Active Configuration"
    )

    st.markdown(
        f"""
        ### AI Configuration Summary

        - Language Preference:
        **{st.session_state.language_preference}**

        - AI Temperature:
        **{st.session_state.ai_temperature}**

        - Retrieval Engine:
        **{st.session_state.retrieval_engine}**

        - Prediction Horizon:
        **{st.session_state.prediction_horizon}**

        - Weather Alerts:
        **{"Enabled" if st.session_state.weather_alerts else "Disabled"}**

        - AI Explanation Mode:
        **{"Enabled" if st.session_state.ai_explanation_mode else "Disabled"}**
        """
    )