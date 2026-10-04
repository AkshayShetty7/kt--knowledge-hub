"""
Source upload API.

This module provides an endpoint for uploading PDF documents.
Uploaded PDFs are stored locally, processed into text chunks,
and added to the vector store for later similarity search.
"""

from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.ingestion import extract_and_chunk_pdf
from app.services.vector_store import create_or_update_vector_store


router = APIRouter(prefix="/sources", tags=["Sources"])


# Directory used to store uploaded source PDFs.
UPLOAD_DIR = Path(__file__).resolve().parents[3] / "storage" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_source(file: UploadFile = File(...)):
    """
    Upload and process a PDF source.

    The uploaded file is validated to ensure that it is a PDF.
    A unique source ID is generated, and the file is stored in the
    application's upload directory.

    The PDF is then processed into text chunks. These chunks are
    converted into embeddings and added to the FAISS vector store.

    Args:
        file: PDF file uploaded through the API request.

    Returns:
        A dictionary containing:
            - source_id: Unique identifier assigned to the uploaded file.
            - filename: Original filename.
            - status: Upload status.
            - pages: Number of pages processed.
            - chunks: Number of text chunks generated.

    Raises:
        HTTPException: If the uploaded file is not a PDF.
    """

    # Validate the uploaded file type.
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed",
        )

    # Generate a unique ID so that uploaded files can be identified
    # independently of their original filenames.
    source_id = str(uuid4())

    # Sanitize the filename by keeping only the filename component.
    filename = Path(file.filename).name

    # Store the file using the generated source ID.
    file_path = UPLOAD_DIR / f"{source_id}_{filename}"

    # Read the uploaded file and save it to disk.
    contents = await file.read()
    file_path.write_bytes(contents)

    # PDF -> pages -> text chunks
    chunks = extract_and_chunk_pdf(
        file_path=str(file_path),
        source_id=source_id,
        filename=filename,
    )

    # Chunks -> embeddings -> FAISS vector store
    create_or_update_vector_store(chunks)

    return {
        "source_id": source_id,
        "filename": filename,
        "status": "uploaded",
        "pages": len(set(
            chunk.metadata["page"]
            for chunk in chunks
        )),
        "chunks": len(chunks),
    }