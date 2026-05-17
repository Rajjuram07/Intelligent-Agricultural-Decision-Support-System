import re


# =========================================================
# EXTRACT LOCATION FROM WEATHER QUERY
# =========================================================
def extract_weather_location(
    query
):

    query = query.lower()

    patterns = [

        r"weather in ([a-zA-Z ]+)",

        r"temperature in ([a-zA-Z ]+)",

        r"rainfall in ([a-zA-Z ]+)",

        r"climate of ([a-zA-Z ]+)",

        r"forecast for ([a-zA-Z ]+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            query
        )

        if match:

            location = match.group(1)

            return location.title().strip()

    return None