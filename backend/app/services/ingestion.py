"""
PDF ingestion and text chunking utilities.

This module loads PDF documents, enriches their page metadata,
and splits the extracted content into smaller chunks suitable
for embedding and vector storage.
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def extract_and_chunk_pdf(
    file_path: str,
    source_id: str,
    filename: str,
):
    """
    Extract text from a PDF and split it into smaller document chunks.

    The PDF is first loaded page by page using PyPDFLoader. Metadata
    identifying the source, filename, file path, and page number is
    then added to each page. The pages are split into overlapping
    text chunks using RecursiveCharacterTextSplitter.

    Each generated chunk is assigned a unique chunk ID based on the
    source ID and its position in the document.

    Args:
        file_path: Path to the PDF file.
        source_id: Unique identifier assigned to the source document.
        filename: Original name of the uploaded PDF.

    Returns:
        A list of LangChain Document objects containing the extracted
        text chunks and their associated metadata.
    """

    # Load the PDF and extract its pages.
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    print(f"Extracted {len(pages)} pages")

    # Add application-specific metadata to each page.
    for page in pages:
        page.metadata["source_id"] = source_id
        page.metadata["filename"] = filename
        page.metadata["file_path"] = str(file_path)

        # PyPDFLoader uses zero-based page numbers.
        # Convert them to human-readable one-based page numbers.
        page_number = page.metadata.get("page", 0)
        page.metadata["page"] = page_number + 1

    # Configure the text splitter.
    #
    # chunk_size: Maximum target size of each chunk.
    # chunk_overlap: Number of characters shared between
    #                consecutive chunks.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    # Split the pages into smaller documents suitable
    # for embedding and vector search.
    chunks = splitter.split_documents(pages)

    # Assign a stable ID to every generated chunk.
    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = f"{source_id}_{index}"

    print(f"Created {len(chunks)} chunks")

    return chunks