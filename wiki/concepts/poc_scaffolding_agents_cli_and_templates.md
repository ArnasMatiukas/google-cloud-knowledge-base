---
type: Guide
title: "One-Command PoC Scaffolding: Agents CLI, Starter Pack & ADK Samples"
description: "How to bootstrap full-stack, deployable Google Cloud multi-agent PoCs in under 60 seconds using Google Agents CLI (google-agents-cli), Agent Starter Pack, and official ADK Samples & Recipes."
category: "3. Agentic Frameworks"
tags: [agents-cli, agent-starter-pack, adk-samples, scaffolding, poc, cloud-run, agent-engine]
resource: "https://adk.dev/get-started/agents-cli/"
timestamp: "2026-10-16T12:48:00Z"
aliases: ["Agents CLI", "Agent Starter Pack", "ADK Samples", "PoC Scaffolding"]
status: "active"
---

# One-Command PoC Scaffolding: Agents CLI, Starter Pack & ADK Samples

In a 24- or 48-hour hackathon, never spend your first 4 hours wiring up boilerplate Dockerfiles, FastAPI servers, session stores, and deployment scripts from scratch. Google Cloud provides three official accelerators to bootstrap a working, deployable PoC in under 60 seconds.

---

## 1. Google Agents CLI (`google-agents-cli`) — Modern Scaffolding & Deployment

**Official Documentation:** [Agents CLI Quickstart](https://adk.dev/get-started/agents-cli/) · [Deploy with Agents CLI](https://adk.dev/deploy/agent-runtime/agents-cli/) · [Agents CLI Docs](https://google.github.io/agents-cli/)

`google-agents-cli` (`agents-cli`) is Google's unified CLI and skill pack for scaffolding, enhancing, and deploying [ADK 2.0](agent_development_kit_adk_and_skills.md) projects to [Vertex AI Agent Engine](vertex_ai_agent_engine.md), [Cloud Run](cloud_run_serverless_and_gpus.md), or GKE.

### Step 1: Install `google-agents-cli` & Coding Agent Skills
```bash
uvx google-agents-cli setup
```
This single command installs the `agents-cli` executable, ADK Python dependencies, and official ADK coding skills into [Antigravity 2.0](antigravity_2_paygo_and_ide_setup.md).

### Step 2: Configure Vertex AI (Agent Platform) Credentials in `.env`
Always configure your scaffolded project's `.env` file to use [Application Default Credentials (ADC)](gcp_cli_and_project_setup.md) on Vertex AI (never consumer API keys):
```dotenv
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_PROJECT=your-hackathon-project-id
GOOGLE_CLOUD_LOCATION=global
```

### Step 3: Enhance an Existing ADK Agent for Production Deployment
If you have a basic `my_agent/agent.py` package, run `scaffold enhance` from its parent directory to automatically generate `app/agent_engine_app.py`, `deployment/` scripts, `.cloudbuild/`, `Makefile`, and `tests/`:

```bash
agents-cli scaffold enhance --deployment-target agent_runtime
```

### Step 4: Deploy in One Command
```bash
gcloud config set project "$GOOGLE_CLOUD_PROJECT"
agents-cli deploy
```
*(Optional)* Provision Cloud Trace and prompt-response telemetry in one command:
```bash
agents-cli infra single-project
```

---

## 2. Agent Starter Pack (`uvx agent-starter-pack create`) — Full-Stack Templates

**Official Documentation:** [Agent Starter Pack Docs](https://googlecloudplatform.github.io/agent-starter-pack/) · [GitHub Repository](https://github.com/GoogleCloudPlatform/agent-starter-pack)

*(Note: Active feature development has consolidated into `google-agents-cli` above, while `agent-starter-pack` remains available for spinning up pre-packaged full-stack templates with embedded web UIs).*

Run the interactive generator without installing anything globally:
```bash
uvx agent-starter-pack create my-hackathon-poc
```

### Included PoC Templates:
- **`adk` (Base ReAct & Multi-Tool Agent):** Full-stack ADK agent with FastAPI backend and web playground.
- **`adk_a2a` (Distributed Agent2Agent):** Pre-wired [A2A protocol](protocols_mcp_and_a2a.md) server (`/.well-known/agent-card.json`) and client orchestrator.
- **`agentic_rag` (Grounded RAG Pipeline):** End-to-end [RAG architecture](rag_grounding_and_search.md) with document ingestion and vector retrieval.
- **`adk_live` (Real-Time Multimodal Voice/Video):** Pre-configured bidirectional WebSocket backend and audio/video web frontend powered by [`gemini-3.8-live`](multimodal_live_voice_and_media.md).

---

## 3. Official ADK Samples & Recipes (`google/adk-samples` & `google/adk-recipes`)

When your hackathon use case matches an existing industry vertical, clone and customize an official reference architecture:

- **[google/adk-samples](https://github.com/google/adk-samples):** Complete, multi-agent domain applications including Customer Service, Travel Concierge, Financial Advisor, Data Science (BigQuery/Code Execution), and Software Bug Assistant.
- **[google/adk-recipes](https://github.com/google/adk-recipes):** Focused, copy-paste code patterns for specific ADK 2.0 integrations, tools, callbacks, and multi-agent workflows.

> [!IMPORTANT]
> **Always Upgrade Sample Model IDs to Latest Tier Models:** When cloning community or older sample repositories, immediately update any hardcoded model strings in `agent.py` to [`gemini-3.8-flash`](agent_platform_models.md) (fast workhorse) or [`gemini-4-argon`](agent_platform_models.md) (deep reasoning/coding) with `GOOGLE_CLOUD_LOCATION="global"`.

---

## Related Concepts

- [Agent Development Kit (ADK 2.0) & Official Skills](agent_development_kit_adk_and_skills.md) — Core `LlmAgent` and `SkillToolset` patterns.
- [ADK 2.0 Graph Workflows, Human-in-the-Loop & Pause/Resume](adk_graph_workflows_and_hitl.md) — Building deterministic state graphs and human approval gates.
- [Custom Frontend UI & Real-Time Agent Streaming](agent_frontend_streaming_ag_ui.md) — Connecting React/Next.js UIs via `adk api_server` and `AG-UI`.
- [Vertex AI Agent Engine (Managed Runtime)](vertex_ai_agent_engine.md) — Hosting deployed agents with managed Sessions and Memory Bank.
