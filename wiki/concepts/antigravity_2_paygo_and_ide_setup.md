---
type: Guide
title: "Antigravity 2.0 Pay-As-You-Go (PayGo) & IDE Setup"
description: "How to configure Antigravity 2.0 Desktop App, CLI (agy), and IDE extensions as Pay-As-You-Go with hackathon Google Cloud accounts and pre-created GCP projects, and how .agents/skills/ loads out of the box."
category: "1. Onboarding & Setup"
tags: [antigravity, paygo, agy, ide, skills, mcp, gemini-enterprise]
resource: "https://antigravity.google/"
timestamp: "2026-10-16T10:25:00Z"
aliases: ["Antigravity 2.0", "Antigravity PayGo", "agy CLI", "Login with Business"]
status: "active"
---

# Antigravity 2.0 Pay-As-You-Go (PayGo) & IDE Setup

**Antigravity 2.0** ([https://antigravity.google/](https://antigravity.google/)) is Google's agentic development platform. When participating in a hackathon or workshop with a provided Google Cloud account and pre-created GCP project, you should run Antigravity 2.0 in **Pay-As-You-Go (PayGo) mode** billed to your GCP project so you get full enterprise token quotas and access to [`gemini-4-argon`](agent_platform_models.md) and [`gemini-3.8-flash`](agent_platform_models.md).

---

## 1. Supported Surfaces for Google Cloud PayGo

Download and use any of the three official enterprise-ready surfaces from [https://antigravity.google/download](https://antigravity.google/download):

- **Antigravity 2.0 Desktop App (Hub):** Standalone multi-agent workspace and trajectory manager.
- **Antigravity CLI (`agy`):** Terminal-native coding agent that inherits `gcloud` Application Default Credentials (ADC).
- **Antigravity IDE Extensions:** Official plugins for **VS Code**, **JetBrains IDEs**, and **Zed**.

> [!WARNING]
> **Do Not Use the Consumer-Only Standalone IDE Fork:** Never use the legacy consumer "Antigravity IDE" fork—it only supports consumer Gmail sign-in and cannot bill token consumption to a Google Cloud project.

---

## 2. How to Sign In as Pay-As-You-Go (Avoid the Consumer Login Trap)

### Critical Rule: Click "Login with Business" (Never "Continue with Google")
On the Antigravity 2.0 login screen, you will see two sign-in paths:
1. ❌ **"Continue with Google" (Consumer Path — DO NOT CLICK):** Routes your account to the consumer free tier, which exhausts rate limits in ~20 minutes and ignores your GCP project billing.
2. ✅ **"Login with Business" / "Use business account" (or *"Prefer to use a GCP project?"*):** Connects Antigravity 2.0 to Google Cloud IAM and bills token usage Pay-As-You-Go against your pre-created GCP project.

### Step-by-Step Setup

#### Step 1: Enable Required APIs & Verify IAM Roles
Ensure `aiplatform.googleapis.com` and `businessaicode.googleapis.com` are enabled (via [Google Cloud CLI & Project Access Setup](gcp_cli_and_project_setup.md)) and that your hackathon user account has:
- `roles/aiplatform.user` (*Vertex AI / Agent Platform User* — required for PayGo model token billing)
- `roles/discoveryengine.agentspaceUser` (*Gemini Enterprise User*)
- `roles/mcp.toolUser` (*MCP Tool User* — required for calling Google Cloud Remote MCP servers)

If you are the Owner/Editor of your pre-created hackathon project, you can bind these roles directly:
```bash
export GOOGLE_CLOUD_PROJECT="$(gcloud config get-value project)"
export USER_EMAIL="$(gcloud config get-value account)"

for ROLE in roles/aiplatform.user roles/discoveryengine.agentspaceUser roles/mcp.toolUser; do
  gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
    --member="user:${USER_EMAIL}" \
    --role="$ROLE"
done
```

#### Step 2: Authenticate Antigravity 2.0 Desktop App or IDE Extension
1. Launch **Antigravity 2.0 Desktop App** or open the **Antigravity extension** in VS Code / JetBrains.
2. Click **"Login with Business"** (or **"Prefer to use a GCP project?"**).
3. Sign in with your provided Google Cloud hackathon credentials.
4. Select or paste your **GCP Project ID** (`$GOOGLE_CLOUD_PROJECT`) and set location to `global`.

#### Step 3: Authenticate Antigravity CLI (`agy`)
The `agy` CLI automatically inherits your `gcloud` Application Default Credentials (ADC):
```bash
gcloud auth login --update-adc
gcloud config set project "$GOOGLE_CLOUD_PROJECT"
gcloud auth application-default set-quota-project "$GOOGLE_CLOUD_PROJECT"

# Start agy in the repository root:
agy
```

#### Step 4: Enable AI Developer Tools PayGo / Overages in Cloud Console
If your hackathon project is configured with Gemini Enterprise AI Developer Tools:
1. Open the Cloud Console settings page:
   `https://console.cloud.google.com/gemini-enterprise/settings/ai-developer-tools?project=YOUR_PROJECT_ID`
2. Turn **On** **AI Developer Tools**.
3. Enable **Overages / Pay-As-You-Go** so agent turns continue seamlessly on project billing without hitting daily seat caps.
4. Under **Model availability**, verify that **Gemini 4 Argon** (`gemini-4-argon`) is toggled **On**.

---

## 3. Out-of-the-Box Workspace Skills (`.agents/skills/`) & MCPs

### Why This Repo Uses `.agents/skills/` Instead of `.gemini/`
Antigravity 2.0's workspace customization loader automatically scans `.agents/skills/<skill-name>/SKILL.md` (as well as root `GEMINI.md` and `AGENTS.md`) and ignores legacy `<workspace>/.gemini/skills/` directories.

When you open `google-cloud-knowledge-base` in Antigravity 2.0, all **8 workspace skills** in `.agents/skills/` load automatically out of the box with zero manual configuration:
- `llm-wiki-search` — Progressive disclosure search across this `wiki/` knowledge base.
- `gcp-knowledge-mcp` — Live lookups via Google Developer Knowledge MCP & ADK Docs MCP.
- `gcp-project-bootstrap` — CLI auth, ADC, and PayGo preflight checks.
- `vertex-adk-builder` — Building ADK 2.0 agents on Agent Platform + official ADK skills setup.
- `graphrag-and-embeddings` — Multimodal embeddings (`gemini-embedding-2`) and GraphRAG architectures.
- `cloud-run-deploy` — One-command Cloud Run source and GPU deployments.
- `llm-wiki-ops` — Ingesting, re-indexing, and verifying the OKF v0.2 wiki.
- `brainstorming` — Collaborative Google Cloud architecture design.

### Wiring Up MCP Servers in Antigravity 2.0
To merge the pre-configured MCP servers from `.agents/mcp_config.json` (`adk-docs-mcp`, `cloud-run`, `gcloud`) into your local Antigravity configuration (`~/.gemini/config/mcp_config.json`), run:

```bash
./scripts/setup_antigravity_mcp.sh

# Or also install Google's official ADK coding skills via uvx:
./scripts/setup_antigravity_mcp.sh --with-adk-skills
```

---

## Related Concepts

- [Google Cloud CLI & Project Access Setup](gcp_cli_and_project_setup.md) — Setting up `gcloud`, ADC, and API enablement.
- [Agent Development Kit (ADK) & Official Skills](agent_development_kit_adk_and_skills.md) — Installing official ADK skills via `uvx google-agents-cli setup`.
- [Google Cloud MCP Servers Catalog](gcp_mcp_servers_catalog.md) — Local and Remote GCP MCP server reference.
- [Agent Platform Latest Models Catalog](agent_platform_models.md) — Canonical model IDs for every tier.
