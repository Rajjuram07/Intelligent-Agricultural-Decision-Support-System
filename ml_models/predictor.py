import joblib

import pandas as pd


# LOAD MODEL
model = joblib.load(
    "ml_models/crop_yield_model.pkl"
)

state_encoder = joblib.load(
    "ml_models/state_encoder.pkl"
)

crop_encoder = joblib.load(
    "ml_models/crop_encoder.pkl"
)


def predict_crop_yield(
    state,
    crop,
    rainfall
):

    # NORMALIZE INPUTS
    state = state.strip()

    crop = crop.strip()

    # VALIDATION
    if state not in state_encoder.classes_:

        raise ValueError(
            f"State '{state}' not found in dataset."
        )

    if crop not in crop_encoder.classes_:

        raise ValueError(
            f"Crop '{crop}' not found in dataset."
        )

    # ENCODE
    state_encoded = state_encoder.transform(
        [state]
    )[0]

    crop_encoded = crop_encoder.transform(
        [crop]
    )[0]

    # INPUT DATAFRAME
    input_data = pd.DataFrame(
        {
            "state": [state_encoded],
            "crop": [crop_encoded],
            "annual_rainfall": [rainfall]
        }
    )

    # PREDICTION
    prediction = model.predict(
        input_data
    )[0]

    return round(
        prediction,
        2
    )