---
name: llm-wiki-search
description: >-
  Search, browse, and retrieve curated Google Cloud knowledge from the local
  Open Knowledge Format (OKF v0.2) LLM Wiki in this repository (`wiki/`). Use
  FIRST whenever the user asks about Google Cloud models, ADK, Antigravity 2.0
  PayGo setup, Cloud Run, BigQuery, Data Stores, RAG, GraphRAG, Gemini Embedding 2,
  Live API, or MCP servers.
---

# LLM Wiki Search Skill (Primary Entry Point)

This skill guides you in navigating and querying the local **Open Knowledge Format (OKF v0.2) LLM Wiki** in `wiki/`.

## Core Mandate

1. **Always Consult the Local Wiki First:** Before proposing an architecture, selecting a Gemini model ID, or writing Google Cloud / ADK code, check `wiki/index.md` or run `./scripts/okf_wiki_cli.py search "<topic>"`.
2. **Enforce Latest Models & Vertex AI Only:** The local wiki indexes **only** the single latest, most capable model per tier on **Google Cloud Agent Platform (Vertex AI)** and strictly forbids consumer `GEMINI_API_KEY` workflows.

## Progressive Disclosure Workflow

### Step 1: Browse the Root Catalog
Inspect the lightweight index to see all documented concepts, categories, and summaries without exhausting your context window:
- Read `wiki/index.md` (or `wiki/concepts/index.md`).

### Step 2: Fast Keyword & Tag Search via CLI
Run the zero-dependency OKF CLI search utility:

```bash
# Human-readable ranked results:
./scripts/okf_wiki_cli.py search "<query>"

# Machine-readable JSON output:
./scripts/okf_wiki_cli.py search "<query>" --json
```

### Step 3: Query Concept Registry by Alias or Term
To check exact concept slugs and aliases in `wiki/CONCEPT_REGISTRY.json`:

```bash
./scripts/okf_wiki_cli.py manage-concepts --action=query --term="<term>"
```

### Step 4: Read Targeted Concept Pages & Follow Cross-Links
Read only the specific concept page(s) needed in `wiki/concepts/<slug>.md` and follow relative Markdown links (`[Target Concept](target_concept.md)`) when deeper multi-service context is required. If a parameter or edge case is not in the local wiki, escalate to the `gcp-knowledge-mcp` skill.
