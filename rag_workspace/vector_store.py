# =========================================================
# VECTOR STORE ENGINE
# =========================================================

import os

import faiss

import numpy as np

from pinecone import Pinecone

from rag_workspace.config import (
    FAISS_INDEX_PATH
)

from utils.config import (

    PINECONE_API_KEY,

    PINECONE_INDEX_NAME
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

# =========================================================
# INITIALIZE PINECONE
# =========================================================
def initialize_pinecone():

    try:

        pc = Pinecone(
            api_key=PINECONE_API_KEY
        )

        index = pc.Index(
            PINECONE_INDEX_NAME
        )

        return index

    except Exception as e:

        print(
            f"Pinecone initialization error: {e}"
        )

        return None

# =========================================================
# PINECONE SEARCH
# =========================================================
def pinecone_search(

    pinecone_index,

    query_embedding,

    top_k=5
):

    try:

        results = pinecone_index.query(

            vector=query_embedding.tolist(),

            top_k=top_k,

            include_metadata=True
        )

        return results.matches

    except Exception as e:

        print(
            f"Pinecone search error: {e}"
        )

        return []