---
name: vertex-adk-builder
description: >-
  Build, test, and evaluate multi-agent systems using Google Agent Development
  Kit (ADK 2.0) and the unified `google-genai` SDK on Google Cloud Agent Platform
  (Vertex AI). Includes where to find and install official ADK coding skills
  (`uvx google-agents-cli setup`), runtime `SkillToolset`, and strict latest-model
  selection (`gemini-4-argon`, `gemini-3.8-flash`).
---

# Vertex AI & ADK 2.0 Agent Builder Skill

Use this skill whenever scaffolding, writing, testing, or debugging agents with **Google Agent Development Kit (ADK)** or the **`google-genai` SDK**.

## 1. Strict Agent Platform Rules (Zero AI Studio)

1. **Always Use Vertex AI Mode:**
   - Environment variables MUST be set:
     ```bash
     export GOOGLE_GENAI_USE_VERTEXAI=true
     export GOOGLE_CLOUD_PROJECT="your-hackathon-project-id"
     export GOOGLE_CLOUD_LOCATION="global"
     ```
   - Never use consumer `GEMINI_API_KEY` endpoints.
2. **Use Only the Single Latest Model Per Tier:**
   - Deep reasoning, complex coding, or video synthesis: `gemini-4-argon` (`location="global"`)
   - Default agent workhorse, tool routing, structured extraction: `gemini-3.8-flash` (`location="global"`)
   - High-volume classification / lightweight routing: `gemini-3.5-flash-lite` (`location="global"`)
   - Multimodal embeddings: `gemini-embedding-2`
   - Real-time bidirectional voice/video: `gemini-3.8-live`

## 2. Where to Find & Install Official ADK Skills

### A. Official ADK Skills for Your Coding Agent ([https://adk.dev/tutorials/coding-with-ai/](https://adk.dev/tutorials/coding-with-ai/))
- **Install via Google Agents CLI:**
  ```bash
  uvx google-agents-cli setup
  ```
  This installs Google's official ADK development skills (project scaffolding, evaluation & scoring, Agent Runtime / Cloud Run / GKE deployment, Gemini Enterprise publishing, OpenTelemetry tracing, and Python API quick reference) into Antigravity 2.0, Claude Code, or Cursor.
- **Official Machine-Readable ADK Docs (`llms.txt`):**
  - Index: `https://adk.dev/llms.txt` (pre-wired in `.agents/mcp_config.json` as `adk-docs-mcp`)
  - Full single-file docs: `https://adk.dev/llms-full.txt`
- **Community Skill Directories:**
  - `https://www.skills.sh/` (`npx skills`), `https://github.com/vudovn/ag-kit`.

### B. Runtime Skills Inside Your Own ADK Agents (`SkillToolset`)
ADK agents can dynamically load `SKILL.md` directories at runtime using progressive disclosure ([https://adk.dev/skills/](https://adk.dev/skills/)):

```python
import pathlib
from google.adk import Agent
from google.adk.skills import load_skill_from_dir
from google.adk.tools import skill_toolset

domain_skill = load_skill_from_dir(
    pathlib.Path(__file__).parent / "skills" / "my-domain-skill"
)

root_agent = Agent(
    model="gemini-3.8-flash",
    name="hackathon_specialist",
    description="Agent equipped with modular on-demand domain skills.",
    instruction="Use your specialized skills on demand to fulfill user requests.",
    tools=[
        skill_toolset.SkillToolset(skills=[domain_skill]),
    ],
)
```

## 3. Standard ADK Project Layout & Local Debugging

```text
my_agent_app/
├── .env                    # GOOGLE_GENAI_USE_VERTEXAI=true, GOOGLE_CLOUD_PROJECT=..., GOOGLE_CLOUD_LOCATION=global
├── requirements.txt        # google-adk>=1.25.0, google-genai
└── my_agent/
    ├── __init__.py         # from . import agent
    └── agent.py            # Defines root_agent = Agent(...)
```

Launch the interactive ADK Web UI locally:
```bash
GOOGLE_GENAI_USE_VERTEXAI=true \
GOOGLE_CLOUD_PROJECT="$GOOGLE_CLOUD_PROJECT" \
GOOGLE_CLOUD_LOCATION="global" \
adk web --allow_origins="*" --host 127.0.0.1 --port 8000 .
```
*(Always open via `http://localhost:8000` or `http://127.0.0.1:8000` in your browser).*

Read [`wiki/concepts/agent_development_kit_adk_and_skills.md`](../../../wiki/concepts/agent_development_kit_adk_and_skills.md) and [`wiki/concepts/google_genai_sdk_vertex.md`](../../../wiki/concepts/google_genai_sdk_vertex.md) for complete patterns.
