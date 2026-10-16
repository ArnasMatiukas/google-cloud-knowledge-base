---
type: Guide
title: "Google Cloud Run: Serverless Containers, Agents & GPUs"
description: "Rapidly deploying web frontends, FastAPI backends, ADK 2.0 agents, remote MCP servers, and GPU-accelerated Gemma 4 open-weight models on Google Cloud Run."
category: "4. Compute & Hosting"
tags: [cloud-run, serverless, containers, gpu, gemma-4, oidc, jobs, deployment]
resource: "https://docs.cloud.google.com/run/docs"
timestamp: "2026-10-16T10:25:00Z"
aliases: ["Cloud Run", "Cloud Run GPUs", "gcloud run deploy", "Cloud Run Jobs"]
status: "active"
---

# Google Cloud Run: Serverless Containers, Agents & GPUs

**Google Cloud Run** ([https://cloud.google.com/run](https://cloud.google.com/run) · [Docs](https://docs.cloud.google.com/run/docs)) is the fastest way to take a hackathon prototype—whether a Next.js/React frontend, a FastAPI backend, a [Google ADK 2.0 agent](agent_development_kit_adk_and_skills.md), a remote [MCP or A2A server](protocols_mcp_and_a2a.md), or a WebSocket [Gemini Live API](multimodal_live_voice_and_media.md) gateway—from your laptop to a live HTTPS URL in under 60 seconds.

---

## 1. One-Command Source Deployment (`--source .`)

You do not need Docker installed locally. Cloud Run builds your container in the cloud (using a `Dockerfile` if present, or Google Cloud Buildpacks for Python/Node.js/Go) and deploys it:

```bash
export GOOGLE_CLOUD_PROJECT="$(gcloud config get-value project)"
export REGION="europe-west1" # or us-central1

gcloud run deploy hackathon-app \
  --source . \
  --project "$GOOGLE_CLOUD_PROJECT" \
  --region "$REGION" \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT},GOOGLE_CLOUD_LOCATION=global,GOOGLE_GENAI_USE_VERTEXAI=true"
```

---

## 2. Granting Cloud Run IAM Access to Agent Platform & Data Stores

Cloud Run services authenticate via their attached Service Account using Application Default Credentials (ADC)—never bake service account JSON keys into container images. Grant `roles/aiplatform.user` so your deployed service can call [`gemini-4-argon`](agent_platform_models.md), [`gemini-3.8-flash`](agent_platform_models.md), and [`gemini-embedding-2`](gemini_embedding_2_multimodal.md):

```bash
PROJECT_NUMBER="$(gcloud projects describe "$GOOGLE_CLOUD_PROJECT" --format='value(projectNumber)')"
RUNTIME_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

# Allow calling Agent Platform (Vertex AI) models:
gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
  --member="serviceAccount:${RUNTIME_SA}" \
  --role="roles/aiplatform.user"
```

---

## 3. Deploying Open-Weight Models (`gemma-4-31b-it`) on Cloud Run GPUs

When your hackathon project requires self-hosting an open-weight model ([`gemma-4-31b-it` or `gemma-4-26b-a4b-it`](agent_platform_models.md)) with on-demand NVIDIA L4 GPUs that scale to zero when idle:

```bash
gcloud run deploy gemma-4-endpoint \
  --image="us-docker.pkg.dev/cloudrun/container/gemma/gemma4-31b" \
  --project="$GOOGLE_CLOUD_PROJECT" \
  --region="us-central1" \
  --gpu=1 \
  --gpu-type="nvidia-l4" \
  --cpu=8 \
  --memory=32Gi \
  --no-cpu-throttling \
  --max-instances=2
```

---

## 4. Key Cloud Run Patterns & Gotchas for Hackathons

- **WebSockets & Streaming (`gemini-3.8-live` / SSE):**
  - Cloud Run natively supports WebSockets and HTTP/2 streaming up to 60 minutes per request. Set `--timeout=3600` and `--session-affinity` when hosting stateful WebSocket gateways.
- **Background Processing & Ingestion (`Cloud Run Jobs`):**
  - For batch data ingestion, PDF parsing, or [GraphRAG entity extraction](graphrag_architectures_on_gcp.md) that runs to completion without serving HTTP traffic, deploy a **Cloud Run Job** (`gcloud run jobs create my-ingest-job --source . && gcloud run jobs execute my-ingest-job`).
- **Securing Backend Microservices (`--no-allow-unauthenticated`):**
  - Deploy public web UIs with `--allow-unauthenticated`, and deploy internal APIs or MCP/A2A sub-agents with `--no-allow-unauthenticated`. The frontend service can mint an OIDC identity token from the Cloud Run metadata server (`http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=https://backend-xyz.a.run.app`) and pass `Authorization: Bearer <ID_TOKEN>`.

---

## Related Concepts

- [Agent Development Kit (ADK 2.0) & Official Skills](agent_development_kit_adk_and_skills.md) — Deploying ADK agents with `adk deploy cloud_run`.
- [Vertex AI Agent Engine (Managed Runtime)](vertex_ai_agent_engine.md) — When to choose Agent Engine vs. Cloud Run.
- [Google Cloud MCP Servers Catalog](gcp_mcp_servers_catalog.md) — Using `@google-cloud/cloud-run-mcp` so your coding agent deploys directly to Cloud Run.
- [Security, FinOps & Quota Guardrails](security_finops_and_quotas.md) — Injecting secrets from Secret Manager (`--set-secrets`).
