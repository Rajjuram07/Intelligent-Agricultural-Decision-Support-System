# =========================================================
# QUERY INTELLIGENCE ENGINE
# =========================================================

AGRICULTURE_KEYWORDS = [

    "crop",
    "farming",
    "agriculture",
    "soil",
    "irrigation",
    "yield",
    "fertilizer",
    "cultivation",
    "harvest",
    "rainfall",
    "weather",
    "climate",
    "paddy",
    "wheat",
    "rice",
    "maize",
    "farmer",
    "disease",
    "pest",
    "kharif",
    "rabi",
    "seed"
]


WEATHER_KEYWORDS = [

    "weather",
    "temperature",
    "humidity",
    "forecast",
    "climate",
    "rain",
    "heat",
    "wind"
]


GENERAL_KEYWORDS = [

    "prime minister",
    "president",
    "capital",
    "history",
    "science",
    "movie",
    "sports",
    "actor",
    "politics"
]


# =========================================================
# DETECT QUERY TYPE
# =========================================================
def detect_query_type(
    query
):

    query = query.lower()

    agriculture_score = 0
    weather_score = 0
    general_score = 0

    # =====================================================
    # AGRICULTURE SCORE
    # =====================================================
    for keyword in AGRICULTURE_KEYWORDS:

        if keyword in query:

            agriculture_score += 1

    # =====================================================
    # WEATHER SCORE
    # =====================================================
    for keyword in WEATHER_KEYWORDS:

        if keyword in query:

            weather_score += 1

    # =====================================================
    # GENERAL SCORE
    # =====================================================
    for keyword in GENERAL_KEYWORDS:

        if keyword in query:

            general_score += 1

    # =====================================================
    # GENERAL QUERY
    # =====================================================
    if general_score > max(
        agriculture_score,
        weather_score
    ):

        return "general"

    # =====================================================
    # WEATHER QUERY
    # =====================================================
    if weather_score > agriculture_score:

        return "weather"

    # =====================================================
    # AGRICULTURE QUERY
    # =====================================================
    return "agriculture"