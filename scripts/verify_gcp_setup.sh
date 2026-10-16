#!/usr/bin/env bash
# ==============================================================================
# Google Cloud Hackathon & Workshop Preflight Verification Script
# Verifies gcloud CLI, user login, target project, ADC, and enabled APIs.
# Usage:
#   ./scripts/verify_gcp_setup.sh
#   ./scripts/verify_gcp_setup.sh --enable-apis
# ==============================================================================

set -euo pipefail

ENABLE_APIS=false
if [[ "${1:-}" == "--enable-apis" ]]; then
  ENABLE_APIS=true
fi

REQUIRED_APIS=(
  "aiplatform.googleapis.com"
  "businessaicode.googleapis.com"
  "run.googleapis.com"
  "cloudbuild.googleapis.com"
  "artifactregistry.googleapis.com"
  "bigquery.googleapis.com"
  "sqladmin.googleapis.com"
  "alloydb.googleapis.com"
  "spanner.googleapis.com"
  "firestore.googleapis.com"
  "storage.googleapis.com"
  "discoveryengine.googleapis.com"
  "secretmanager.googleapis.com"
  "developerknowledge.googleapis.com"
)

echo "============================================================"
echo " Google Cloud Knowledge Base - Hackathon Environment Check"
echo "============================================================"

# 1. Check gcloud CLI
if ! command -v gcloud >/dev/null 2>&1; then
  echo "[FAIL] gcloud CLI is not installed or not in PATH."
  echo "       Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install"
  echo "       Or open Google Cloud Shell in your browser: https://shell.cloud.google.com"
  exit 1
fi
echo "[OK]   gcloud CLI found: $(gcloud --version | head -n 1)"

# 2. Check active authenticated account
ACTIVE_ACCOUNT="$(gcloud auth list --filter="status:ACTIVE" --format="value(account)" 2>/dev/null || true)"
if [[ -z "$ACTIVE_ACCOUNT" ]]; then
  echo "[FAIL] No active gcloud user session found."
  echo "       Run: gcloud auth login"
  exit 1
fi
echo "[OK]   Authenticated account: $ACTIVE_ACCOUNT"

# 3. Check configured GCP project
PROJECT_ID="${GOOGLE_CLOUD_PROJECT:-$(gcloud config get-value project 2>/dev/null || true)}"
if [[ -z "$PROJECT_ID" || "$PROJECT_ID" == "(unset)" ]]; then
  echo "[FAIL] No active Google Cloud project configured."
  echo "       List your pre-created projects: gcloud projects list"
  echo "       Then set your project:          gcloud config set project YOUR_PROJECT_ID"
  exit 1
fi
echo "[OK]   Active GCP Project: $PROJECT_ID"

# 4. Check Application Default Credentials (ADC)
ADC_FILE="${GOOGLE_APPLICATION_CREDENTIALS:-$HOME/.config/gcloud/application_default_credentials.json}"
if [[ ! -f "$ADC_FILE" ]]; then
  echo "[WARN] Application Default Credentials (ADC) file not found at $ADC_FILE."
  echo "       SDKs, ADK, and Antigravity CLI (agy) require ADC for Pay-As-You-Go billing."
  echo "       Run:"
  echo "         gcloud auth application-default login"
  echo "         gcloud auth application-default set-quota-project $PROJECT_ID"
else
  echo "[OK]   ADC credentials file found: $ADC_FILE"
fi

# 5. Check Vertex AI environment variables
if [[ "${GOOGLE_GENAI_USE_VERTEXAI:-}" != "true" && "${GOOGLE_GENAI_USE_VERTEXAI:-}" != "1" ]]; then
  echo "[INFO] Tip: Export Agent Platform env vars (or copy .env.example to .env):"
  echo "         export GOOGLE_GENAI_USE_VERTEXAI=true"
  echo "         export GOOGLE_CLOUD_PROJECT=$PROJECT_ID"
  echo "         export GOOGLE_CLOUD_LOCATION=global"
else
  echo "[OK]   GOOGLE_GENAI_USE_VERTEXAI is enabled (${GOOGLE_GENAI_USE_VERTEXAI})."
fi

# 6. Enable APIs if requested
if [[ "$ENABLE_APIS" == "true" ]]; then
  echo ""
  echo "[INFO] Enabling core hackathon APIs on project '$PROJECT_ID'..."
  gcloud services enable "${REQUIRED_APIS[@]}" --project="$PROJECT_ID"
  echo "[OK]   All core hackathon APIs enabled."
else
  echo ""
  echo "[INFO] To enable all core hackathon APIs in one command, run:"
  echo "         ./scripts/verify_gcp_setup.sh --enable-apis"
fi

echo "============================================================"
echo " Preflight check complete!"
echo "============================================================"
