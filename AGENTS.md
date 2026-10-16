# Google Cloud Knowledge Base — Agent System Contract

## Purpose
This repository serves as a curated **Open Knowledge Format (OKF v0.2) LLM Wiki** (`wiki/`) and out-of-the-box **Antigravity 2.0** skill pack (`.agents/skills/`) for Google Cloud hackathons and workshops.

---

## Core Mandates for AI Coding Agents

1. **Always Search the Local OKF Wiki First (`llm-wiki-search`):**
   - Before proposing an architecture, picking a model ID, or writing Google Cloud / ADK code, inspect [`wiki/index.md`](wiki/index.md) or run `./scripts/okf_wiki_cli.py search "<topic>"`.
   - If live documentation details are needed beyond `wiki/concepts/`, use the [`gcp-knowledge-mcp`](.agents/skills/gcp-knowledge-mcp/SKILL.md) skill (`google-developer-knowledge` and `adk-docs-mcp`).
2. **100% Google Cloud Agent Platform (Vertex AI) Native:**
   - Never suggest or generate code for consumer API-key workflows (`GEMINI_API_KEY`).
   - Always authenticate via Google Cloud IAM / Application Default Credentials (ADC) with `GOOGLE_GENAI_USE_VERTEXAI=true`, `GOOGLE_CLOUD_PROJECT`, and `GOOGLE_CLOUD_LOCATION="global"`.
3. **Use Only the Single Latest Model Per Tier:**
   - **Frontier Reasoning, Coding & Video (Pro Tier):** `gemini-4-argon` (`location="global"`)
   - **High-Throughput Agent Workhorse (Flash Tier):** `gemini-3.8-flash` (`location="global"`)
   - **Ultra-Fast / High-Volume (Flash-Lite Tier):** `gemini-3.5-flash-lite` (`location="global"`)
   - **Multimodal Embeddings Tier:** `gemini-embedding-2`
   - **Text-to-Speech (TTS) Tier:** `gemini-3.8-flash-tts` / `gemini-3.8-flash-lite-tts` (`location="global"`)
   - **Speech-to-Text / Transcription (ASR) Tier:** `gemini-3.5-transcribe-live` / `gemini-3.5-transcribe` (`location="global"`)
   - **Real-Time Bidirectional Voice & Video (Live API):** `gemini-3.8-live` / `gemini-3.8-live-extended-thinking` (`location="global"`)
   - **Image Generation & Editing Tier:** `gemini-nano-banana-2.1` / `gemini-3.1-flash-lite-image` (`location="global"`)
   - **Video & Audio Generation / Editing Tier:** `gemini-omni-1.1-flash` (`location="global"`)
   - **Music & Song Generation Tier:** `lyria-3.5` (`location="global"`)
   - **Open-Weight Models (Cloud Run GPUs):** `gemma-4-31b-it` / `gemma-4-26b-a4b-it`
   - Never use older or retired model generations.
4. **Antigravity 2.0 Out-of-the-Box Skills (`.agents/skills/`):**
   - Keep all workspace skills in `.agents/skills/<skill-name>/SKILL.md` and MCP definitions in `.agents/mcp_config.json`. Do not recreate a legacy `.gemini/` directory.

---

## Rules for `README.md`
When adding new tools or updating `README.md`, you MUST adhere to the following rules:

1. **Be Concise:** Keep it straight to the point. No fluff or unnecessary information.
2. **Use Bullet Points for Lists:** When a section lists multiple items or supported products, always use a bulleted list for readability.
3. **Follow the Structure:** Every entry must strictly follow the specific format below.
4. **Entry Format:**
   - **Heading:** A dedicated section/heading for the tool, service, or framework.
   - **Description:** A brief 1-2 sentence description.
   - **Source Formatting:** The `**Source:**` line must always be placed on a new, isolated line (separated by a blank line from the description). Provide a direct link to the official source or documentation.

---

## Rules for Maintaining `wiki/` (OKF v0.2)
Whenever adding or modifying concept pages in `wiki/concepts/`:
1. Run `./scripts/okf_wiki_cli.py rebuild-index` to update `wiki/index.md`, `wiki/concepts/index.md`, and `wiki/CONCEPT_REGISTRY.json`.
2. Run `./scripts/okf_wiki_cli.py verify` and ensure **0 errors** and **0 warnings**.
3. Log the update via `./scripts/okf_wiki_cli.py log-entry`.
