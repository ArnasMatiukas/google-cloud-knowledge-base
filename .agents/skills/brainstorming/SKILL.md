---
name: brainstorming
description: >-
  Turn hackathon ideas into concrete Google Cloud & Agent Platform architectures
  through structured, collaborative design exploration. Use before building a
  new feature, multi-agent workflow, or application.
---

# Brainstorming Hackathon Ideas into Google Cloud Architectures

## Overview

Help hackathon participants turn rough ideas into concrete, deployable Google Cloud architectures grounded in the local OKF Wiki (`wiki/index.md`).

## Step-by-Step Process

### 1. Ground in the Local Knowledge Base First
- Activate `llm-wiki-search` (`./scripts/okf_wiki_cli.py search "<topic>"` or read `wiki/index.md`) to check the recommended latest models (`gemini-4-argon`, `gemini-3.8-flash`, `gemini-embedding-2`, `gemini-3.8-live`, etc.), storage options, and ADK patterns.
- Strictly use **Google Cloud Agent Platform (Vertex AI)** with ADC (`GOOGLE_GENAI_USE_VERTEXAI=true`). Never propose Google AI Studio.

### 2. Clarify Scope Quickly
- Ask focused questions one at a time to clarify user intent, data sources, latency requirements, and hackathon time constraints.
- Prefer concise multiple-choice options when trade-offs exist.

### 3. Propose 2–3 Concrete GCP Architectures
- Lead with the **recommended hackathon fast-path** (e.g., ADK + `gemini-3.8-flash` on Cloud Run, or rapid GraphRAG with `gemini-embedding-2`), followed by enterprise-scale alternatives (e.g., Vertex AI Agent Engine, Cloud Spanner Graph, AlloyDB AI).
- Explain trade-offs in setup time, complexity, and capabilities.

### 4. Present the Design Incrementally
- Cover:
  1. **Model Selection** (exact latest model IDs per tier)
  2. **Agent & Tool Orchestration** (ADK 2.0, MCP servers, A2A)
  3. **Data & Retrieval Layer** (BigQuery, Cloud SQL/AlloyDB `pgvector`, Spanner Graph, Firestore, GCS)
  4. **Hosting & Deployment** (Cloud Run or Vertex AI Agent Engine)
