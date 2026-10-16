---
type: Concept
title: "Agent Platform Latest Models Catalog (Single Model Per Tier)"
description: "Authoritative reference of the single latest, most capable Google Cloud Agent Platform (Vertex AI) model for every capability tier: Gemini 4 Argon, Gemini 3.8 Flash, Gemini 3.5 Flash-Lite, Gemini Embedding 2, TTS, Live API, Image, Video, Music, and Gemma 4."
category: "2. Models & SDKs"
tags: [models, gemini-4-argon, gemini-3-8-flash, gemini-embedding-2, gemini-3-8-live, nano-banana, omni, vertex-ai]
resource: "https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/google-models"
timestamp: "2026-10-16T10:25:00Z"
aliases: ["Vertex AI Models", "Gemini 4 Argon", "Gemini 3.8 Flash", "Latest Gemini Models"]
status: "active"
---

# Agent Platform Latest Models Catalog (Single Model Per Tier)

To eliminate ambiguity during hackathons and workshops, this knowledge base indexes **only the single latest, most capable model for each capability tier** on **Google Cloud Agent Platform (Vertex AI)**. Always select the canonical model ID listed below for your target capability tier.

**Official Documentation:** [Google Models on Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/google-models)

---

## 1. Master Model Selection Table (One Canonical Model Per Tier)

| Capability Tier | Canonical Model ID | Recommended Endpoint | Context Window (In / Out) | Primary Hackathon Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Frontier Reasoning, Coding & Video (Pro Tier)** | `gemini-4-argon` | `global` (also `us`, `eu`) | 1,048,576 / 1,048,576 | Deep multi-step reasoning, complex software engineering, computer use, and agentic video understanding (`thinking_level="HIGH"`). ([Docs](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/4-argon)) |
| **High-Throughput Agent Workhorse (Flash Tier)** | `gemini-3.8-flash` | `global` (also `us`, `eu`) | 1,048,576 / 65,536 | Default model for [ADK agents](agent_development_kit_adk_and_skills.md), tool calling, structured JSON / [GraphRAG](graphrag_architectures_on_gcp.md) extraction, and fast multimodal reasoning. ([Docs](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-8-flash)) |
| **Ultra-Fast / High-Volume (Flash-Lite Tier)** | `gemini-3.5-flash-lite` | `global` (also `us`, `eu`) | 1,048,576 / 65,536 | High-frequency classification, intent routing, bulk data tagging, and sub-second micro-tasks at the lowest token cost. ([Docs](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-5-flash-lite)) |
| **Multimodal Embeddings Tier** | `gemini-embedding-2` | `global`, `us-central1`, `europe-west1` | 8,192 input tokens | Unified embeddings across **Text, Images, Audio, Video, and PDFs** in one vector space (`256`–`3072` dimensions). ([Docs](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/embeddings)) |
| **Text-to-Speech (TTS) Tier** | `gemini-3.8-flash-tts` *(+ `gemini-3.8-flash-lite-tts`)* | `global` | 8,192 text in / Audio out | Expressive single- and multi-speaker speech synthesis in 130 languages, streaming output, style prompts, voice design, and voice replication. |
| **Speech-to-Text / Transcription (ASR) Tier** | `gemini-3.5-transcribe-live` *(streaming)* / `gemini-3.5-transcribe` *(batch)* | `global` | Audio in / Text out | Real-time bidirectional streaming speech-to-text with Voice Activity Detection (VAD) or synchronous file transcription. |
| **Real-Time Bidirectional Voice & Video (Live API)** | `gemini-3.8-live` *(+ `gemini-3.8-live-extended-thinking`)* | `global` | Streaming Audio & Video | Low-latency two-way conversational voice/video agents with barge-in, tool calling, and 1080p Live Avatar output. ([Docs](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-8-live)) |
| **Image Generation & Editing Tier** | `gemini-nano-banana-2.1` *(+ `gemini-3.1-flash-lite-image`)* | `global` | 131,072 in / 32,768 out (1K/2K/4K) | Photorealistic text-to-image, conversational multi-turn image editing, character consistency, and virtual try-on. |
| **Video & Audio Generation / Editing Tier** | `gemini-omni-1.1-flash` | `global` | Multimodal in / Video+Audio out | Unified Text-to-Video, Image-to-Video, Reference-to-Video, conversational video editing, video extension, and 48kHz audio up to 4K. |
| **Music & Song Generation Tier** | `lyria-3.5` | `global` | Text prompt in / Audio out | Full-song music generation (vocals, lyrics, and studio instrumentation up to 4 minutes). |
| **Open-Weight Models (Cloud Run GPUs)** | `gemma-4-31b-it` *(dense)* / `gemma-4-26b-a4b-it` *(MoE)* | [Cloud Run NVIDIA L4](cloud_run_serverless_and_gpus.md) | 128,000 | Self-hosted open-weight multimodal & function-calling models when custom container hosting on Cloud Run GPUs is required. |

---

## 2. Key Model Tuning & Endpoint Rules

### 1. Always Use `location="global"` for Frontier Models
On Google Cloud Agent Platform, configuring `location="global"` routes requests through Google's global dynamic workload pool—giving you the highest default Queries Per Minute (QPM) and Tokens Per Minute (TPM) and avoiding single-region `429 RESOURCE_EXHAUSTED` bottlenecks. (Use `us` or `eu` multi-region endpoints only if strict regional data residency is required).

### 2. Controlling Latency vs. Reasoning Depth (`thinking_level`)
Both `gemini-4-argon` and `gemini-3.8-flash` default to `thinking_level="HIGH"` (`default_budget = -1`), allowing the model to reason deeply before responding:
- **When you need maximum reasoning quality** (complex code generation, multi-hop analysis, YouTube/video synthesis, or customer email distillation): keep `thinking_level="HIGH"`.
- **When you need the lowest possible Time-To-First-Token (TTFT)** on `gemini-3.8-flash` (such as real-time UI routing, fast chat turns, or simple JSON extraction): explicitly set `thinking_level="LOW"` in `GenerateContentConfig`:

```python
from google import genai
from google.genai import types

client = genai.Client(vertexai=True, project="YOUR_PROJECT_ID", location="global")

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Classify this user request into BILLING, TECHNICAL, or GENERAL.",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="LOW"),
    ),
)
```

---

## Related Concepts

- [Google GenAI SDK on Vertex AI](google_genai_sdk_vertex.md) — Python SDK patterns for structured outputs, caching, and function calling.
- [Gemini Embedding 2 (Multimodal Embeddings)](gemini_embedding_2_multimodal.md) — Deep dive into unified text, image, audio, video, and PDF embeddings.
- [Multimodal Live API, Voice, Image & Video](multimodal_live_voice_and_media.md) — Implementation patterns for `gemini-3.8-live`, `gemini-3.8-flash-tts`, `gemini-nano-banana-2.1`, and `gemini-omni-1.1-flash`.
- [Agent Development Kit (ADK) & Official Skills](agent_development_kit_adk_and_skills.md) — Orchestrating multi-agent systems with `gemini-4-argon` and `gemini-3.8-flash`.
