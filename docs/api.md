# Search API

## POST /search

Performs a similarity search against the vector store.

### Request

```json
{
    "query": "What is machine learning?",
    "k": 4
}
```
### Response

```json

{
    "query": "What is machine learning?",
    "results": [
        {
            "text": "...",
            "metadata": {}
        }
    ]
}

```