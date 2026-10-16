---
type: Concept
title: "Operational Data Stores: Spanner Graph, AlloyDB, Cloud SQL, Firestore & GCS"
description: "Decision matrix and quick-start patterns for choosing the right Google Cloud operational database or storage service in hackathons: Cloud Spanner Graph, AlloyDB AI, Cloud SQL for PostgreSQL (pgvector), Firestore, and Cloud Storage (GCS)."
category: "5. Data & Analytics"
tags: [spanner, alloydb, cloud-sql, pgvector, firestore, gcs, storage, databases]
resource: "https://docs.cloud.google.com/firestore/native/docs"
timestamp: "2026-10-16T10:25:00Z"
aliases: ["GCP Data Stores", "Cloud SQL pgvector", "AlloyDB AI", "Firestore", "Cloud Storage"]
status: "active"
---

# Operational Data Stores: Spanner Graph, AlloyDB, Cloud SQL, Firestore & GCS

Picking the right data layer in the first 30 minutes of a hackathon saves hours of refactoring. Use the decision table below to match your workload to the right Google Cloud storage service.

---

## 1. Hackathon Data Store Decision Matrix

| Data Store | Best For | Provisioning Time | Vector / Graph Support | Official Docs |
| :--- | :--- | :--- | :--- | :--- |
| **Cloud Storage (GCS)** | Unstructured files, PDFs, images, audio, video (`gs://` URIs passed directly to Gemini), and static assets. | **~5 seconds** (`gcloud storage buckets create`) | Via [BigQuery Object Tables](bigquery_ai_and_analytics.md) or [`gemini-embedding-2`](gemini_embedding_2_multimodal.md) | [GCS Docs](https://docs.cloud.google.com/storage/docs) |
| **Firestore (Native Mode)** | Serverless real-time JSON document store for app state, user profiles, chat history, and rapid 24h hackathon prototypes. | **~15 seconds** (zero instance warmup) | Native KNN Vector Search (`find_nearest`) | [Firestore Docs](https://docs.cloud.google.com/firestore/native/docs) |
| **Cloud SQL for PostgreSQL** | Familiar relational SQL + `pgvector` semantic search + `apache_age` / recursive CTE graph queries. | ~5–8 minutes | `vector` (`pgvector` HNSW/IVFFlat) + `apache_age` | [Cloud SQL Vector Docs](https://docs.cloud.google.com/sql/docs/postgres/generate-manage-vector-embeddings) |
| **AlloyDB for PostgreSQL** | High-performance enterprise PostgreSQL with **AlloyDB AI** (`alloydb_scann` index up to 10x faster than standard HNSW) and inline `google_ml_integration`. | ~8–12 minutes (requires VPC peering/PSC) | `alloydb_scann` + `vector` + `apache_age` | [AlloyDB AI Docs](https://docs.cloud.google.com/alloydb/docs/ai) |
| **Cloud Spanner Graph** | Globally scalable **multi-model relational + ISO GQL Property Graph + Vector Search** in a single Zero-ETL engine (ideal for [GraphRAG](graphrag_architectures_on_gcp.md)). | **~30 seconds** (Free Trial / granular instance) | Native `GRAPH_TABLE` (ISO GQL) + `COSINE_DISTANCE` / `APPROX_COSINE_DISTANCE` | [Spanner Graph Docs](https://docs.cloud.google.com/spanner/docs/graph/overview) |

---

## 2. Quick-Start CLI & Code Snippets

### A. Cloud Storage (GCS) — Staging Multimodal Files for Gemini
```bash
export BUCKET_NAME="${GOOGLE_CLOUD_PROJECT}-media"
gcloud storage buckets create "gs://${BUCKET_NAME}" --location=us-central1
gcloud storage cp ./sample_diagram.png "gs://${BUCKET_NAME}/sample_diagram.png"
```
Once uploaded to `gs://`, pass the URI directly into [`gemini-4-argon`, `gemini-3.8-flash`](google_genai_sdk_vertex.md), or [`gemini-embedding-2`](gemini_embedding_2_multimodal.md) via `types.Part.from_uri(file_uri="gs://...", mime_type="...")`.

### B. Firestore — Zero-Config Serverless Document & Vector Store
Create the default database in Native mode:
```bash
gcloud firestore databases create --location=nam5 --type=firestore-native
```
Read/write documents in Python using ADC:
```python
from google.cloud import firestore

db = firestore.Client(project="your-hackathon-project-id")
db.collection("sessions").document("user-123").set({
    "topic": "GraphRAG Architecture",
    "status": "active",
})
```

### C. Cloud SQL for PostgreSQL / AlloyDB with `pgvector`
Enable the `vector` extension and create an HNSW index for 768-dimensional [`gemini-embedding-2`](gemini_embedding_2_multimodal.md) embeddings:
```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE knowledge_chunks (
    chunk_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    modality TEXT DEFAULT 'text',
    gcs_uri TEXT,
    embedding vector(768)
);

CREATE INDEX ON knowledge_chunks USING hnsw (embedding vector_cosine_ops);
```

---

## Related Concepts

- [How to Build GraphRAGs on Google Cloud](graphrag_architectures_on_gcp.md) — Combining Spanner Graph, AlloyDB/Cloud SQL `pgvector`, or BigQuery with `gemini-embedding-2`.
- [BigQuery AI & Analytics](bigquery_ai_and_analytics.md) — Serverless analytical queries and `VECTOR_SEARCH`.
- [RAG, Grounding & Search on Google Cloud](rag_grounding_and_search.md) — End-to-end RAG decision framework.
- [Google Cloud Native Integrated & Local MCP Servers](gcp_mcp_servers_catalog.md) — Connecting agents directly to Spanner (`https://spanner.googleapis.com/mcp`), AlloyDB (`https://alloydb.googleapis.com/mcp`), Cloud SQL (`https://sqladmin.googleapis.com/mcp`), and Firestore (`https://firestore.googleapis.com/mcp`) via native remote MCP endpoints.
