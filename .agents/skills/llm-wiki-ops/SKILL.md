---
name: llm-wiki-ops
description: >-
  Operate, ingest new sources, re-index, and verify the Open Knowledge Format
  (OKF v0.2) LLM Wiki in this repository (`wiki/`). Use when adding new concepts
  to the knowledge base, rebuilding `wiki/index.md`, or validating links.
---

# LLM Wiki Operations & Ingestion Skill

This skill guides you in maintaining, extending, and verifying the local **Open Knowledge Format (OKF v0.2) LLM Wiki** in `wiki/` using `./scripts/okf_wiki_cli.py`.

## Operational Workflow

### 1. Ingest Raw Sources into Layer 1 (`wiki/raw/`)
```bash
# Ingest from a URL:
./scripts/okf_wiki_cli.py ingest --source "https://docs.cloud.google.com/..." --title "Service Spec" --category "Data & Analytics"

# Ingest raw notes or text:
./scripts/okf_wiki_cli.py ingest --text "Technical architecture notes..." --title "Architecture Notes" --category "RAG & Knowledge"
```

### 2. Check for Existing Concepts Before Creating New Files
Prevent duplicate pages by querying `wiki/CONCEPT_REGISTRY.json`:
```bash
./scripts/okf_wiki_cli.py manage-concepts --action=query --term="<topic>"
```

### 3. Author or Update Atomic Concept Pages (`wiki/concepts/<slug>.md`)
Every file in `wiki/concepts/` MUST start with valid OKF v0.2 YAML frontmatter (`type`, `title`, `description`, `category`, `tags`, `resource`, `timestamp`, `aliases`, `status`) and follow the rules in `wiki/SCHEMA.md` (100% Vertex AI native, zero AI Studio, single latest model per tier).

### 4. Rebuild Indices & Synchronize Registry
Whenever a concept page is added or edited, regenerate `wiki/index.md`, `wiki/concepts/index.md`, and `wiki/CONCEPT_REGISTRY.json`:
```bash
./scripts/okf_wiki_cli.py rebuild-index
```

### 5. Verify Conformance & Link Hygiene
Run verification and confirm **0 errors** and **0 warnings**:
```bash
./scripts/okf_wiki_cli.py verify
```

### 6. Record Changelog Entry
Append the update to `wiki/log.md`:
```bash
./scripts/okf_wiki_cli.py log-entry --title "<Update Title>" --message "<Summary>" --pages "concepts/<slug>.md"
```
