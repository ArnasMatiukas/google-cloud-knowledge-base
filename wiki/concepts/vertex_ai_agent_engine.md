---
type: Architecture
title: "Vertex AI Agent Engine (Managed Agent Runtime)"
description: "Deploying and scaling ADK and custom agents on Google Cloud's managed Vertex AI Agent Engine (ReasoningEngine) with managed Sessions, long-term Memory Bank, Code Execution Sandbox, and Cloud Trace."
category: "3. Agentic Frameworks"
tags: [agent-engine, reasoning-engine, vertex-ai, sessions, memory-bank, opentelemetry, adk]
resource: "https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale"
timestamp: "2026-10-16T10:25:00Z"
aliases: ["Vertex AI Agent Engine", "ReasoningEngine", "Agent Runtime", "Memory Bank"]
status: "active"
---

# Vertex AI Agent Engine (Managed Agent Runtime)

**Vertex AI Agent Engine** (`ReasoningEngine`, [https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale)) is Google Cloud Agent Platform's fully managed runtime for deploying, scaling, and governing [ADK agents](agent_development_kit_adk_and_skills.md) and custom container (BYOC) agents.

---

## 1. Core Managed Capabilities

1. **Managed Agent Runtime (`reasoningEngines`):** Packages your Python ADK agent (or custom container image) into an auto-scaling, IAM-protected HTTPS & [A2A endpoint](protocols_mcp_and_a2a.md).
2. **Managed Sessions (`VertexAiSessionService`):** Persists multi-turn conversation history, event logs, and session state (`session.state`) across stateless requests—replacing local `InMemorySessionService`.
3. **Long-Term Memory Bank (`VertexAiMemoryBankService`):** Automatically extracts, consolidates, and retrieves durable user facts and preferences across separate sessions using managed embeddings and LLM consolidation.
4. **Code Execution Sandbox:** Provides a secure, isolated micro-environment for agents that need to generate and execute Python data-analysis or plotting code at runtime.
5. **Built-In OpenTelemetry Observability:** Streams structured span traces, token metrics, and tool execution logs directly into **Cloud Trace**, **Cloud Monitoring**, and **Cloud Logging**.

---

## 2. Deploying an ADK Agent to Agent Engine

### Option A: Deploy via `agents-cli` / `adk deploy`
```bash
adk deploy agent_engine \
  --project="$GOOGLE_CLOUD_PROJECT" \
  --region="us-central1" \
  --staging_bucket="gs://${GOOGLE_CLOUD_PROJECT}-agent-staging" \
  --display_name="hackathon-concierge-agent" \
  ./concierge_agent
```

### Option B: Deploy Programmatically in Python (`vertexai.agent_engines`)
```python
import vertexai
from vertexai import agent_engines
from concierge_agent.agent import root_agent

vertexai.init(
    project="your-hackathon-project-id",
    location="us-central1",
    staging_bucket="gs://your-hackathon-project-id-agent-staging",
)

# 1. Wrap your ADK root_agent with telemetry enabled
app = agent_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True,
)

# 2. Deploy to managed Vertex AI Agent Engine
remote_agent = agent_engines.create(
    app,
    requirements=["google-adk>=1.25.0", "google-genai", "pydantic"],
    display_name="hackathon-concierge-agent",
)

# 3. Stream queries against the deployed agent
for event in remote_agent.stream_query(
    user_id="attendee-01",
    message="Recommend a GraphRAG architecture for 50,000 PDF manuals.",
):
    print(event)
```

---

## 3. Key Deployment & Observability Gotchas

- **Populating the Console "Sessions" and "Traces" Tabs (Custom BYOC Containers):**
  - When deploying a standard Python `AdkApp(agent=root_agent, enable_tracing=True)`, Agent Engine automatically wires `VertexAiSessionService` and Cloud Trace.
  - If you deploy a custom Bring-Your-Own-Container (`container_spec`) running a custom FastAPI server, avoid `InMemoryRunner` (which keeps sessions in container RAM and leaves the Console **Sessions** tab empty). Instead, initialize your `Runner` with `VertexAiSessionService(project=PROJECT_ID, location=LOCATION, agent_engine_id=ENGINE_ID)` and pass `GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY=true` in `deploymentSpec.env`.
- **Reserved Environment Variables in `deploymentSpec.env`:**
  - Never manually pass `GOOGLE_CLOUD_AGENT_ENGINE_ID` or `GOOGLE_CLOUD_AGENT_ENGINE_LOCATION` inside `deploymentSpec.env`—Agent Engine reserves and injects those automatically (passing them manually returns `HTTP 400 Bad Request`).
- **When to Choose Agent Engine vs. Cloud Run:**
  - Choose **Vertex AI Agent Engine** when you want turnkey managed `VertexAiSessionService`, **Memory Bank**, native [A2A](protocols_mcp_and_a2a.md) registration, and Agent Platform Console trace visualization.
  - Choose **[Google Cloud Run](cloud_run_serverless_and_gpus.md)** when you are deploying a full-stack web UI (Next.js/React + FastAPI), custom WebSocket [Gemini Live API](multimodal_live_voice_and_media.md) gateway, or GPU-backed open-weight model (`gemma-4-31b-it`).

---

## Related Concepts

- [Agent Development Kit (ADK 2.0) & Official Skills](agent_development_kit_adk_and_skills.md) — Building and testing ADK agents locally before deployment.
- [Cloud Run Serverless & GPUs](cloud_run_serverless_and_gpus.md) — Alternative serverless container hosting for full-stack apps and agents.
- [Agentic Protocols: MCP & A2A](protocols_mcp_and_a2a.md) — Exposing and invoking agents across projects via the Agent2Agent protocol.
- [Security, FinOps & Quota Guardrails](security_finops_and_quotas.md) — Least-privilege IAM and telemetry best practices.
