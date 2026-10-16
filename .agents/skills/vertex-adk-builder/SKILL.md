---
name: vertex-adk-builder
description: >-
  Build, scaffold, stream, and deploy multi-agent PoCs using Google Agent
  Development Kit (ADK 2.0) and the unified `google-genai` SDK on Google Cloud
  Agent Platform (Vertex AI). Covers one-command PoC scaffolding (`agents-cli`,
  `agent-starter-pack`, `adk-samples`), ADK 2.0 Graph Workflows (`Workflow`,
  `RequestInput`, `require_confirmation`, `ResumabilityConfig`), custom React
  frontend streaming (`adk api_server` `/run_sse` & `AG-UI` / `CopilotKit`),
  `SkillToolset`, and strict latest-model selection (`gemini-4-argon`,
  `gemini-3.8-flash`).
---

# Vertex AI & ADK 2.0 Agent Builder Skill

Use this skill whenever scaffolding, writing, connecting a custom frontend to, or deploying agents with **Google Agent Development Kit (ADK 2.0)** or the **`google-genai` SDK**.

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

## 2. One-Command PoC Scaffolding & Official ADK Skills

- **Install Official ADK Coding Skills & `agents-cli` ([https://adk.dev/get-started/agents-cli/](https://adk.dev/get-started/agents-cli/)):**
  ```bash
  uvx google-agents-cli setup
  ```
- **Enhance & Deploy an ADK Project (`agents-cli`):**
  ```bash
  agents-cli scaffold enhance --deployment-target agent_runtime
  agents-cli deploy
  ```
- **Full-Stack PoC Templates (`agent-starter-pack` & `adk-samples`):**
  - `uvx agent-starter-pack create my-poc` (`adk`, `adk_a2a`, `agentic_rag`, `adk_live`)
  - Reference architectures: `https://github.com/google/adk-samples` and `https://github.com/google/adk-recipes`
  - Details: [`wiki/concepts/poc_scaffolding_agents_cli_and_templates.md`](../../../wiki/concepts/poc_scaffolding_agents_cli_and_templates.md)

## 3. ADK 2.0 Graph Workflows, Human-in-the-Loop (HITL) & Pause/Resume

- **Declarative Graph Routing (`Workflow` & `RequestInput`):**
  ```python
  from google.adk import Agent, Workflow
  from google.adk.events import RequestInput

  def ask_human_approval(data: str):
      yield RequestInput(message=f"Approve action for {data}? (yes/no)")

  root_agent = Workflow(
      name="approval_graph",
      edges=[("START", intake_agent, ask_human_approval, finalize_fn)],
  )
  ```
- **Tool-Level Confirmation (`require_confirmation=True`):**
  ```python
  from google.adk.tools import FunctionTool
  tools = [FunctionTool(sensitive_action, require_confirmation=True)]
  ```
- **Resumable Workflows (`ResumabilityConfig`):**
  ```python
  from google.adk.apps import App, ResumabilityConfig
  app = App(name="my_app", root_agent=root_agent, resumability_config=ResumabilityConfig(is_resumable=True))
  ```
  Details: [`wiki/concepts/adk_graph_workflows_and_hitl.md`](../../../wiki/concepts/adk_graph_workflows_and_hitl.md)

## 4. Custom Frontend UI & Real-Time Streaming (`adk api_server` & `AG-UI`)

- **Path A: Built-In REST + SSE Server (`adk api_server`):**
  ```bash
  adk api_server --allow_origins="*" --host 0.0.0.0 --port 8000 .
  ```
  Create a session via `POST /apps/{app}/users/{user}/sessions/{session}` and stream live events via `POST /run_sse`.
- **Path B: Rich React UI with `AG-UI` & `CopilotKit` (`ag-ui-adk`):**
  Expose your `App` at `/ag-ui` via `ADKAgent.from_app(adk_app)` and `add_adk_fastapi_endpoint(app, ag_ui_agent, path="/ag-ui")`.
  Details: [`wiki/concepts/agent_frontend_streaming_ag_ui.md`](../../../wiki/concepts/agent_frontend_streaming_ag_ui.md)

## 5. Runtime Skills Inside Your Own ADK Agents (`SkillToolset`)

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
    tools=[skill_toolset.SkillToolset(skills=[domain_skill])],
)
```

Read [`wiki/concepts/agent_development_kit_adk_and_skills.md`](../../../wiki/concepts/agent_development_kit_adk_and_skills.md) and [`wiki/concepts/google_genai_sdk_vertex.md`](../../../wiki/concepts/google_genai_sdk_vertex.md) for complete patterns.
