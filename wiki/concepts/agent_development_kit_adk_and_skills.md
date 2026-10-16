---
type: Guide
title: "Agent Development Kit (ADK 2.0) & Official ADK Skills"
description: "Complete guide to Google's Agent Development Kit (ADK 2.0) on Vertex AI: LlmAgent, workflow orchestrators, where to find and install official ADK coding skills (google-agents-cli, adk.dev/llms.txt), and runtime SkillToolset."
category: "3. Agentic Frameworks"
tags: [adk, agents, skills, skill-toolset, google-agents-cli, llms-txt, multi-agent]
resource: "https://adk.dev/"
timestamp: "2026-10-16T10:25:00Z"
aliases: ["Google ADK", "ADK 2.0", "ADK Skills", "SkillToolset", "google-agents-cli"]
status: "active"
---

# Agent Development Kit (ADK 2.0) & Official ADK Skills

The **Google Agent Development Kit (ADK)** ([https://adk.dev/](https://adk.dev/)) is Google's open-source framework (available in Python, TypeScript, Go, Java, and Kotlin) for building, evaluating, and deploying production multi-agent systems on **Google Cloud Agent Platform (Vertex AI)**.

- **Official Documentation:** [https://adk.dev/](https://adk.dev/)
- **GitHub Repositories:** [ADK Python](https://github.com/google/adk-python) · [ADK TypeScript](https://github.com/google/adk-js) · [ADK Go](https://github.com/google/adk-go) · [ADK Java](https://github.com/google/adk-java) · [ADK Recipes & Samples](https://github.com/google/adk-recipes)

---

## 1. Where to Find & Install Official ADK Skills

There are **two distinct layers of ADK Skills** that every hackathon team should know:

### Layer A: Official ADK Skills for Your AI Coding Assistant (`Code with AI`)
**Official Guide:** [https://adk.dev/tutorials/coding-with-ai/](https://adk.dev/tutorials/coding-with-ai/)

To give your coding agent ([Antigravity 2.0](antigravity_2_paygo_and_ide_setup.md), Claude Code, or Cursor) deep expertise in ADK 2.0 so it never hallucinates outdated APIs:

1. **Google Agents CLI (`google-agents-cli`):**
   - **Official Docs:** [https://google.github.io/agents-cli/](https://google.github.io/agents-cli/)
   - Run one command in your project directory to install Google's official ADK development skills into your workspace:
     ```bash
     uvx google-agents-cli setup
     ```
   - **What It Installs:**
     - ADK development lifecycle and coding guidelines
     - Project scaffolding and `root_agent` package conventions
     - Evaluation methodology and scoring (`adk eval`)
     - [Vertex AI Agent Engine](vertex_ai_agent_engine.md), [Cloud Run](cloud_run_serverless_and_gpus.md), and GKE deployment
     - Gemini Enterprise agent publishing
     - OpenTelemetry trace, logging, and integrations
     - Python API quick reference and documentation index
2. **Official ADK Docs MCP Server (`adk-docs-mcp`):**
   - Pre-configured in this repository's `.agents/mcp_config.json` (run `./scripts/setup_antigravity_mcp.sh` to merge into `~/.gemini/config/mcp_config.json`):
     ```json
     {
       "mcpServers": {
         "adk-docs-mcp": {
           "command": "uvx",
           "args": [
             "--from", "mcpdoc",
             "--with", "mcp<2",
             "mcpdoc",
             "--urls", "AgentDevelopmentKit:https://adk.dev/llms.txt",
             "--transport", "stdio"
           ]
         }
       }
     }
     ```
3. **Machine-Readable ADK Documentation Indexes (`llms.txt`):**
   - **Compact Index with Links:** [https://adk.dev/llms.txt](https://adk.dev/llms.txt)
   - **Full Single-File Reference:** [https://adk.dev/llms-full.txt](https://adk.dev/llms-full.txt)
4. **Community & Ecosystem Skill Directories:**
   - [Skills.sh Gallery](https://www.skills.sh/) (`npx skills`)
   - [Antigravity Kit (AG-Kit)](https://github.com/vudovn/ag-kit)

---

### Layer B: Runtime Skills Inside the ADK Agents You Build (`SkillToolset`)
**Official Guide:** [https://adk.dev/skills/](https://adk.dev/skills/) · **Spec:** [https://agentskills.io/specification](https://agentskills.io/specification)

Instead of stuffing every rule and reference table into a monolithic system prompt, the ADK agents you build can load modular `SKILL.md` folders dynamically at runtime using **`SkillToolset`** and **Progressive Disclosure** (Level 1 metadata $\rightarrow$ Level 2 `SKILL.md` body $\rightarrow$ Level 3 resources):

```python
import pathlib
from google.adk import Agent
from google.adk.skills import load_skill_from_dir
from google.adk.tools import skill_toolset

# Load any standard SKILL.md directory (including skills from .agents/skills/!)
graphrag_skill = load_skill_from_dir(
    pathlib.Path(__file__).parent / "skills" / "graphrag-and-embeddings"
)

def query_knowledge_graph(entity_name: str) -> dict:
    """Queries the project's GraphRAG store for entity relationships."""
    return {"entity": entity_name, "neighbors": ["Cloud Run", "Spanner Graph"]}

my_skill_toolset = skill_toolset.SkillToolset(
    skills=[graphrag_skill],
    additional_tools=[query_knowledge_graph],
)

root_agent = Agent(
    model="gemini-3.8-flash",
    name="architecture_assistant",
    description="An ADK agent that loads specialized domain skills on demand.",
    instruction="You are a Google Cloud assistant. Use your skills on demand to solve user tasks.",
    tools=[my_skill_toolset],
)
```
- **Official Code Sample:** [ADK Python `skills_agent`](https://github.com/google/adk-python/tree/main/contributing/samples/environment_and_skills/skills_agent)

---

## 2. Core ADK Multi-Agent Patterns (Vertex AI Native)

### Standard Project Structure
```text
my_hackathon_project/
├── .env                        # GOOGLE_GENAI_USE_VERTEXAI=true, GOOGLE_CLOUD_PROJECT=..., GOOGLE_CLOUD_LOCATION=global
├── requirements.txt            # google-adk>=1.25.0, google-genai
└── concierge_agent/
    ├── __init__.py             # Must contain: from . import agent
    └── agent.py                # Must expose: root_agent = ...
```

### Combining `LlmAgent` with Deterministic Workflow Agents
Use [`gemini-3.8-flash`](agent_platform_models.md) for fast specialist routing/extraction and [`gemini-4-argon`](agent_platform_models.md) for deep synthesis, wired together with `SequentialAgent`, `ParallelAgent`, or `LoopAgent`:

```python
from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent

researcher = LlmAgent(
    name="researcher",
    model="gemini-3.8-flash",
    instruction="Extract key technical requirements from the user request.",
    output_key="requirements_summary",
)

security_reviewer = LlmAgent(
    name="security_reviewer",
    model="gemini-3.8-flash",
    instruction="Identify IAM and VPC guardrails for: {requirements_summary}",
    output_key="security_notes",
)

architect_synthesizer = LlmAgent(
    name="architect_synthesizer",
    model="gemini-4-argon",
    instruction="Synthesize a final GCP blueprint using {requirements_summary} and {security_notes}.",
)

root_agent = SequentialAgent(
    name="blueprint_pipeline",
    sub_agents=[researcher, security_reviewer, architect_synthesizer],
)
```

---

## 3. Running `adk web` Locally (With SSH / Remote VM Tunnel Gotchas)

Launch the interactive ADK Dev UI (includes live event traces, state inspection, and tool-call visualization):

```bash
GOOGLE_GENAI_USE_VERTEXAI=true \
GOOGLE_CLOUD_PROJECT="$GOOGLE_CLOUD_PROJECT" \
GOOGLE_CLOUD_LOCATION="global" \
adk web --allow_origins="*" --host 127.0.0.1 --port 8000 .
```

> [!TIP]
> **`adk web` Localhost & Port-Forwarding Gotchas:**
> 1. **Always open `http://localhost:8000/` or `http://127.0.0.1:8000/`** in your browser. ADK's DNS-rebinding protection blocks requests whose `Host` header is a remote machine hostname (`403 Forbidden: host not allowed`).
> 2. If forwarding over SSH (`ssh -L 8000:localhost:8000`), always pass `--allow_origins="*"` so cross-origin requests succeed.
> 3. If you restart `adk web` and see `404 Session not found`, remove `?session=...` from the browser URL or click **+ New Session**.

---

## Related Concepts

- [Vertex AI Agent Engine (Managed Runtime)](vertex_ai_agent_engine.md) — Deploying ADK agents to managed `ReasoningEngine` with Sessions and Memory Bank.
- [Cloud Run Serverless & GPUs](cloud_run_serverless_and_gpus.md) — Deploying ADK agents to Cloud Run via `adk deploy cloud_run`.
- [Agentic Protocols: MCP & A2A](protocols_mcp_and_a2a.md) — Connecting ADK agents to MCP servers (`McpToolset`) and remote A2A agents (`RemoteA2aAgent`).
- [Agent Platform Latest Models Catalog](agent_platform_models.md) — Canonical model IDs for ADK agents.
