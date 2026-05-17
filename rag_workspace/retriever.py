# =========================================================
# RETRIEVER ENGINE
# =========================================================

import numpy as np

from rag_workspace.embeddings import (
    model
)

from rag_workspace.vector_store import (
    search_documents
)


# =========================================================
# RETRIEVE DOCUMENTS
# =========================================================
def retrieve_documents(

    query,

    index,

    documents,

    top_k=5
):

    # =====================================================
    # QUERY EMBEDDING
    # =====================================================
    query_embedding = model.encode(
        [query]
    )[0]

    # =====================================================
    # SEARCH DOCUMENTS
    # =====================================================
    distances, indices = search_documents(

        index,

        query_embedding,

        top_k
    )

    retrieved_docs = []

    # =====================================================
    # PROCESS RESULTS
    # =====================================================
    for distance, idx in zip(
        distances,
        indices
    ):

        if idx >= len(documents):

            continue

        doc = documents[idx]

        similarity = 1 / (
            1 + float(distance)
        )

        retrieved_docs.append({

            "text": doc["text"],

            "metadata": doc["metadata"],

            "similarity": round(
                similarity,
                3
            )
        })

    return retrieved_docs