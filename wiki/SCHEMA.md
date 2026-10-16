# Google Cloud Knowledge Base — OKF Wiki Schema & Governance

This wiki implements the **Open Knowledge Format (OKF v0.2)** and Andrej Karpathy's **three-layer LLM Wiki architecture** to maintain a persistent, cross-linked knowledge base for Google Cloud hackathons, workshops, and agentic engineering.

---

## 1. Core Repository Policy Mandates

1. **100% Google Cloud Agent Platform (Vertex AI) Native:**
   - Never include or recommend consumer API-key workflows (`GEMINI_API_KEY`).
   - Every SDK snippet, CLI tool, and agent configuration MUST authenticate via Google Cloud IAM / Application Default Credentials (ADC) with `GOOGLE_GENAI_USE_VERTEXAI=true`.
2. **Single Latest Model Per Tier (Zero Ambiguity):**
   - Only the single newest, most capable Google model of each tier is documented so hackathon participants never have to guess which model ID to choose:
     - **Frontier Reasoning, Coding & Video (Pro Tier):** `gemini-4-argon`
     - **High-Throughput Agent Workhorse (Flash Tier):** `gemini-3.8-flash`
     - **Ultra-Fast / High-Volume (Flash-Lite Tier):** `gemini-3.5-flash-lite`
     - **Multimodal Embeddings Tier:** `gemini-embedding-2`
     - **Text-to-Speech (TTS) Tier:** `gemini-3.8-flash-tts` (and `gemini-3.8-flash-lite-tts`)
     - **Speech-to-Text / Transcription (ASR) Tier:** `gemini-3.5-transcribe-live` (streaming) / `gemini-3.5-transcribe` (batch)
     - **Real-Time Bidirectional Voice & Video (Live API):** `gemini-3.8-live` (and `gemini-3.8-live-extended-thinking`)
     - **Image Generation & Editing Tier:** `gemini-nano-banana-2.1` (and `gemini-3.1-flash-lite-image`)
     - **Video & Audio Generation / Editing Tier:** `gemini-omni-1.1-flash`
     - **Music & Song Generation Tier:** `lyria-3.5`
     - **Open-Weight Models (Cloud Run GPUs):** `gemma-4-31b-it` (and `gemma-4-26b-a4b-it`)
3. **Validated Canonical Links Only:**
   - Every external documentation URL must resolve with `HTTP 200 OK` and point to canonical `docs.cloud.google.com`, `adk.dev`, `antigravity.google`, or official GitHub repositories.

---

## 2. Three-Layer Architecture

```text
wiki/
├── SCHEMA.md                 # Layer 3: Governance, frontmatter specification, and policy rules
├── CONCEPT_REGISTRY.json     # Machine-readable concept registry, aliases, tags, and paths
├── index.md                  # Layer 2 Catalog: Human & agent-readable progressive disclosure index
├── log.md                    # Chronological changelog of additions & updates
├── raw/                      # Layer 1: Raw Sources (immutable source repository)
│   ├── MANIFEST.json         # Ingest manifest (sources, SHA-256 hashes, timestamps)
│   └── PROCESSING_QUEUE.json # Queue tracking raw item distillation status
└── concepts/                 # Layer 2: Atomic OKF v0.2 Markdown concept & guide pages
    ├── index.md              # Auto-generated concept directory listing
    └── *.md                  # Domain concept pages
```

---

## 3. Concept Document Specification (OKF v0.2)

Every concept document in `wiki/concepts/<slug>.md` MUST begin with a valid YAML frontmatter block:

```markdown
---
type: Guide
title: "Descriptive Concept Title"
description: "A concise 1-2 sentence executive summary."
category: "1. Onboarding & Setup"
tags: [gcloud, adc, vertex-ai, auth]
resource: "https://docs.cloud.google.com/gemini-enterprise-agent-platform/overview"
timestamp: "2026-10-16T10:00:00Z"
aliases: ["Alternative Name", "Acronym"]
status: "active"
---
```

---

## 4. CLI Maintenance Commands

```bash
# Search the wiki
./scripts/okf_wiki_cli.py search "graphrag"

# Query concept registry to prevent duplicates
./scripts/okf_wiki_cli.py manage-concepts --action=query --term="embedding"

# Rebuild index (wiki/index.md, wiki/concepts/index.md, and wiki/CONCEPT_REGISTRY.json)
./scripts/okf_wiki_cli.py rebuild-index

# Verify OKF compliance and relative link integrity (must return 0 errors, 0 warnings)
./scripts/okf_wiki_cli.py verify

# Record update in changelog
./scripts/okf_wiki_cli.py log-entry --title "Updated Concept" --message "Summary of change" --pages "concepts/agent_platform_models.md"
```
