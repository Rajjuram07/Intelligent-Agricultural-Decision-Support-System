import pandas as pd

import joblib

from sklearn.model_selection import (
    train_test_split
)

from sklearn.compose import (
    ColumnTransformer
)

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import (
    OneHotEncoder
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from xgboost import XGBRegressor


# =========================================================
# LOAD CLEAN DATASET
# =========================================================
df = pd.read_csv(
    "data/processed/clean_agriculture_data.csv"
)

print("Dataset Loaded Successfully")
print(df.shape)


# =========================================================
# FEATURES & TARGET
# =========================================================
features = [
    "year",
    "state_name",
    "district_name",
    "crop_name",
    "crop_type",
    "season",
    "area",
    "production"
]

target = "yield"


X = df[features]

y = df[target]


# =========================================================
# CATEGORICAL & NUMERIC FEATURES
# =========================================================
categorical_features = [
    "state_name",
    "district_name",
    "crop_name",
    "crop_type",
    "season"
]

numeric_features = [
    "year",
    "area",
    "production"
]


# =========================================================
# PREPROCESSING
# =========================================================
preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        )
    ],
    remainder="passthrough"
)


# =========================================================
# MODEL
# =========================================================
model = XGBRegressor(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)


# =========================================================
# PIPELINE
# =========================================================
pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "model",
            model
        )
    ]
)


# =========================================================
# TRAIN TEST SPLIT
# =========================================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# =========================================================
# TRAIN MODEL
# =========================================================
print("\nTraining Advanced XGBoost Model...")

pipeline.fit(
    X_train,
    y_train
)

print("Training Completed!")


# =========================================================
# PREDICTIONS
# =========================================================
predictions = pipeline.predict(
    X_test
)


# =========================================================
# EVALUATION
# =========================================================
mae = mean_absolute_error(
    y_test,
    predictions
)

mse = mean_squared_error(
    y_test,
    predictions
)

rmse = mse ** 0.5

r2 = r2_score(
    y_test,
    predictions
)


print("\nMODEL PERFORMANCE")

print(f"MAE: {mae}")

print(f"RMSE: {rmse}")

print(f"R2 Score: {r2}")


# =========================================================
# SAVE MODEL
# =========================================================
joblib.dump(
    pipeline,
    "ml_models/advanced_crop_yield_model.pkl"
)

print(
    "\nAdvanced model saved successfully!"
)