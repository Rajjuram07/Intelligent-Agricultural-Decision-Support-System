# =========================================================
# RAG WORKSPACE CONFIGURATION
# =========================================================

import os


# =========================================================
# DATA PATHS
# =========================================================
BASE_DIR = "rag_workspace"

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

FAISS_DIR = os.path.join(
    BASE_DIR,
    "faiss_index"
)

CACHE_DIR = os.path.join(
    BASE_DIR,
    "cache"
)


# =========================================================
# FILE PATHS
# =========================================================
DATASET_PATH = os.path.join(
    DATA_DIR,
    "agriculture_climate_data.csv"
)

FAISS_INDEX_PATH = os.path.join(
    FAISS_DIR,
    "agriculture_index.faiss"
)

DOCUMENTS_PATH = os.path.join(
    CACHE_DIR,
    "documents.pkl"
)

EMBEDDINGS_PATH = os.path.join(
    CACHE_DIR,
    "embeddings.npy"
)


# =========================================================
# RAG SETTINGS
# =========================================================
TOP_K_RESULTS = 5

SIMILARITY_THRESHOLD = 0.70

MAX_CONTEXT_DOCUMENTS = 5

EMBEDDING_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)


# =========================================================
# QUERY HISTORY SETTINGS
# =========================================================
MAX_QUERY_HISTORY = 20


# =========================================================
# GEMINI SETTINGS
# =========================================================
DEFAULT_TEMPERATURE = 0.7

DEFAULT_MODEL = (
    "gemini-3-flash-preview"
)


# =========================================================
# CREATE REQUIRED DIRECTORIES
# =========================================================
os.makedirs(
    DATA_DIR,
    exist_ok=True
)

os.makedirs(
    FAISS_DIR,
    exist_ok=True
)

os.makedirs(
    CACHE_DIR,
    exist_ok=True
)

# =========================================================
# PINECONE CONFIGURATION
# =========================================================
PINECONE_API_KEY = os.getenv(
    "PINECONE_API_KEY"
)

PINECONE_INDEX_NAME = os.getenv(
    "PINECONE_INDEX_NAME"
)