---
type: Guide
title: "Multimodal Live API, Voice (TTS/ASR), Image & Video Generation"
description: "How to build real-time voice, video, image, and music experiences on Google Cloud Agent Platform using only the latest models per tier: gemini-3.8-live, gemini-3.8-flash-tts, gemini-3.5-transcribe-live, gemini-nano-banana-2.1, gemini-omni-1.1-flash, and lyria-3.5."
category: "7. Multimodal & Live"
tags: [live-api, gemini-3-8-live, tts, asr, nano-banana, omni, lyria, multimodal, voice]
resource: "https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-8-live"
timestamp: "2026-10-16T10:25:00Z"
aliases: ["Gemini Live API", "Gemini 3.8 Live", "Nano Banana 2.1", "Gemini Omni 1.1 Flash", "Gemini TTS"]
status: "active"
---

# Multimodal Live API, Voice (TTS/ASR), Image & Video Generation

Hackathon demos stand out when they combine real-time voice, vision, and generative media. Always use the **single latest model per tier** on the `global` endpoint.

---

## 1. Real-Time Bidirectional Voice & Video Agents (`gemini-3.8-live`)

- **Canonical Model ID:** `gemini-3.8-live` (or `gemini-3.8-live-extended-thinking` for Thinker-Talker reasoning)
- **Official Docs:** [Gemini 3.8 Live on Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-8-live)
- **Key Capabilities:** Native audio-to-audio (16 kHz PCM in, 24 kHz PCM out) + live video streaming, natural barge-in / interruption handling, affective prosody, live tool calling, and 1080p Live Avatar output.

```python
from google import genai
from google.genai import types

client = genai.Client(vertexai=True, project="your-hackathon-project-id", location="global")

config = types.LiveConnectConfig(
    response_modalities=["AUDIO"],
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Puck")
        )
    ),
    # CRITICAL GOTCHA: Always enable contextWindowCompression so multi-turn live sessions
    # do not compound input audio token billing on every turn and can run past 15 minutes!
    context_window_compression=types.ContextWindowCompressionConfig(
        trigger_tokens=16000,
        sliding_window=types.SlidingWindow(target_tokens=8000),
    ),
)

async def run_live_session():
    async with client.aio.live.connect(model="gemini-3.8-live", config=config) as session:
        await session.send_client_content(
            turns=types.Content(role="user", parts=[types.Part.from_text(text="Hello! Give me a 10-second pitch.")]),
            turn_complete=True,
        )
        async for response in session.receive():
            if response.data:
                # Stream 24kHz PCM audio bytes to speaker / WebSocket client
                pass
```

> [!IMPORTANT]
> **`gemini-3.8-live` Context Window Compression Gotcha:** Bidirectional Live API sessions re-send cumulative session history on each turn and do not use implicit context caching. Always configure `context_window_compression` (`SlidingWindow`) to cap per-turn token consumption and lift the 15-minute session duration cap.

---

## 2. Expressive Text-to-Speech (`gemini-3.8-flash-tts`) & Streaming ASR (`gemini-3.5-transcribe-live`)

### A. Text-to-Speech (TTS) Tier
- **Canonical Model ID:** `gemini-3.8-flash-tts` (or `gemini-3.8-flash-lite-tts` for lowest latency)
- **Capabilities:** 130 languages, single- and multi-speaker dialogue synthesis, natural-language style steering (e.g., *"Speak in a calm, upbeat podcast host tone"*), voice design, and voice replication on `location="global"`.

### B. Speech-to-Text / Transcription (ASR) Tier
- **Canonical Model IDs:**
  - `gemini-3.5-transcribe-live` — Real-time bidirectional streaming speech-to-text with built-in Voice Activity Detection (`ACTIVITY_START` / `ACTIVITY_END`). *(Tip: Gate silence locally or use VAD events so you do not stream long stretches of dead air).*
  - `gemini-3.5-transcribe` — Synchronous batch/unary audio transcription.

---

## 3. Image Generation & Conversational Editing (`gemini-nano-banana-2.1`)

- **Canonical Model ID:** `gemini-nano-banana-2.1` (and `gemini-3.1-flash-lite-image` for ultra-fast 1K generation)
- **Capabilities:** Native 1K, 2K, and 4K image generation, conversational multi-turn editing, mask-free inpainting, character consistency across multiple reference images, and accurate in-image text rendering on `location="global"`:

```python
response = client.models.generate_content(
    model="gemini-nano-banana-2.1",
    contents="Create a clean isometric architectural diagram of a serverless Cloud Run + Spanner Graph application on a dark charcoal background.",
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
    ),
)
for part in response.candidates[0].content.parts:
    if part.inline_data:
        with open("generated_diagram.png", "wb") as f:
            f.write(part.inline_data.data)
```

---

## 4. Unified Video & Audio Generation (`gemini-omni-1.1-flash`) & Music (`lyria-3.5`)

- **Video Generation & Editing (`gemini-omni-1.1-flash`):**
  - Replaces retiring Veo 3.1 preview endpoints with a unified model supporting **Text-to-Video (T2V)**, **Image-to-Video (I2V)**, **Reference-to-Video (R2V)**, **conversational video editing**, **video extension**, and **synchronized 48 kHz stereo audio** up to **4K resolution** (`16:9` and `9:16`) on `location="global"`.
- **Full-Song Music Generation (`lyria-3.5`):**
  - Generates studio-quality full songs with vocals, lyrics, and instrumentation up to 4 minutes from a text prompt.

---

## Related Concepts

- [Agent Platform Latest Models Catalog](agent_platform_models.md) — Complete single-model-per-tier summary table.
- [Google GenAI SDK on Vertex AI](google_genai_sdk_vertex.md) — Calling Agent Platform models with ADC.
- [Cloud Run Serverless & GPUs](cloud_run_serverless_and_gpus.md) — Hosting WebSocket relays for `gemini-3.8-live`.
