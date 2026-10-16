---
type: Guide
title: "Gemini Embedding 2 (Multimodal Embeddings)"
description: "Complete guide to gemini-embedding-2 on Google Cloud Agent Platform: unified multimodal embeddings across text, images, audio, video, and PDFs (8,192 tokens), Matryoshka dimensionality, and task-specific optimization."
category: "2. Models & SDKs"
tags: [gemini-embedding-2, embeddings, multimodal, rag, graphrag, matryoshka, vector-search]
resource: "https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/embeddings"
timestamp: "2026-10-16T10:25:00Z"
aliases: ["gemini-embedding-2", "Multimodal Embeddings", "Vertex AI Embeddings"]
status: "active"
---

# Gemini Embedding 2 (Multimodal Embeddings)

**`gemini-embedding-2`** is Google Cloud's latest canonical embedding model on Agent Platform (Vertex AI). Unlike legacy text-only embedding models (`text-embedding-004`, `text-embedding-005`), `gemini-embedding-2` natively maps **Text, Images, Audio, Video, and PDFs** into a **single unified vector space** with an **8,192-token context window**.

**Official Documentation:** [Embeddings on Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/embeddings)

---

## 1. Why `gemini-embedding-2` Changes Hackathon RAG & GraphRAG

1. **Zero-Pipeline Multimodal Retrieval:** You can embed architecture diagrams (`image/png`), product photos (`image/jpeg`), meeting audio clips (`audio/mp3`, `audio/wav`), demo videos (`video/mp4`), PDF documents (`application/pdf`), and raw text directly—without building brittle OCR, image-captioning, or ASR preprocessing pipelines first.
2. **Cross-Modal Similarity Search:** A plain-text user query (`"Where is the authentication bottleneck in the checkout flow?"`) can directly retrieve the matching slide diagram image, video segment, or PDF page via cosine similarity.
3. **8,192 Input Token Context Window:** Embeds full document sections, code files, or multi-page transcripts in a single vector without aggressive micro-chunking.
4. **Matryoshka Representation Learning (`output_dimensionality`):** Supports truncating the output vector from `3072` dimensions down to `1536`, `768`, `512`, or `256` dimensions with minimal accuracy loss, speeding up vector index queries in [Cloud Spanner Graph](graphrag_architectures_on_gcp.md), [AlloyDB / Cloud SQL `pgvector`](datastores_cloudsql_alloydb_spanner_firestore_gcs.md), and [BigQuery](bigquery_ai_and_analytics.md).

---

## 2. Python SDK Implementation (`google-genai`)

```python
from google import genai
from google.genai import types

client = genai.Client(
    vertexai=True,
    project="your-hackathon-project-id",
    location="us-central1",  # or global / europe-west1
)

# 1. Embed Multimodal Documents & Media (Indexing Time)
doc_response = client.models.embed_content(
    model="gemini-embedding-2",
    contents=[
        "Cloud Run scales stateless containers automatically from zero to N instances.",
        types.Part.from_uri(
            file_uri="gs://my-hackathon-bucket/system_architecture.png",
            mime_type="image/png",
        ),
        types.Part.from_uri(
            file_uri="gs://my-hackathon-bucket/spec_sheet.pdf",
            mime_type="application/pdf",
        ),
    ],
    config=types.EmbedContentConfig(
        task_type="RETRIEVAL_DOCUMENT",
        output_dimensionality=768,
    ),
)

for idx, emb in enumerate(doc_response.embeddings):
    print(f"Item {idx} vector length: {len(emb.values)}")

# 2. Embed a User Search Query (Query Time)
query_response = client.models.embed_content(
    model="gemini-embedding-2",
    contents="How does Cloud Run scale containers and connect to the database?",
    config=types.EmbedContentConfig(
        task_type="RETRIEVAL_QUERY",
        output_dimensionality=768,
    ),
)
query_vector = query_response.embeddings[0].values
```

---

## 3. Choosing the Right `task_type`

Always specify `task_type` in `EmbedContentConfig` so `gemini-embedding-2` optimizes the vector geometry for your workload:

| `task_type` Value | When to Use It |
| :--- | :--- |
| `RETRIEVAL_DOCUMENT` | Embedding knowledge base articles, chunks, images, videos, PDFs, or [GraphRAG](graphrag_architectures_on_gcp.md) node summaries for storage in a vector index. |
| `RETRIEVAL_QUERY` | Embedding a user's search question or agent retrieval query at runtime. |
| `CODE_RETRIEVAL_QUERY` | Embedding a natural-language query used to search over source code snippets or functions. |
| `QUESTION_ANSWERING` | Embedding questions matched against a corpus of FAQ answers. |
| `FACT_VERIFICATION` | Embedding claims to retrieve supporting or refuting evidence passages. |
| `SEMANTIC_SIMILARITY` | Symmetric comparison between two items (e.g., deduplicating GraphRAG entities or matching user profiles). |
| `CLASSIFICATION` | Using embeddings as features for intent or category classification. |
| `CLUSTERING` | Grouping related documents, tickets, or multimodal assets by topic. |

---

## 4. Calling `gemini-embedding-2` Directly from SQL

Both **BigQuery** and **AlloyDB / Cloud SQL for PostgreSQL** can invoke `gemini-embedding-2` directly inside SQL queries without external Python glue code:

- **In BigQuery (`ML.GENERATE_EMBEDDING`):** See [BigQuery AI & Analytics](bigquery_ai_and_analytics.md).
- **In Spanner Graph / AlloyDB / Cloud SQL:** See [How to Build GraphRAGs on Google Cloud](graphrag_architectures_on_gcp.md) and [Operational Data Stores](datastores_cloudsql_alloydb_spanner_firestore_gcs.md).

---

## Related Concepts

- [How to Build GraphRAGs on Google Cloud](graphrag_architectures_on_gcp.md) — Combining `gemini-embedding-2` vector seed lookup with multi-hop graph traversal.
- [RAG, Grounding & Search on Google Cloud](rag_grounding_and_search.md) — Choosing between OKF Wiki, Vertex AI Search, and custom multimodal Vector RAG.
- [Agent Platform Latest Models Catalog](agent_platform_models.md) — Full Q4 2026 model catalog.
- [Google GenAI SDK on Vertex AI](google_genai_sdk_vertex.md) — Unified Python SDK patterns.
