---
type: Guide
title: "Security, FinOps & Quota Guardrails for Hackathons"
description: "Essential hackathon survival guide for avoiding 429 RESOURCE_EXHAUSTED quota errors on Vertex AI, managing third-party secrets in Secret Manager, protecting agents with Model Armor, and keeping GCP costs under control."
category: "8. MCP & Guardrails"
tags: [quotas, 429, global-endpoint, secret-manager, model-armor, finops, security, iam]
resource: "https://docs.cloud.google.com/gemini-enterprise-agent-platform/overview"
timestamp: "2026-10-16T10:25:00Z"
aliases: ["Vertex AI Quotas", "429 RESOURCE_EXHAUSTED", "Secret Manager", "Hackathon Guardrails"]
status: "active"
---

# Security, FinOps & Quota Guardrails for Hackathons

Nothing derails a live hackathon demo faster than an unexpected `429 RESOURCE_EXHAUSTED` error or a leaked credential pushed to GitHub. Follow these four guardrails from hour one.

---

## 1. How to Avoid `429 RESOURCE_EXHAUSTED` on Agent Platform

1. **Always Use `location="global"` for Frontier Models:**
   - Single-region endpoints (like `us-central1` or `europe-west1`) have fixed regional TPU pools and lower default per-project RPM/TPM quotas.
   - Setting `GOOGLE_CLOUD_LOCATION="global"` (or `genai.Client(vertexai=True, project=..., location="global")`) routes [`gemini-4-argon`, `gemini-3.8-flash`, `gemini-3.5-flash-lite`, `gemini-3.8-live`, `gemini-nano-banana-2.1`, and `gemini-omni-1.1-flash`](agent_platform_models.md) through Google Cloud's global dynamic capacity router.
2. **Use `thinking_level="LOW"` on `gemini-3.8-flash` for High-Frequency Loops:**
   - By default, `gemini-3.8-flash` runs with `thinking_level="HIGH"`, which can consume thousands of thinking tokens per call. When running parallel batch extraction (e.g., [GraphRAG ingestion](graphrag_architectures_on_gcp.md)) or rapid UI classification, set `thinking_level="LOW"` to reduce token consumption by 70–85% and cut latency in half.
3. **Enable `contextWindowCompression` on `gemini-3.8-live`:**
   - Live bidirectional audio/video sessions re-bill cumulative session tokens on every turn. Always set `ContextWindowCompressionConfig` with a `SlidingWindow` (see [Multimodal Live API, Voice & Media](multimodal_live_voice_and_media.md)).

---

## 2. Zero Hardcoded Keys: ADC + Secret Manager

1. **For All Google Cloud Services (`Vertex AI`, `BigQuery`, `Spanner`, `Firestore`, `GCS`):**
   - Never create or commit a service account `.json` key file.
   - Locally, use `gcloud auth application-default login` ([CLI & Project Setup](gcp_cli_and_project_setup.md)).
   - On [Cloud Run](cloud_run_serverless_and_gpus.md) or [Vertex AI Agent Engine](vertex_ai_agent_engine.md), the attached service account provides ADC automatically.
2. **For External Third-Party API Tokens (GitHub, Slack, Stripe, etc.):**
   - Store third-party tokens in **Google Cloud Secret Manager** and mount them into Cloud Run as environment variables:
     ```bash
     # 1. Create the secret:
     printf "my-third-party-token" | gcloud secrets create external-api-token --data-file=-

     # 2. Inject into Cloud Run at deploy time:
     gcloud run deploy hackathon-app \
       --source . \
       --region europe-west1 \
       --set-secrets="EXTERNAL_API_TOKEN=external-api-token:latest"
     ```

---

## 3. BigQuery & Database Cost Guardrails

- **Always Dry-Run BigQuery Queries:** Pass `--dry_run` or set `--maximum_bytes_billed=1000000000` (1 GB) when querying [BigQuery](bigquery_ai_and_analytics.md) so a missing `WHERE` clause on a multi-terabyte public dataset never drains your hackathon project credits.
- **Scale Down Idle GPU Services:** When deploying [`gemma-4-31b-it` on Cloud Run GPUs](cloud_run_serverless_and_gpus.md), keep `--min-instances=0` so the NVIDIA L4 GPU scales down to zero cost when not actively serving requests.

---

## Related Concepts

- [Google Cloud CLI & Project Access Setup](gcp_cli_and_project_setup.md) — Setting up ADC and quota projects properly.
- [Antigravity 2.0 Pay-As-You-Go & IDE Setup](antigravity_2_paygo_and_ide_setup.md) — Using "Login with Business" so coding agents don't hit consumer free-tier rate limits.
- [Agent Platform Latest Models Catalog](agent_platform_models.md) — Selecting the right model tier and endpoint.
