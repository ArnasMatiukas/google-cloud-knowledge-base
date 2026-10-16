# Google Cloud Knowledge Base — Agent System Contract

See [`GEMINI.md`](GEMINI.md) and [`wiki/index.md`](wiki/index.md) for the complete repository instructions, OKF v0.2 LLM Wiki index, and out-of-the-box `.agents/skills/` catalog.

- Always consult [`wiki/index.md`](wiki/index.md) or run `./scripts/okf_wiki_cli.py search "<topic>"` first.
- Use **Google Cloud Agent Platform (Vertex AI)** with Application Default Credentials (`GOOGLE_GENAI_USE_VERTEXAI=true`, `location="global"`). Never use consumer `GEMINI_API_KEY` workflows.
- Use only the single latest model per tier documented in [`wiki/concepts/agent_platform_models.md`](wiki/concepts/agent_platform_models.md) (`gemini-4-argon`, `gemini-3.8-flash`, `gemini-3.5-flash-lite`, `gemini-embedding-2`, `gemini-3.8-flash-tts`, `gemini-3.5-transcribe-live`, `gemini-3.8-live`, `gemini-nano-banana-2.1`, `gemini-omni-1.1-flash`, `lyria-3.5`, `gemma-4-31b-it`).
