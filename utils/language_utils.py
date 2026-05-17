from langdetect import detect


# =========================================================
# DETECT LANGUAGE
# =========================================================
def detect_language(text):

    try:

        language = detect(text)

        return language

    except Exception:

        return "en"