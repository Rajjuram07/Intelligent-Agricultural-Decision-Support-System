# =========================================================
# DATA LOADER
# =========================================================

import pandas as pd

from rag_workspace.config import (
    DATASET_PATH
)


# =========================================================
# COLUMN STANDARDIZATION
# =========================================================
def standardize_columns(df):

    column_mapping = {

        # =================================================
        # STATE
        # =================================================
        "State_Name": "state",
        "state": "state",

        # =================================================
        # DISTRICT
        # =================================================
        "District_Name": "district",
        "district": "district",

        # =================================================
        # YEAR
        # =================================================
        "Crop_Year": "year",
        "year": "year",
        "year_cleaned": "year",

        # =================================================
        # CROP
        # =================================================
        "Crop": "crop",
        "crop": "crop",

        # =================================================
        # PRODUCTION
        # =================================================
        "Production": "production",
        "production": "production",

        # =================================================
        # YIELD
        # =================================================
        "Yield": "yield",
        "yield": "yield",

        # =================================================
        # RAINFALL
        # =================================================
        "Annual_Rainfall": "rainfall",
        "annual_rainfall": "rainfall",
        "rainfall": "rainfall"
    }

    # =====================================================
    # RENAME COLUMNS
    # =====================================================
    df = df.rename(
        columns=column_mapping
    )

    return df


# =========================================================
# LOAD DATASET
# =========================================================
def load_dataset():

    df = pd.read_csv(
        DATASET_PATH
    )

    # =====================================================
    # STANDARDIZE COLUMNS
    # =====================================================
    df = standardize_columns(df)

    return df


# =========================================================
# PREPARE DOCUMENTS
# =========================================================
def prepare_dataset():

    df = load_dataset()

    documents = []

    # =====================================================
    # CREATE DOCUMENTS
    # =====================================================
    for _, row in df.iterrows():

        state = str(
            row.get(
                "state",
                "Unknown"
            )
        )

        district = str(
            row.get(
                "district",
                "Unknown"
            )
        )

        year = str(
            row.get(
                "year",
                "Unknown"
            )
        )

        crop = str(
            row.get(
                "crop",
                "Unknown"
            )
        )

        production = str(
            row.get(
                "production",
                "Unknown"
            )
        )

        yield_value = str(
            row.get(
                "yield",
                "Unknown"
            )
        )

        rainfall = str(
            row.get(
                "rainfall",
                "Unknown"
            )
        )

        # =================================================
        # DOCUMENT TEXT
        # =================================================
        text = f"""
        In {year}, the district {district}
        in {state} produced {production}
        tonnes of {crop} with yield
        {yield_value} tonnes per hectare
        and recorded {rainfall}
        mm annual rainfall.
        """

        # =================================================
        # DOCUMENT OBJECT
        # =================================================
        documents.append({

            "text": text,

            "metadata": {

                "state": state,

                "district": district,

                "year": year,

                "crop": crop,

                "production": production,

                "yield": yield_value,

                "rainfall": rainfall
            }
        })

    return df, documents