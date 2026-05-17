# =========================================================
# STATISTICS ENGINE
# =========================================================

import pandas as pd

import numpy as np


# =========================================================
# GENERATE SUMMARY STATISTICS
# =========================================================
def generate_statistics(
    retrieved_docs
):

    if not retrieved_docs:

        return {}

    production_values = []

    yield_values = []

    rainfall_values = []

    # =====================================================
    # EXTRACT VALUES
    # =====================================================
    for doc in retrieved_docs:

        metadata = doc["metadata"]

        try:

            production = float(
                metadata.get(
                    "production",
                    0
                )
            )

            production_values.append(
                production
            )

        except Exception:

            pass

        try:

            yield_value = float(
                metadata.get(
                    "yield",
                    0
                )
            )

            yield_values.append(
                yield_value
            )

        except Exception:

            pass

        try:

            rainfall = float(
                metadata.get(
                    "rainfall",
                    0
                )
            )

            rainfall_values.append(
                rainfall
            )

        except Exception:

            pass

    # =====================================================
    # GENERATE STATISTICS
    # =====================================================
    stats = {

        "production": {

            "average": round(
                np.mean(
                    production_values
                ),
                2
            ) if production_values else 0,

            "maximum": round(
                np.max(
                    production_values
                ),
                2
            ) if production_values else 0,

            "minimum": round(
                np.min(
                    production_values
                ),
                2
            ) if production_values else 0
        },

        "yield": {

            "average": round(
                np.mean(
                    yield_values
                ),
                2
            ) if yield_values else 0,

            "maximum": round(
                np.max(
                    yield_values
                ),
                2
            ) if yield_values else 0,

            "minimum": round(
                np.min(
                    yield_values
                ),
                2
            ) if yield_values else 0
        },

        "rainfall": {

            "average": round(
                np.mean(
                    rainfall_values
                ),
                2
            ) if rainfall_values else 0,

            "maximum": round(
                np.max(
                    rainfall_values
                ),
                2
            ) if rainfall_values else 0,

            "minimum": round(
                np.min(
                    rainfall_values
                ),
                2
            ) if rainfall_values else 0
        }
    }

    return stats