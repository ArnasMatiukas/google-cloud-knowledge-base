---
name: gcp-project-bootstrap
description: >-
  Configure and verify Google Cloud CLI access, Application Default Credentials
  (ADC), project quota binding, API enablement, and Antigravity 2.0 Pay-As-You-Go
  (PayGo) setup for hackathon and workshop accounts. Use when starting a new
  project or troubleshooting authentication/billing errors.
---

# Google Cloud Project & Antigravity 2.0 PayGo Bootstrap Skill

Hackathon and workshop attendees are provided with a **Google Cloud user account** and a **pre-created fresh GCP project**. Use this skill to get their CLI, SDKs, and Antigravity 2.0 environment authenticated and ready in under 5 minutes.

## 1. Automated Preflight & API Enablement

Run the repository's preflight check script to verify `gcloud`, active account, project ID, ADC, and enabled APIs:

```bash
# Check status:
./scripts/verify_gcp_setup.sh

# Enable all core hackathon APIs in one command:
./scripts/verify_gcp_setup.sh --enable-apis
```

## 2. Step-by-Step Manual CLI & ADC Setup

If `verify_gcp_setup.sh` reports missing authentication or ADC credentials, guide the user through:

```bash
# 1. Sign in with your provided Google Cloud hackathon credentials
gcloud auth login

# 2. List pre-created projects and bind your target project ID
gcloud projects list
export GOOGLE_CLOUD_PROJECT="your-hackathon-project-id"
gcloud config set project "$GOOGLE_CLOUD_PROJECT"

# 3. Configure Application Default Credentials (ADC) and Quota Project
gcloud auth application-default login
gcloud auth application-default set-quota-project "$GOOGLE_CLOUD_PROJECT"

# 4. Export Agent Platform (Vertex AI) environment variables
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_LOCATION="global"
```

## 3. Antigravity 2.0 Pay-As-You-Go (PayGo) Setup

When attendees use **Antigravity 2.0** ([https://antigravity.google/download](https://antigravity.google/download)), enforce these rules:

1. **Use Supported Enterprise/PayGo Surfaces Only:**
   - Use **Antigravity 2.0 Desktop App (Hub)**, **Antigravity CLI (`agy`)**, or the **Antigravity IDE Extension** (VS Code, JetBrains, Zed).
   - **Never** use the standalone consumer "Antigravity IDE" fork, which cannot connect to a GCP project.
2. **Click "Login with Business" (Never "Continue with Google"):**
   - On the Antigravity 2.0 sign-in screen, clicking *"Continue with Google"* traps the user in consumer free-tier rate limits that exhaust in ~20 minutes.
   - Always click **"Login with Business" / "Use business account"** (or **"Prefer to use a GCP project?"**), sign in with the hackathon Google Cloud account, and enter `$GOOGLE_CLOUD_PROJECT` (location: `global`).
3. **Antigravity CLI (`agy`) PayGo Mode:**
   - Once `gcloud auth application-default login` and `gcloud config set project "$GOOGLE_CLOUD_PROJECT"` are set, `agy` automatically inherits ADC and bills Pay-As-You-Go token usage to `aiplatform.googleapis.com` on the project.
4. **AI Developer Tools Overages Toggle:**
   - In Cloud Console (`https://console.cloud.google.com/gemini-enterprise/settings/ai-developer-tools?project=$GOOGLE_CLOUD_PROJECT`), ensure **AI Developer Tools** is **On**, **Overages / Pay-As-You-Go** is enabled, and **Gemini 4 Argon** is toggled **On**.

For full troubleshooting of `403 PERMISSION_DENIED`, `CONSUMER_INVALID`, or `429 RESOURCE_EXHAUSTED`, read [`wiki/concepts/gcp_cli_and_project_setup.md`](../../../wiki/concepts/gcp_cli_and_project_setup.md) and [`wiki/concepts/antigravity_2_paygo_and_ide_setup.md`](../../../wiki/concepts/antigravity_2_paygo_and_ide_setup.md).
