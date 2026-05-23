# =========================================================
# RAG ENGINE
# =========================================================

import streamlit as st

import google.generativeai as genai

from rag_workspace.data_loader import (
    prepare_dataset
)

from rag_workspace.embeddings import (

    generate_embeddings,

    save_embeddings,

    load_embeddings,

    embeddings_exist
)

from rag_workspace.vector_store import (

    create_faiss_index,

    save_faiss_index,

    load_faiss_index
)

from rag_workspace.retriever import (
    retrieve_documents
)

from rag_workspace.statistics_engine import (
    generate_statistics
)

from rag_workspace.config import (

    TOP_K_RESULTS,

    DEFAULT_MODEL,

    DEFAULT_TEMPERATURE
)

from utils.config import (
    GEMINI_API_KEY
)


# =========================================================
# CONFIGURE GEMINI
# =========================================================
genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel(
    DEFAULT_MODEL
)


# =========================================================
# INITIALIZE RAG SYSTEM
# =========================================================
def initialize_rag_system():

    # =====================================================
    # LOAD DATASET
    # =====================================================
    print(
        "Loading agricultural dataset..."
    )

    df, documents = prepare_dataset()

    print(
        f"Loaded {len(documents)} documents."
    )

    # =====================================================
    # LOAD EXISTING EMBEDDINGS
    # =====================================================
    if embeddings_exist():

        print(
            "Loading cached embeddings..."
        )

        documents, embeddings = load_embeddings()

    else:

        print(
            "Generating embeddings for first time..."
        )

        embeddings = generate_embeddings(
            documents
        )

        save_embeddings(

            documents,

            embeddings
        )

        print(
            "Embeddings generated and cached."
        )

    # =====================================================
    # LOAD EXISTING FAISS INDEX
    # =====================================================
    index = load_faiss_index()

    # =====================================================
    # CREATE NEW INDEX
    # =====================================================
    if index is None:

        print(
            "Creating FAISS index..."
        )

        index = create_faiss_index(
            embeddings
        )

        save_faiss_index(
            index
        )

        print(
            "FAISS index created."
        )

    else:

        print(
            "Loading existing FAISS index..."
        )

    # =====================================================
    # RETURN RAG SYSTEM
    # =====================================================
    return {

        "dataframe": df,

        "documents": documents,

        "embeddings": embeddings,

        "index": index
    }


# =========================================================
# GENERATE RAG RESPONSE
# =========================================================
def generate_rag_response(

    query,

    rag_system,

    top_k=5,

    temperature=0.7
):

    # =====================================================
    # VALIDATION
    # =====================================================
    if rag_system is None:

        raise ValueError(
            "RAG system is not initialized."
        )

    # =====================================================
    # RETRIEVE DOCUMENTS
    # =====================================================
    retrieved_docs = retrieve_documents(

        query,

        rag_system["index"],

        rag_system["documents"],

        top_k
    )

    # =====================================================
    # GENERATE STATISTICS
    # =====================================================
    statistics = generate_statistics(
        retrieved_docs
    )

    # =====================================================
    # CONTEXT CREATION
    # =====================================================
    context = "\n\n".join([

        doc["text"]

        for doc in retrieved_docs
    ])

    # =====================================================
    # PROMPT
    # =====================================================
    prompt = f"""
    You are an agricultural and climate
    intelligence assistant.

    Use ONLY the provided agricultural
    records to answer the question.

    ====================================================

    QUESTION:
    {query}

    ====================================================

    AGRICULTURAL RECORDS:
    {context}

    ====================================================

    IMPORTANT RULES

    - Use retrieved records carefully
    - Keep answer factual
    - Do not generate fake statistics
    - Mention trends if visible
    - Mention rainfall impact if relevant
    - Keep answer professional
    - Use retrieved agricultural data only
    """

    # =====================================================
    # GEMINI RESPONSE
    # =====================================================
    response = model.generate_content(
        prompt
    )

    # =====================================================
    # EXPLAINABLE AI INSIGHTS
    # =====================================================
    explanation = {

        "retrieval_engine": st.session_state.get(
            "retrieval_engine",
            "FAISS"
        ),

        "documents_retrieved": len(
            retrieved_docs
        ),

        "average_similarity": round(

            sum(
                doc["similarity"]
                for doc in retrieved_docs
            ) / len(retrieved_docs),

            3
        ) if retrieved_docs else 0,

        "rainfall_analysis": (

            "Rainfall patterns indicate "
            "potential agricultural impact."

            if statistics.get(
                "rainfall",
                {}
            ).get(
                "average",
                0
            ) > 0

            else "No rainfall intelligence detected."
        ),

        "production_trend": (

            "Production statistics show "
            "historical agricultural variation."

            if statistics.get(
                "production",
                {}
            ).get(
                "average",
                0
            ) > 0

            else "No production trend available."
        )
    }

    # =====================================================
    # FINAL RESPONSE
    # =====================================================
    return {

        "answer": response.text,

        "retrieved_docs": retrieved_docs,

        "statistics": statistics,

        "explanation": explanation
    }