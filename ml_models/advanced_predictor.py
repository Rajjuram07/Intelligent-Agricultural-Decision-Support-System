import joblib

import pandas as pd


# =========================================================
# LOAD ADVANCED MODEL
# =========================================================
model = joblib.load(
    "ml_models/advanced_crop_yield_model.pkl"
)


# =========================================================
# PREDICT YIELD
# =========================================================
def predict_crop_yield(
    year,
    state,
    district,
    crop,
    crop_type,
    season,
    area,
    production
):

    # CREATE INPUT DATAFRAME
    input_data = pd.DataFrame(
        {
            "year": [year],
            "state_name": [state],
            "district_name": [district],
            "crop_name": [crop],
            "crop_type": [crop_type],
            "season": [season],
            "area": [area],
            "production": [production]
        }
    )

    # MODEL PREDICTION
    prediction = model.predict(
        input_data
    )[0]

    return round(
        float(prediction),
        2
    )