# =========================================================
# QUERY HISTORY SYSTEM
# =========================================================

import json

from pathlib import Path

from datetime import datetime


# =========================================================
# HISTORY FILE
# =========================================================
HISTORY_FILE = Path(
    "rag_workspace/query_history/history.json"
)

# =========================================================
# CREATE DIRECTORY
# =========================================================
HISTORY_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

# =========================================================
# CREATE FILE IF NOT EXISTS
# =========================================================
if not HISTORY_FILE.exists():

    with open(
        HISTORY_FILE,
        "w"
    ) as f:

        json.dump(
            [],
            f
        )


# =========================================================
# LOAD QUERY HISTORY
# =========================================================
def load_query_history():

    try:

        with open(
            HISTORY_FILE,
            "r"
        ) as f:

            return json.load(f)

    except Exception:

        return []


# =========================================================
# SAVE QUERY HISTORY
# =========================================================
def save_query_history(

    query,

    answer
):

    history = load_query_history()

    history.append({

        "query": query,

        "answer": answer,

        "timestamp": str(
            datetime.now()
        )
    })

    with open(
        HISTORY_FILE,
        "w"
    ) as f:

        json.dump(
            history,
            f,
            indent=4
        )