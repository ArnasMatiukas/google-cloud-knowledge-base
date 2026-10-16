---
name: graphrag-and-embeddings
description: >-
  Build Multimodal Vector RAG and GraphRAG pipelines on Google Cloud using
  `gemini-embedding-2` and `gemini-3.8-flash` across Cloud Spanner Graph,
  AlloyDB AI / Cloud SQL `pgvector`, BigQuery, or lightweight `NetworkX` / OKF
  Wiki graphs. Use whenever the user wants to embed text/images/audio/video/PDFs
  or build a knowledge graph / GraphRAG system.
---

# Multimodal Embeddings (`gemini-embedding-2`) & GraphRAG Builder Skill

Use this skill when designing or implementing semantic search, multimodal RAG, or **GraphRAG** on Google Cloud.

## 1. Always Use `gemini-embedding-2` for Embeddings

`gemini-embedding-2` is Google Cloud's unified multimodal embedding model ([https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/embeddings](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/embeddings)):
- **Single Vector Space Across Modalities:** Directly embeds **Text, Images (`image/png`, `image/jpeg`), Audio, Video, and PDFs** (up to **8,192 input tokens** per call) without separate OCR or transcription steps.
- **Matryoshka Dimensions (`output_dimensionality`):** Use `768` or `1536` for fast ANN indexing in Spanner/Postgres/BigQuery, or `3072` for maximum precision.

```python
from google import genai
from google.genai import types

client = genai.Client(vertexai=True, project="YOUR_PROJECT_ID", location="us-central1")

response = client.models.embed_content(
    model="gemini-embedding-2",
    contents=[
        "Service outage root cause in payment gateway",
        types.Part.from_uri(file_uri="gs://my-bucket/architecture_diagram.png", mime_type="image/png"),
    ],
    config=types.EmbedContentConfig(
        task_type="RETRIEVAL_DOCUMENT",
        output_dimensionality=768,
    ),
)
```

## 2. Choosing the Right GraphRAG Architecture on Google Cloud

Select from the 4 proven GraphRAG architectures documented in [`wiki/concepts/graphrag_architectures_on_gcp.md`](../../../wiki/concepts/graphrag_architectures_on_gcp.md):

1. **Option 1 — Rapid 15-Minute Hackathon GraphRAG (`NetworkX` + `gemini-embedding-2` or OKF Wiki Graph):**
   - Best when a hackathon team needs zero database provisioning time.
   - Extracts entity-relationship triples with `gemini-3.8-flash` structured outputs, embeds node summaries with `gemini-embedding-2`, stores the property graph in `NetworkX` (persisted as JSON in GCS/Firestore), finds top-$K$ seed nodes via cosine similarity, and expands a 2-hop ego-graph (`nx.ego_graph(G, seed, radius=2)`).
2. **Option 2 — AlloyDB AI or Cloud SQL for PostgreSQL (`pgvector` + Apache AGE / Recursive CTEs):**
   - Best for PostgreSQL apps needing transactional tables + vector search + multi-hop graph traversal in one SQL query (`WITH RECURSIVE` over `nodes` and `edges` tables indexed with `pgvector` HNSW/ScaNN).
3. **Option 3 — Serverless Analytical GraphRAG on BigQuery (`AI.GENERATE_TABLE` + `VECTOR_SEARCH`):**
   - Best for large document corpora in GCS Object Tables with zero infrastructure management. Extracts triples in SQL using `AI.GENERATE_TABLE`, embeds nodes with `ML.GENERATE_EMBEDDING`, and joins 1–3 hops in standard SQL.
4. **Option 4 — Enterprise Multi-Model GraphRAG on Cloud Spanner Graph (`GRAPH_TABLE` + Vector KNN/ANN):**
   - Best for globally scalable Zero-ETL operational GraphRAG combining ISO GQL (`MATCH (a)-[e]->(b)`) and `COSINE_DISTANCE` / `APPROX_COSINE_DISTANCE` in a single query.

Read [`wiki/concepts/gemini_embedding_2_multimodal.md`](../../../wiki/concepts/gemini_embedding_2_multimodal.md) and [`wiki/concepts/graphrag_architectures_on_gcp.md`](../../../wiki/concepts/graphrag_architectures_on_gcp.md) for complete copy-pasteable code and SQL/GQL queries.
