# =========================================================
# RETRIEVER ENGINE
# =========================================================

import numpy as np

import streamlit as st

from rag_workspace.embeddings import (
    model
)

from rag_workspace.vector_store import (

    search_documents,

    initialize_pinecone,

    pinecone_search
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

    retrieved_docs = []

    retrieval_engine = st.session_state.get(

        "retrieval_engine",

        "FAISS"
    )

    # =====================================================
    # FAISS RETRIEVAL
    # =====================================================
    if retrieval_engine == "FAISS":

        distances, indices = search_documents(

            index,

            query_embedding,

            top_k
        )

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

    # =====================================================
    # PINECONE RETRIEVAL
    # =====================================================
    elif retrieval_engine == "Pinecone":

        pinecone_index = initialize_pinecone()

        if pinecone_index:

            matches = pinecone_search(

                pinecone_index,

                query_embedding,

                top_k
            )

            for match in matches:

                retrieved_docs.append({

                    "text": match.metadata.get(
                        "text",
                        ""
                    ),

                    "metadata": match.metadata,

                    "similarity": round(
                        match.score,
                        3
                    )
                })

    # =====================================================
    # HYBRID RETRIEVAL
    # =====================================================
    elif retrieval_engine == "Hybrid AI Retrieval":

        # ================================================
        # FAISS RESULTS
        # ================================================
        distances, indices = search_documents(

            index,

            query_embedding,

            top_k
        )

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

        # ================================================
        # PINECONE RESULTS
        # ================================================
        pinecone_index = initialize_pinecone()

        if pinecone_index:

            matches = pinecone_search(

                pinecone_index,

                query_embedding,

                top_k
            )

            for match in matches:

                retrieved_docs.append({

                    "text": match.metadata.get(
                        "text",
                        ""
                    ),

                    "metadata": match.metadata,

                    "similarity": round(
                        match.score,
                        3
                    )
                })

        # ================================================
        # REMOVE DUPLICATES
        # ================================================
        unique_docs = []

        seen_texts = set()

        for doc in retrieved_docs:

            if doc["text"] not in seen_texts:

                unique_docs.append(doc)

                seen_texts.add(
                    doc["text"]
                )

        # ================================================
        # SORT BY SIMILARITY
        # ================================================
        retrieved_docs = sorted(

            unique_docs,

            key=lambda x: x["similarity"],

            reverse=True
        )

    return retrieved_docs[:top_k]