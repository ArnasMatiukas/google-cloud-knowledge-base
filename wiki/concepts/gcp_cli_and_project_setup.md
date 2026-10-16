---
type: Guide
title: "Google Cloud CLI & Project Access Setup"
description: "Step-by-step 5-minute guide for hackathon and workshop attendees to authenticate gcloud CLI, configure Application Default Credentials (ADC), bind a pre-created GCP project, and enable core Agent Platform APIs."
category: "1. Onboarding & Setup"
tags: [gcloud, cli, adc, authentication, iam, quota-project, onboarding]
resource: "https://docs.cloud.google.com/gemini-enterprise-agent-platform/overview"
timestamp: "2026-10-16T10:25:00Z"
aliases: ["GCP CLI Setup", "ADC Setup", "gcloud auth", "Project Bootstrap"]
status: "active"
---

# Google Cloud CLI & Project Access Setup

During Google Cloud hackathons and workshops, participants are provided with a **Google Cloud user account (credentials)** and a **pre-created fresh GCP project**. Follow this guide to authenticate your terminal, configure Application Default Credentials (ADC) for SDKs and agents, and enable the required Google Cloud APIs.

---

## 1. Automated Preflight & Setup Script

You can verify your setup and enable all required hackathon APIs in one command from the repository root:

```bash
# Check gcloud login, project, and ADC status:
./scripts/verify_gcp_setup.sh

# Automatically enable all core hackathon APIs on your active project:
./scripts/verify_gcp_setup.sh --enable-apis
```

---

## 2. Step-by-Step Manual CLI Onboarding

### Step 1: Sign In with Your Provided Google Cloud Credentials
Authenticate your `gcloud` CLI session using the account credentials provided by the event organizers:

```bash
gcloud auth login
```

*(If you cannot install the `gcloud` CLI locally, open [Google Cloud Shell](https://shell.cloud.google.com) directly in your browser using your hackathon credentials—`gcloud`, Python, Node.js, and Go are pre-installed).*

### Step 2: List & Bind Your Pre-Created GCP Project
Find your assigned project ID and set it as your active default project:

```bash
gcloud projects list

export GOOGLE_CLOUD_PROJECT="your-hackathon-project-id"
gcloud config set project "$GOOGLE_CLOUD_PROJECT"
```

### Step 3: Configure Application Default Credentials (ADC) & Quota Project
Python (`google-genai`, `google-adk`), TypeScript, Go, local MCP servers, and [Antigravity 2.0 Pay-As-You-Go](antigravity_2_paygo_and_ide_setup.md) authenticate automatically through **Application Default Credentials (ADC)**—eliminating the need to create or download insecure service account JSON keys:

```bash
gcloud auth application-default login
gcloud auth application-default set-quota-project "$GOOGLE_CLOUD_PROJECT"
```

> [!IMPORTANT]
> Always run `gcloud auth application-default set-quota-project "$GOOGLE_CLOUD_PROJECT"`. Without a quota project bound to your ADC credentials, calls to Vertex AI (`aiplatform.googleapis.com`) or the Developer Knowledge API will fail with `403 PERMISSION_DENIED: SERVICE_DISABLED` or `CONSUMER_INVALID`.

### Step 4: Enable Core Hackathon APIs
Pre-created fresh GCP projects have most service APIs disabled by default. Enable the core agentic, serverless, and database stack in a single command:

```bash
gcloud services enable \
  aiplatform.googleapis.com \
  businessaicode.googleapis.com \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  bigquery.googleapis.com \
  sqladmin.googleapis.com \
  alloydb.googleapis.com \
  spanner.googleapis.com \
  firestore.googleapis.com \
  storage.googleapis.com \
  discoveryengine.googleapis.com \
  secretmanager.googleapis.com \
  developerknowledge.googleapis.com
```

### Step 5: Export Agent Platform Environment Variables
Configure your shell or `.env` file (see `.env.example` in the repo root) so the [Google GenAI SDK](google_genai_sdk_vertex.md) and [Agent Development Kit (ADK)](agent_development_kit_adk_and_skills.md) route all calls through **Google Cloud Agent Platform (Vertex AI)** on the `global` endpoint:

```bash
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT="your-hackathon-project-id"
export GOOGLE_CLOUD_LOCATION="global"
```

---

## 3. Troubleshooting Common Hackathon Auth Errors

- **`403 PERMISSION_DENIED: Vertex AI API has not been used in project ... before or it is disabled`**
  - **Cause:** Either `aiplatform.googleapis.com` is not enabled on `$GOOGLE_CLOUD_PROJECT`, or your ADC quota project points to an old project.
  - **Fix:** Run `gcloud services enable aiplatform.googleapis.com --project="$GOOGLE_CLOUD_PROJECT"` and `gcloud auth application-default set-quota-project "$GOOGLE_CLOUD_PROJECT"`.
- **`DefaultCredentialsError: Your default credentials were not found`**
  - **Cause:** You ran `gcloud auth login` (which authenticates the `gcloud` CLI binary) but did not run `gcloud auth application-default login` (which creates `~/.config/gcloud/application_default_credentials.json` for client SDKs).
  - **Fix:** Run `gcloud auth application-default login`.
- **`ValueError: Missing key inputs argument! To use the Google AI API, provide (api_key) ...`**
  - **Cause:** `GOOGLE_GENAI_USE_VERTEXAI=true` is not set in the environment, causing the SDK to default to consumer AI Studio mode instead of Vertex AI.
  - **Fix:** Set `export GOOGLE_GENAI_USE_VERTEXAI=true` or initialize `genai.Client(vertexai=True, project=..., location="global")`.

---

## Related Concepts

- [Antigravity 2.0 Pay-As-You-Go & IDE Setup](antigravity_2_paygo_and_ide_setup.md) — Connecting Antigravity 2.0 to your hackathon GCP project.
- [Agent Platform Latest Models Catalog](agent_platform_models.md) — Choosing the single latest model per tier.
- [Google GenAI SDK on Vertex AI](google_genai_sdk_vertex.md) — Calling Gemini models with ADC in Python.
- [Security, FinOps & Quota Guardrails](security_finops_and_quotas.md) — Avoiding rate limits and managing secrets.
