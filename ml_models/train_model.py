import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestRegressor

from sklearn.preprocessing import LabelEncoder

from sklearn.metrics import mean_absolute_error

import joblib


# LOAD DATASET
df = pd.read_csv(
    "data/raw/agriculture_data.csv"
)


# DROP NULL VALUES
df = df.dropna()


# SELECT FEATURES
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


# MODEL
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)


# TRAIN
model.fit(
    X_train,
    y_train
)


# PREDICT
predictions = model.predict(X_test)


# EVALUATE
mae = mean_absolute_error(
    y_test,
    predictions
)

print(f"Model MAE: {mae}")


# SAVE MODEL
joblib.dump(
    model,
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

print("Model training completed!")