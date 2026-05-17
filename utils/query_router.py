# =========================================================
# SMART QUERY ROUTER
# =========================================================

import re


# =========================================================
# AGRICULTURE KEYWORDS
# =========================================================
AGRICULTURE_KEYWORDS = [

    "crop",
    "farming",
    "agriculture",
    "yield",
    "farmer",
    "cultivation",
    "irrigation",
    "soil",
    "fertilizer",
    "harvest",
    "rainfall",
    "weather",
    "rice",
    "wheat",
    "maize",
    "cotton",
    "sugarcane",
    "bihar",
    "punjab",
    "assam",
    "season",
    "kharif",
    "rabi",
    "pesticide",
    "humidity",
    "temperature",
    "climate",
    "crop health",
    "plant disease",
    "agronomy",
    "livestock",
    "water management",
    "seed",
    "sowing"
]


# =========================================================
# WEATHER KEYWORDS
# =========================================================
WEATHER_KEYWORDS = [

    "weather",
    "temperature",
    "humidity",
    "rain",
    "forecast",
    "heat",
    "wind",
    "storm",
    "climate"
]


# =========================================================
# GREETING KEYWORDS
# =========================================================
GREETING_KEYWORDS = [

    "hello",
    "hi",
    "hey",
    "good morning",
    "good evening",
    "how are you"
]


# =========================================================
# QUERY CLASSIFIER
# =========================================================
def classify_query(query):

    query = query.lower()

    # =====================================================
    # GREETING DETECTION
    # =====================================================
    for word in GREETING_KEYWORDS:

        if word in query:

            return "greeting"

    # =====================================================
    # WEATHER DETECTION
    # =====================================================
    for word in WEATHER_KEYWORDS:

        if word in query:

            return "weather"

    # =====================================================
    # AGRICULTURE DETECTION
    # =====================================================
    for word in AGRICULTURE_KEYWORDS:

        if word in query:

            return "agriculture"

    # =====================================================
    # GENERAL KNOWLEDGE
    # =====================================================
    return "general"