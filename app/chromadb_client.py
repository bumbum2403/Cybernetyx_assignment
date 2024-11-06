import chromadb
from sentence_transformers import SentenceTransformer
from fastapi import HTTPException
import asyncio
import logging

logger = logging.getLogger(__name__)

# Constants
COLLECTION_NAME = "documents"
MODEL_NAME = 'all-MiniLM-L6-v2'

# Initialize ChromaDB client and the transformer model for embeddings
client = chromadb.Client()
model = SentenceTransformer(MODEL_NAME)

async def ingest_document(text: str, filename: str) -> None:
    """
    Ingest a document into ChromaDB.

    Args:
    text (str): Document text.
    filename (str): Document filename.

    Raises:
    HTTPException: If ingestion fails.
    """
    try:
        loop = asyncio.get_running_loop()
        embedding = await loop.run_in_executor(None, model.encode, [text])

        collection = client.get_or_create_collection(name=COLLECTION_NAME)
        collection.upsert(
            documents=[text],
            metadatas=[{"filename": filename}],
            embeddings=embedding
        )
        logger.info(f"Document {filename} ingested successfully.")
    except Exception as e:
        logger.error(f"Error ingesting document: {e}")
        raise HTTPException(status_code=500, detail="Failed to ingest document")


async def query_document(query: str) -> list:
    """
    Query ChromaDB for documents based on a query string.

    Args:
    query (str): Query string.

    Returns:
    list: List of documents found.

    Raises:
    HTTPException: If query fails or no documents are found.
    """
    try:
        loop = asyncio.get_running_loop()
        query_embedding = await loop.run_in_executor(None, model.encode, [query])

        collection = client.get_or_create_collection(name=COLLECTION_NAME)
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=5
        )

        if results and results.get('documents', []):
            return results['documents']
        else:
            raise HTTPException(status_code=404, detail="No documents found")
    except Exception as e:
        logger.error(f"Error querying ChromaDB: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")