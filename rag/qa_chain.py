import google.generativeai as genai

from utils.config import (
    GEMINI_API_KEY
)

from rag.intelligent_engine import (
    intelligent_agriculture_analysis
)

from utils.language_utils import (
    detect_language
)

from utils.query_intelligence import (
    detect_query_type
)

from utils.weather_query_parser import (
    extract_weather_location
)

model = genai.GenerativeModel(
    "gemini-3-flash-preview"
)

# =========================================================
# GREETING RESPONSE
# =========================================================
def generate_greeting_response():

    return """
# 👋 Welcome to KrishiMitra AI

I am your intelligent agricultural assistant.

You can ask me about:

✅ Crop recommendations

✅ Weather intelligence

✅ Yield prediction

✅ Irrigation planning

✅ Climate risks

✅ Farming guidance

✅ Agricultural analytics

---

### Example Questions

- Will rice cultivation perform well in Assam?
- Which crop is suitable for Bihar?
- Weather conditions in Delhi
- Best irrigation practices for wheat
"""

# =========================================================
# GENERAL AI RESPONSE
# =========================================================
def generate_general_response(
    question,
    language
):

    prompt = f"""
    You are a helpful AI assistant.

    Answer the following question naturally,
    professionally,
    and accurately.

    ====================================================

    QUESTION:
    {question}

    ====================================================

    LANGUAGE:
    {language}

    Respond in the SAME language
    as the user query.

    ====================================================

    IMPORTANT RULES

    - Keep answer concise
    - Do not mention agriculture
    - Do not generate farming advice
    - Be accurate and trustworthy
    """

    response = model.generate_content(
        prompt
    )

    return response.text

# =========================================================
# WEATHER RESPONSE
# =========================================================
def generate_weather_response(
    question,
    language
):
    
    # =====================================================
    # EXTRACT WEATHER LOCATION
    # =====================================================
    location = extract_weather_location(
        question
    )

    prompt = f"""
    You are an intelligent weather assistant.

    Answer the user's weather-related question
    clearly and professionally.

    ====================================================

    USER QUESTION:
    {question}

    ====================================================

    DETECTED LOCATION:
    {location}

    ====================================================

    RESPONSE REQUIREMENTS

    - Explain weather conditions clearly
    - Focus weather analysis on detected location
    - Mention possible climate impact
    - Mention temperature/rainfall impact
    - Keep response concise
    - Use natural conversational language

    ====================================================

    LANGUAGE:
    {language}

    Respond in the SAME language
    as the user query.

    ====================================================

    IMPORTANT RULES

    - Do not force agriculture context
    - Avoid fake weather statistics
    - Keep response realistic
    """

    response = model.generate_content(
        prompt
    )

    return response.text

# =========================================================
# CONFIGURE GEMINI
# =========================================================
genai.configure(
    api_key=GEMINI_API_KEY
)


# =========================================================
# LOAD GEMINI MODEL
# =========================================================
model = genai.GenerativeModel(
    "gemini-3-flash-preview"
)


# =========================================================
# GENERATE AI RESPONSE
# =========================================================
def generate_response(

    question,

    response_mode="Detailed Analysis"
):
    # =====================================================
    # DETECT USER LANGUAGE
    # =====================================================
    language = detect_language(
        question
    )

    # =====================================================
    # CLASSIFY QUERY
    # =====================================================
    query_type = detect_query_type(
        question
    )
    
    # =====================================================
    # GREETING QUERIES
    # =====================================================
    if query_type == "greeting":

        return (
            generate_greeting_response(),
            {}
        )

    # =====================================================
    # GENERAL KNOWLEDGE QUERIES
    # =====================================================
    if query_type == "general":

        response = generate_general_response(

            question,

            language
        )

        return response, {}
    
    # =====================================================
    # WEATHER QUERIES
    # =====================================================
    if query_type == "weather":

        response = generate_weather_response(

            question,

            language
        )

        return response, {}

    # =====================================================
    # RUN AGRICULTURAL ANALYSIS ENGINE
    # =====================================================
    analysis = intelligent_agriculture_analysis(
        question
    )

    # =====================================================
    # EXTRACT ANALYSIS RESULTS
    # =====================================================
    context = analysis["context"]

    prediction = analysis["prediction"]

    state = analysis["state"]

    district = analysis["district"]

    crop = analysis["crop"]

    crop_type = analysis["crop_type"]

    season = analysis["season"]

    year = analysis["year"]

    current_weather = analysis["current_weather"]

    forecast_weather = analysis["forecast_weather"]

    weather_summary = analysis["weather_summary"]

    insights = analysis["insights"]

    # =====================================================
    # HANDLE EMPTY VALUES
    # =====================================================
    if not state:

        state = "Not Detected"

    if not district:

        district = "Not Detected"

    if not crop:

        crop = "General Agriculture"

    if not prediction:

        prediction = "Prediction unavailable"

    if not weather_summary:

        weather_summary = (
            "Weather information unavailable"
        )

    # =====================================================
    # RESPONSE STYLE
    # =====================================================
    if response_mode == "Quick Advice":
    
        response_instruction = """
    
        RESPONSE STYLE:
        - Keep response under 150 words
        - Focus only on actionable advice
        - Use very simple farmer-friendly language
        - Avoid long explanations
        """
    
    elif response_mode == "Expert Mode":
    
        response_instruction = """
    
        RESPONSE STYLE:
        - Include detailed agricultural analysis
        - Mention climate impact
        - Mention productivity trends
        - Include technical insights
        - Include advanced farming recommendations
        """
    
    else:
    
        response_instruction = """
    
        RESPONSE STYLE:
        - Provide balanced detailed explanation
        - Keep response professional and readable
        - Include practical farmer guidance
        """

    # =====================================================
    # PROMPT
    # =====================================================
    prompt = f"""
    You are KrishiMitra AI,
    an advanced agricultural intelligence system
    designed to help farmers, researchers,
    and agricultural analysts.

    Your goal is to provide:
    - practical agricultural guidance,
    - weather-aware recommendations,
    - yield analysis,
    - cultivation insights,
    - risk assessment,
    - farmer-friendly explanations.

    ====================================================

    USER QUESTION:
    {question}

    ====================================================

    AGRICULTURAL ANALYSIS

    State:
    {state}

    District:
    {district}

    Crop:
    {crop}

    Crop Type:
    {crop_type}

    Season:
    {season}

    Year:
    {year}

    Predicted Yield:
    {prediction}

    ====================================================

    WEATHER AND CLIMATE ANALYSIS

    {weather_summary}

    ====================================================

    KEY AGRICULTURAL INSIGHTS

    {insights}

    ====================================================

    HISTORICAL AGRICULTURAL CONTEXT

    {context}

    ====================================================

    RESPONSE FORMAT

    ## Current Agricultural Situation
    Explain current crop and agricultural conditions.

    ## Yield Analysis
    Explain expected productivity and cultivation outlook.

    ## Weather Impact
    Explain how weather conditions may affect farming.

    ## Possible Risks
    Mention possible climate, disease, irrigation,
    pest, or production risks.

    ## Recommendations
    Give practical and actionable recommendations.

    ## Final Advisory
    Provide a short final conclusion.

    ====================================================

    LANGUAGE INSTRUCTION

    Detected Language:
    {language}

    Respond in the SAME language as the user question.

    If the question is in:
    - Hindi → respond in Hindi
    - Telugu → respond in Telugu
    - Tamil → respond in Tamil
    - English → respond in English

    Use farmer-friendly natural language.

    ====================================================

    IMPORTANT RULES

    - Use simple farmer-friendly language.
    - Avoid technical machine learning terminology.
    - Keep responses realistic and practical.
    - Make recommendations actionable.
    - Do not generate fake statistics.
    - Use the provided agricultural context carefully.
    - Keep the response professional and trustworthy.
    """

    # =====================================================
    # GENERATE RESPONSE
    # =====================================================
    try:

        response = model.generate_content(
            prompt
        )

        return response.text, analysis

    except Exception as e:

        return f"""
        Error generating AI response:

        {str(e)}

        Please try again.
        """