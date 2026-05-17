# =========================================================
# VECTOR STORE ENGINE
# =========================================================

import os

import faiss

import numpy as np

from rag_workspace.config import (
    FAISS_INDEX_PATH
)


# =========================================================
# CREATE FAISS INDEX
# =========================================================
def create_faiss_index(
    embeddings
):

    embeddings = np.array(
        embeddings
    ).astype(
        "float32"
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(
        embeddings
    )

    return index


# =========================================================
# SAVE FAISS INDEX
# =========================================================
def save_faiss_index(
    index
):

    faiss.write_index(
        index,
        FAISS_INDEX_PATH
    )

    print(
        "FAISS index saved successfully."
    )


# =========================================================
# LOAD FAISS INDEX
# =========================================================
def load_faiss_index():

    if not os.path.exists(
        FAISS_INDEX_PATH
    ):

        return None

    index = faiss.read_index(
        FAISS_INDEX_PATH
    )

    return index


# =========================================================
# SEARCH SIMILAR DOCUMENTS
# =========================================================
def search_documents(

    index,

    query_embedding,

    top_k=5
):

    query_embedding = np.array(

        [query_embedding]

    ).astype(
        "float32"
    )

    distances, indices = index.search(

        query_embedding,

        top_k
    )

    return distances[0], indices[0]