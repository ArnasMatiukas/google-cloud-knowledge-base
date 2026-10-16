---
name: cloud-run-deploy
description: >-
  Deploy containerized web apps, FastAPI backends, ADK agents, and remote MCP
  servers to Google Cloud Run (`gcloud run deploy`) with Vertex AI ADC IAM
  bindings and GPU support. Use whenever deploying or updating Cloud Run
  services.
---

# Google Cloud Run Deployment Skill

Use this skill to deploy hackathon applications, ADK 2.0 agents, or remote MCP servers to **Google Cloud Run** ([https://docs.cloud.google.com/run/docs](https://docs.cloud.google.com/run/docs)).

## 1. One-Command Source Deployment (Web Apps, APIs & ADK Agents)

Cloud Run can build and deploy directly from source (`Dockerfile` or Buildpacks) without requiring a local Docker daemon:

```bash
export GOOGLE_CLOUD_PROJECT="$(gcloud config get-value project)"
export REGION="europe-west1" # or us-central1

gcloud run deploy my-hackathon-service \
  --source . \
  --project "$GOOGLE_CLOUD_PROJECT" \
  --region "$REGION" \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT},GOOGLE_CLOUD_LOCATION=global,GOOGLE_GENAI_USE_VERTEXAI=true"
```

## 2. Granting the Cloud Run Service Account Access to Agent Platform

Ensure the Cloud Run runtime service account has permission to invoke Vertex AI / Agent Platform models (`roles/aiplatform.user`):

```bash
PROJECT_NUMBER="$(gcloud projects describe "$GOOGLE_CLOUD_PROJECT" --format='value(projectNumber)')"
RUNTIME_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
  --member="serviceAccount:${RUNTIME_SA}" \
  --role="roles/aiplatform.user"
```

## 3. Deploying ADK Agents Directly via ADK CLI

If deploying an ADK agent directory:
```bash
adk deploy cloud_run \
  --project="$GOOGLE_CLOUD_PROJECT" \
  --region="$REGION" \
  --service_name="my-adk-agent" \
  --with_ui \
  ./my_agent
```

## 4. Deploying Open-Weight Models (`gemma-4-31b-it`) on Cloud Run GPUs

When self-hosting open-weight models on Cloud Run with NVIDIA L4 GPUs:
```bash
gcloud run deploy gemma-4-service \
  --image="us-docker.pkg.dev/cloudrun/container/gemma/gemma4-31b" \
  --project="$GOOGLE_CLOUD_PROJECT" \
  --region="us-central1" \
  --gpu=1 \
  --gpu-type="nvidia-l4" \
  --cpu=8 \
  --memory=32Gi \
  --no-cpu-throttling
```

See [`wiki/concepts/cloud_run_serverless_and_gpus.md`](../../../wiki/concepts/cloud_run_serverless_and_gpus.md) for service-to-service OIDC authentication, Secret Manager injection, and Cloud Run Jobs.
