---
type: Guide
title: "Google GenAI SDK on Vertex AI"
description: "How to use the unified google-genai SDK in Google Cloud Agent Platform (Vertex AI) mode for text generation, Pydantic structured outputs, function calling, GCS multimodal inputs, and context caching."
category: "2. Models & SDKs"
tags: [google-genai, python, sdk, vertex-ai, structured-outputs, function-calling, caching]
resource: "https://github.com/googleapis/python-genai"
timestamp: "2026-10-16T10:25:00Z"
aliases: ["google-genai", "GenAI SDK", "vertexai=True"]
status: "active"
---

# Google GenAI SDK on Vertex AI

The **`google-genai`** SDK ([https://github.com/googleapis/python-genai](https://github.com/googleapis/python-genai)) is Google's unified SDK for calling all [Agent Platform models](agent_platform_models.md). Do **not** use the deprecated `google-cloud-aiplatform` (`vertexai.generative_models`) package for new projects.

---

## 1. Installation & Vertex AI Initialization

Install the SDK:

```bash
pip install -U google-genai pydantic
```

Configure environment variables (see [Google Cloud CLI & Project Access Setup](gcp_cli_and_project_setup.md)) so the client authenticates automatically via Application Default Credentials (ADC):

```bash
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT="your-hackathon-project-id"
export GOOGLE_CLOUD_LOCATION="global"
```

Initialize the client in Python:

```python
from google import genai
from google.genai import types

# Automatically reads GOOGLE_GENAI_USE_VERTEXAI, GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION
# or pass them explicitly:
client = genai.Client(
    vertexai=True,
    project="your-hackathon-project-id",
    location="global",
)
```

---

## 2. Core SDK Patterns for Hackathons

### A. Text & Reasoning Generation (`gemini-4-argon` / `gemini-3.8-flash`)

```python
response = client.models.generate_content(
    model="gemini-4-argon",
    contents="Design a resilient event-driven microservice architecture on Cloud Run and Pub/Sub.",
    config=types.GenerateContentConfig(
        system_instruction="You are a Principal Google Cloud Architect. Be concise and technical.",
        thinking_config=types.ThinkingConfig(thinking_level="HIGH"),
        temperature=0.2,
    ),
)
print(response.text)
```

### B. Guaranteed Structured Outputs with Pydantic (`response_schema`)

Use `response_mime_type="application/json"` with a Pydantic model to guarantee schema-valid JSON responses (ideal for API backends and [GraphRAG entity extraction](graphrag_architectures_on_gcp.md)):

```python
from pydantic import BaseModel, Field

class BugReportAnalysis(BaseModel):
    severity: str = Field(description="One of: CRITICAL, HIGH, MEDIUM, LOW")
    affected_service: str
    root_cause_hypothesis: str
    remediation_steps: list[str]

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Checkout service is returning HTTP 503 after the v2.4 deployment due to DB pool exhaustion.",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=BugReportAnalysis,
        thinking_config=types.ThinkingConfig(thinking_level="LOW"),
    ),
)

analysis: BugReportAnalysis = response.parsed
print(analysis.severity, analysis.remediation_steps)
```

### C. Multimodal Inputs Directly from Cloud Storage (`gs://`)

With Vertex AI mode, you do not need to download or re-upload files via a Files API—pass any [Cloud Storage (GCS)](datastores_cloudsql_alloydb_spanner_firestore_gcs.md) `gs://` URI directly:

```python
response = client.models.generate_content(
    model="gemini-4-argon",
    contents=[
        types.Part.from_uri(
            file_uri="gs://my-hackathon-bucket/demo_recording.mp4",
            mime_type="video/mp4",
        ),
        "Summarize the technical architecture shown in this video and list any bottlenecks.",
    ],
)
print(response.text)
```

### D. Native Function Calling (Tools)

Pass standard Python functions with type annotations and docstrings directly in `config.tools`:

```python
def get_cloud_run_status(service_name: str, region: str) -> dict:
    """Checks the health and latest revision of a Cloud Run service."""
    return {"service": service_name, "region": region, "status": "HEALTHY", "revision": "rev-004"}

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Is the payment-api service healthy in europe-west1?",
    config=types.GenerateContentConfig(
        tools=[get_cloud_run_status],
    ),
)
print(response.text)
```

### E. Async Streaming (`client.aio`) for FastAPI & Web UIs

For low-latency web endpoints on [Cloud Run](cloud_run_serverless_and_gpus.md), always use the async client (`client.aio`):

```python
async def stream_response(prompt: str):
    async for chunk in await client.aio.models.generate_content_stream(
        model="gemini-3.8-flash",
        contents=prompt,
    ):
        print(chunk.text, end="", flush=True)
```

---

## Related Concepts

- [Agent Platform Latest Models Catalog](agent_platform_models.md) — Model IDs and context window limits across all tiers.
- [Gemini Embedding 2 (Multimodal Embeddings)](gemini_embedding_2_multimodal.md) — Calling `client.models.embed_content` with `gemini-embedding-2`.
- [Agent Development Kit (ADK) & Official Skills](agent_development_kit_adk_and_skills.md) — Multi-agent orchestration built on `google-genai`.
- [RAG, Grounding & Search on Google Cloud](rag_grounding_and_search.md) — Enabling Google Search and Maps grounding in `GenerateContentConfig`.
