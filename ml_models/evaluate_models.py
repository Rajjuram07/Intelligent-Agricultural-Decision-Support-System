import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import LabelEncoder

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from sklearn.linear_model import LinearRegression

from sklearn.tree import DecisionTreeRegressor

from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor
)

from xgboost import XGBRegressor

import joblib

import numpy as np


# LOAD DATASET
df = pd.read_csv(
    "data/raw/agriculture_data.csv"
)


# REMOVE NULL VALUES
df = df.dropna()


# FEATURES
features = [
    "state",
    "crop",
    "annual_rainfall"
]

target = "yield"


# LABEL ENCODING
state_encoder = LabelEncoder()

crop_encoder = LabelEncoder()


df["state"] = state_encoder.fit_transform(
    df["state"]
)

df["crop"] = crop_encoder.fit_transform(
    df["crop"]
)


# INPUT / OUTPUT
X = df[features]

y = df[target]


# TRAIN TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# MODELS
models = {

    "Linear Regression": LinearRegression(),

    "Decision Tree": DecisionTreeRegressor(
        random_state=42
    ),

    "Random Forest": RandomForestRegressor(
        n_estimators=100,
        random_state=42
    ),

    "Gradient Boosting": GradientBoostingRegressor(
        random_state=42
    ),

    "XGBoost": XGBRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=6,
        random_state=42
    )
}


# RESULTS
results = []

best_model = None

best_r2 = -999


print("\nMODEL EVALUATION STARTED\n")


# TRAIN & EVALUATE
for name, model in models.items():

    print(f"Training {name}...")

    # TRAIN
    model.fit(
        X_train,
        y_train
    )

    # PREDICT
    predictions = model.predict(
        X_test
    )

    # METRICS
    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions
        )
    )

    r2 = r2_score(
        y_test,
        predictions
    )

    # STORE RESULTS
    results.append({
        "Model": name,
        "MAE": round(mae, 4),
        "RMSE": round(rmse, 4),
        "R2 Score": round(r2, 4)
    })

    print(f"{name} Completed")
    print(f"MAE: {mae}")
    print(f"RMSE: {rmse}")
    print(f"R2 Score: {r2}")
    print("-" * 50)

    # BEST MODEL
    if r2 > best_r2:

        best_r2 = r2

        best_model = model

        best_model_name = name


# RESULTS DATAFRAME
results_df = pd.DataFrame(
    results
)


# SORT BY R2 SCORE
results_df = results_df.sort_values(
    by="R2 Score",
    ascending=False
)


# DISPLAY RESULTS
print("\nMODEL COMPARISON\n")

print(results_df)


# SAVE RESULTS
results_df.to_csv(
    "ml_models/model_comparison.csv",
    index=False
)


# SAVE BEST MODEL
joblib.dump(
    best_model,
    "ml_models/crop_yield_model.pkl"
)

joblib.dump(
    state_encoder,
    "ml_models/state_encoder.pkl"
)

joblib.dump(
    crop_encoder,
    "ml_models/crop_encoder.pkl"
)


print("\nBEST MODEL:")
print(best_model_name)

print("\nMODEL EVALUATION COMPLETED!")