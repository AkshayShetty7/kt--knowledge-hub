"""
Vector store management.

This module handles document embeddings and persistent FAISS vector
storage. It provides functionality to create or update the vector
index, load an existing index, and perform similarity searches.
"""

from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# Directory where the FAISS index and associated metadata are stored.
VECTOR_DB_DIR = (
    Path(__file__).resolve().parents[3]
    / "storage"
    / "vector_db"
)

VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)


# Embedding model used to convert text chunks into numerical vectors.
EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"


# Load the embedding model once when this module is initialized.
# Reusing the same model avoids loading it for every request.
print("Loading BGE embedding model...")

_embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    model_kwargs={
        # Run embedding generation on the CPU.
        "device": "cpu",
    },
    encode_kwargs={
        # Normalize vectors for more consistent similarity calculations.
        "normalize_embeddings": True,

        # Process documents in batches to improve embedding throughput.
        "batch_size": 32,
    },
)

print("BGE embedding model ready!")


def create_or_update_vector_store(chunks):
    """
    Create a new FAISS index or add chunks to an existing index.

    If a FAISS index already exists, it is loaded and the supplied
    document chunks are added to it. Otherwise, a new FAISS index is
    created from the supplied chunks.

    The resulting vector store is persisted to disk.

    Args:
        chunks: List of document chunks to embed and store.

    Returns:
        The FAISS vector store containing the supplied chunks.
    """

    index_file = VECTOR_DB_DIR / "index.faiss"

    if index_file.exists():
        print("Existing FAISS index found.")
        print("Adding new chunks...")

        # Load the existing FAISS index and add the new chunks.
        vector_store = FAISS.load_local(
            str(VECTOR_DB_DIR),
            _embeddings,
            allow_dangerous_deserialization=True,
        )

        vector_store.add_documents(chunks)

    else:
        print("No FAISS index found.")
        print("Creating a new FAISS index...")

        # Create a new FAISS index from the supplied document chunks.
        vector_store = FAISS.from_documents(
            documents=chunks,
            embedding=_embeddings,
        )

    # Persist the updated index to disk.
    vector_store.save_local(str(VECTOR_DB_DIR))

    print(f"Added {len(chunks)} chunks to FAISS")
    print(f"Vector DB: {VECTOR_DB_DIR}")

    return vector_store


def load_vector_store():
    """
    Load the existing FAISS vector store from disk.

    Returns:
        The loaded FAISS vector store if an index exists;
        otherwise, None.
    """

    index_file = VECTOR_DB_DIR / "index.faiss"

    if not index_file.exists():
        return None

    return FAISS.load_local(
        str(VECTOR_DB_DIR),
        _embeddings,
        allow_dangerous_deserialization=True,
    )


def search_vector_store(query: str, k: int = 4):
    """
    Search the vector store for documents similar to a query.

    The existing FAISS index is loaded and a similarity search is
    performed using the supplied query.

    Args:
        query: Text query used to search the vector store.
        k: Maximum number of similar documents to return.

    Returns:
        A list of the most similar documents. Returns an empty list
        if no vector store exists.
    """

    vector_store = load_vector_store()

    # No index exists yet, so there are no documents to search.
    if vector_store is None:
        return []

    return vector_store.similarity_search(
        query,
        k=k,
    )