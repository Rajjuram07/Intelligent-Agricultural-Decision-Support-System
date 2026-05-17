import pandas as pd


# =========================================================
# LOAD DATASET
# =========================================================
df = pd.read_csv(
    "data/raw/agriculture_data_2023.csv"
)

print("Original Shape:")
print(df.shape)


# =========================================================
# STANDARDIZE COLUMN NAMES
# =========================================================
df.columns = [
    col.strip().lower().replace(" ", "_")
    for col in df.columns
]

print("\nColumns:")
print(df.columns)


# =========================================================
# KEEP IMPORTANT COLUMNS
# =========================================================
required_columns = [
    "year",
    "state_name",
    "district_name",
    "crop_name",
    "crop_code",
    "crop_type",
    "season",
    "area",
    "production",
    "yield"
]

df = df[required_columns]


# =========================================================
# DROP NULL VALUES
# =========================================================
df = df.dropna()


# =========================================================
# REMOVE DUPLICATES
# =========================================================
df = df.drop_duplicates()


# =========================================================
# CLEAN TEXT COLUMNS
# =========================================================
text_columns = [
    "state_name",
    "district_name",
    "crop_name",
    "crop_type",
    "season"
]

for col in text_columns:

    df[col] = (
        df[col]
        .astype(str)
        .str.strip()
        .str.title()
    )


# =========================================================
# CONVERT NUMERIC COLUMNS
# =========================================================
numeric_columns = [
    "crop_code",
    "area",
    "production",
    "yield"
]

for col in numeric_columns:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )


# =========================================================
# REMOVE INVALID VALUES
# =========================================================
df = df[
    (df["yield"] > 0)
    &
    (df["production"] > 0)
    &
    (df["area"] > 0)
]


# =========================================================
# YEAR CLEANING
# =========================================================
df["year"] = (
    df["year"]
    .astype(str)
    .str.extract(r'(\d{4})')
)

df = df.dropna(subset=["year"])

df["year"] = df["year"].astype(int)


# =========================================================
# FEATURE ENGINEERING
# =========================================================
df["production_per_area"] = (
    df["production"] / df["area"]
)


# =========================================================
# SAVE CLEAN DATASET
# =========================================================
output_path = (
    "data/processed/"
    "clean_agriculture_data.csv"
)

df.to_csv(
    output_path,
    index=False
)

print("\nCleaned Shape:")
print(df.shape)

print("\nDataset cleaned successfully!")

print(f"\nSaved to:\n{output_path}")