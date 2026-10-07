"""
Search API endpoints.

This module provides an API endpoint for performing similarity searches
against the application's vector store.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.vector_store import search_vector_store


router = APIRouter(prefix="/search", tags=["Search"])


class SearchRequest(BaseModel):
    """
    Request schema for the search endpoint.

    Attributes:
        query: The text query provided by the user.
        k: Number of relevant documents to retrieve.
    """
    query: str
    k: int = 4


@router.post("")
def search(request: SearchRequest):
    """
    Search the vector store using the user's query.

    The query is passed to the vector-store service, which performs
    similarity search and returns the most relevant documents.

    Args:
        request: SearchRequest containing the query and number of
            results to retrieve.

    Returns:
        A dictionary containing the original query and the retrieved
        documents along with their metadata.

    Raises:
        HTTPException: If an error occurs while searching the vector store.
    """

    try:
        results = search_vector_store(
            query=request.query,
            k=request.k,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    return {
        "query": request.query,
        "results": [
            {
                "text": doc.page_content,
                "metadata": doc.metadata,
            }
            for doc in results
        ],
    }