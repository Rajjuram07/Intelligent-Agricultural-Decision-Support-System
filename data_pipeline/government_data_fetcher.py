import requests

import pandas as pd

from utils.config import (
    DATA_GOV_API_KEY
)


# =========================================================
# GOVERNMENT API CONFIG
# =========================================================
RESOURCE_ID = "YOUR_RESOURCE_ID"

BASE_URL = (
    "https://api.data.gov.in/resource/"
)


# =========================================================
# FETCH GOVERNMENT DATA
# =========================================================
def fetch_government_data():

    url = (
        f"{BASE_URL}{RESOURCE_ID}"
        f"?api-key={DATA_GOV_API_KEY}"
        f"&format=json"
        f"&limit=1000"
    )

    print("\nFetching government data...")

    response = requests.get(url)

    data = response.json()

    records = data.get(
        "records",
        []
    )

    if not records:

        print(
            "No records received."
        )

        return

    # =====================================================
    # CONVERT TO DATAFRAME
    # =====================================================
    df = pd.DataFrame(records)

    print("\nData Retrieved:")
    print(df.shape)

    # =====================================================
    # SAVE RAW DATA
    # =====================================================
    output_path = (
        "data/raw/latest_government_data.csv"
    )

    df.to_csv(
        output_path,
        index=False
    )

    print(
        f"\nGovernment data saved to:\n"
        f"{output_path}"
    )


# =========================================================
# RUN
# =========================================================
if __name__ == "__main__":

    fetch_government_data()