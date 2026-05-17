# =========================================================
# EMBEDDING ENGINE
# =========================================================

import os

import pickle

import numpy as np

from sentence_transformers import (
    SentenceTransformer
)

from rag_workspace.config import (

    EMBEDDING_MODEL,

    DOCUMENTS_PATH,

    EMBEDDINGS_PATH
)


# =========================================================
# LOAD EMBEDDING MODEL
# =========================================================
model = SentenceTransformer(
    EMBEDDING_MODEL
)


# =========================================================
# GENERATE EMBEDDINGS
# =========================================================
def generate_embeddings(
    documents
):

    if not documents:

        return []

    texts = [

        doc["text"]

        for doc in documents
    ]

    embeddings = model.encode(

        texts,

        show_progress_bar=True
    )

    return embeddings


# =========================================================
# SAVE EMBEDDINGS
# =========================================================
def save_embeddings(

    documents,

    embeddings
):

    try:

        # =================================================
        # SAVE DOCUMENTS
        # =================================================
        with open(

            DOCUMENTS_PATH,

            "wb"

        ) as f:

            pickle.dump(
                documents,
                f
            )

        # =================================================
        # SAVE EMBEDDINGS
        # =================================================
        np.save(

            EMBEDDINGS_PATH,

            embeddings
        )

        print(
            "Embeddings saved successfully."
        )

    except Exception as e:

        print(
            f"""
            Error saving embeddings:

            {str(e)}
            """
        )


# =========================================================
# LOAD EMBEDDINGS
# =========================================================
def load_embeddings():

    try:

        # =================================================
        # LOAD DOCUMENTS
        # =================================================
        with open(

            DOCUMENTS_PATH,

            "rb"

        ) as f:

            documents = pickle.load(
                f
            )

        # =================================================
        # LOAD EMBEDDINGS
        # =================================================
        embeddings = np.load(
            EMBEDDINGS_PATH
        )

        return documents, embeddings

    except Exception:

        return [], []


# =========================================================
# CHECK CACHE
# =========================================================
def embeddings_exist():

    return (

        os.path.exists(
            DOCUMENTS_PATH
        )

        and

        os.path.exists(
            EMBEDDINGS_PATH
        )
    )