import pandas as pd

from sentence_transformers import (
    SentenceTransformer
)

from rag.vector_store import index


# =========================================================
# LOAD EMBEDDING MODEL
# =========================================================
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# =========================================================
# UPLOAD DATA TO PINECONE
# =========================================================
def upload_data_to_pinecone(
    csv_path,
    batch_size=100
):

    # LOAD DATASET
    df = pd.read_csv(csv_path)

    print("\nDataset Loaded")
    print(df.shape)

    vectors = []

    # ITERATE RECORDS

    start_index = 86100  # START FROM THIS INDEX TO AVOID DUPLICATES  
    for i, row in df.iloc[start_index:].iterrows():

        # CREATE TEXT REPRESENTATION
        text = f"""
        Year: {row['year']}
        State: {row['state_name']}
        District: {row['district_name']}
        Crop: {row['crop_name']}
        Crop Type: {row['crop_type']}
        Season: {row['season']}
        Area: {row['area']}
        Production: {row['production']}
        Yield: {row['yield']}
        """

        # GENERATE EMBEDDING
        embedding = embedding_model.encode(
            text
        ).tolist()

        # VECTOR OBJECT
        vectors.append(
            (
                str(i),
                embedding,
                {
                    "text": text,
                    "state": str(row["state_name"]),
                    "district": str(row["district_name"]),
                    "crop": str(row["crop_name"]),
                    "season": str(row["season"]),
                    "year": str(row["year"])
                }
            )
        )

        # BATCH UPSERT
        if len(vectors) >= batch_size:

            index.upsert(
                vectors=vectors
            )

            print(
                f"Uploaded {i + 1} records"
            )

            vectors = []

    # REMAINING VECTORS
    if vectors:

        index.upsert(
            vectors=vectors
        )

    print(
        "\nAll vectors uploaded successfully!"
    )


# =========================================================
# RETRIEVE CONTEXT
# =========================================================
def retrieve_context(
    query,
    top_k=5
):

    # QUERY EMBEDDING
    query_embedding = embedding_model.encode(
        query
    ).tolist()

    # SEARCH PINECONE
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    contexts = []

    for match in results["matches"]:

        contexts.append(
            match["metadata"]["text"]
        )

    return "\n".join(contexts)