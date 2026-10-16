---
type: Guide
title: "Google BigQuery: Serverless Analytics, In-SQL Gemini & Vector Search"
description: "How to use Google BigQuery in hackathons for serverless analytics, calling gemini-3.8-flash and gemini-embedding-2 directly inside SQL (AI.GENERATE, ML.GENERATE_EMBEDDING), Object Tables over GCS media, and VECTOR_SEARCH."
category: "5. Data & Analytics"
tags: [bigquery, bqml, ai-generate, vector-search, object-tables, sql, analytics]
resource: "https://docs.cloud.google.com/bigquery/docs"
timestamp: "2026-10-16T10:25:00Z"
aliases: ["BigQuery", "BigQuery ML", "AI.GENERATE", "BigQuery Vector Search"]
status: "active"
---

# Google BigQuery: Serverless Analytics, In-SQL Gemini & Vector Search

**Google BigQuery** ([https://cloud.google.com/bigquery](https://cloud.google.com/bigquery) · [Docs](https://docs.cloud.google.com/bigquery/docs)) is Google Cloud's serverless, multimodal enterprise data warehouse. For hackathons, BigQuery lets you run LLM enrichment, structured extraction, multimodal analysis over [Cloud Storage (GCS)](datastores_cloudsql_alloydb_spanner_firestore_gcs.md) files, and vector similarity search **entirely in standard GoogleSQL** with zero servers to manage.

---

## 1. Cost & Quota Guardrail: Always Dry-Run First

Before running queries against large public datasets (`bigquery-public-data.*`) or production tables, always estimate bytes scanned using `--dry_run` (which costs \$0) and set `--maximum_bytes_billed`:

```bash
# 1. Dry-run to inspect bytes processed:
bq query --use_legacy_sql=false --dry_run \
  'SELECT COUNT(*) FROM `bigquery-public-data.usa_names.usa_1910_current`'

# 2. Execute with a 1 GB safety cap:
bq query --use_legacy_sql=false --maximum_bytes_billed=1000000000 \
  'SELECT name, SUM(number) AS total FROM `bigquery-public-data.usa_names.usa_1910_current` GROUP BY name ORDER BY total DESC LIMIT 10'
```

---

## 2. Calling Gemini Directly Inside SQL (`AI.GENERATE` & `AI.GENERATE_TABLE`)

After creating a BigQuery Cloud Resource Connection and remote model pointing to [`gemini-3.8-flash`](agent_platform_models.md), you can enrich thousands of rows or extract structured columns directly in SQL:

```sql
-- 1. Register the remote Gemini 3.8 Flash model in BigQuery
CREATE OR REPLACE MODEL `my_dataset.gemini_flash_model`
REMOTE WITH CONNECTION `us.vertex_ai_conn`
OPTIONS (endpoint = 'gemini-3.8-flash');

-- 2. Extract structured schema columns from raw customer feedback using AI.GENERATE_TABLE
SELECT
  ticket_id,
  sentiment,
  urgency_score,
  extracted_entities
FROM
  AI.GENERATE_TABLE(
    MODEL `my_dataset.gemini_flash_model`,
    (SELECT ticket_id, raw_text AS prompt FROM `my_dataset.support_tickets`),
    STRUCT(
      "sentiment STRING, urgency_score INT64, extracted_entities ARRAY<STRING>" AS output_schema
    )
  );
```

---

## 3. Multimodal Embeddings (`gemini-embedding-2`) & `VECTOR_SEARCH` in SQL

Combine **Object Tables** (which expose unstructured PDFs, images, audio, and video in GCS buckets as SQL rows) with [`gemini-embedding-2`](gemini_embedding_2_multimodal.md) and `VECTOR_SEARCH`:

```sql
-- 1. Register gemini-embedding-2 in BigQuery
CREATE OR REPLACE MODEL `my_dataset.embedding_model`
REMOTE WITH CONNECTION `us.vertex_ai_conn`
OPTIONS (endpoint = 'gemini-embedding-2');

-- 2. Generate 768-d embeddings over a table of documents
CREATE OR REPLACE TABLE `my_dataset.doc_embeddings` AS
SELECT *
FROM ML.GENERATE_EMBEDDING(
  MODEL `my_dataset.embedding_model`,
  (SELECT doc_id, title, content FROM `my_dataset.knowledge_docs`),
  STRUCT(TRUE AS flatten_json_output, 'RETRIEVAL_DOCUMENT' AS task_type, 768 AS output_dimensionality)
);

-- 3. Run semantic similarity search with VECTOR_SEARCH
SELECT
  base.doc_id,
  base.title,
  distance
FROM VECTOR_SEARCH(
  TABLE `my_dataset.doc_embeddings`,
  'ml_generate_embedding_result',
  (
    SELECT ml_generate_embedding_result
    FROM ML.GENERATE_EMBEDDING(
      MODEL `my_dataset.embedding_model`,
      (SELECT 'How do I configure PayGo in Antigravity 2.0?' AS content),
      STRUCT(TRUE AS flatten_json_output, 'RETRIEVAL_QUERY' AS task_type, 768 AS output_dimensionality)
    )
  ),
  top_k => 5,
  distance_type => 'COSINE'
);
```

---

## Related Concepts

- [How to Build GraphRAGs on Google Cloud](graphrag_architectures_on_gcp.md) — Using BigQuery `AI.GENERATE_TABLE` + `VECTOR_SEARCH` for serverless analytical GraphRAG.
- [Gemini Embedding 2 (Multimodal Embeddings)](gemini_embedding_2_multimodal.md) — Embedding text, images, audio, video, and PDFs.
- [Operational Data Stores: Spanner, AlloyDB, Cloud SQL, Firestore & GCS](datastores_cloudsql_alloydb_spanner_firestore_gcs.md) — Choosing between analytical (BigQuery) and transactional data stores.
- [Google Cloud Native Integrated & Local MCP Servers](gcp_mcp_servers_catalog.md) — Connecting agents directly to BigQuery via its native remote MCP endpoint (`https://bigquery.googleapis.com/mcp`).
