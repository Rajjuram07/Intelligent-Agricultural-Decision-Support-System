import pandas as pd

import re


# =========================================================
# LOAD CLEAN DATASET
# =========================================================
df = pd.read_csv(
    "data/processed/clean_agriculture_data.csv"
)


# =========================================================
# UNIQUE VALUES
# =========================================================
states = set(
    df["state_name"]
    .dropna()
    .astype(str)
    .str.lower()
)

districts = set(
    df["district_name"]
    .dropna()
    .astype(str)
    .str.lower()
)

crops = set(
    df["crop_name"]
    .dropna()
    .astype(str)
    .str.lower()
)

crop_types = set(
    df["crop_type"]
    .dropna()
    .astype(str)
    .str.lower()
)

seasons = set(
    df["season"]
    .dropna()
    .astype(str)
    .str.lower()
)


# =========================================================
# ENTITY EXTRACTION
# =========================================================
def extract_entities(question):

    question_lower = question.lower()

    extracted = {
        "state": None,
        "district": None,
        "crop": None,
        "crop_type": None,
        "season": None,
        "year": None
    }

    # =====================================================
    # STATE DETECTION
    # =====================================================
    for state in states:

        if state in question_lower:

            extracted["state"] = state.title()

            break

    # =====================================================
    # DISTRICT DETECTION
    # =====================================================
    for district in districts:

        if district in question_lower:

            extracted["district"] = district.title()

            break

    # =====================================================
    # CROP DETECTION
    # =====================================================
    for crop in crops:

        if crop in question_lower:

            extracted["crop"] = crop.title()

            break

    # =====================================================
    # CROP TYPE DETECTION
    # =====================================================
    for crop_type in crop_types:

        if crop_type in question_lower:

            extracted["crop_type"] = (
                crop_type.title()
            )

            break

    # =====================================================
    # SEASON DETECTION
    # =====================================================
    for season in seasons:

        if season in question_lower:

            extracted["season"] = (
                season.title()
            )

            break

    # =====================================================
    # YEAR EXTRACTION
    # =====================================================
    year_match = re.search(
        r"\b(19\d{2}|20\d{2})\b",
        question
    )

    if year_match:

        extracted["year"] = int(
            year_match.group(1)
        )

    return extracted