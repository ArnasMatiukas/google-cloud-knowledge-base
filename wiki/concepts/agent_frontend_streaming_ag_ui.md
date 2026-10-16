---
type: Guide
title: "Custom Frontend UI & Real-Time Agent Streaming (adk api_server, SSE & AG-UI)"
description: "How to connect custom React, Next.js, or Vite web frontends to ADK 2.0 agents on Vertex AI using the built-in ADK REST/SSE API Server (adk api_server / /run_sse) or the AG-UI protocol and CopilotKit."
category: "3. Agentic Frameworks"
tags: [frontend, streaming, sse, ag-ui, copilotkit, api-server, react, adk]
resource: "https://adk.dev/runtime/api-server/"
timestamp: "2026-10-16T12:48:00Z"
aliases: ["ADK API Server", "AG-UI for ADK", "CopilotKit ADK", "Agent SSE Streaming"]
status: "active"
---

# Custom Frontend UI & Real-Time Agent Streaming (`adk api_server`, SSE & `AG-UI`)

While `adk web` is ideal for developer debugging, hackathon judges and enterprise buyers evaluate PoCs through a **custom, branded web interface** that streams agent reasoning, live tool execution cards, and [Human-in-the-Loop approvals](adk_graph_workflows_and_hitl.md) in real time.

ADK 2.0 provides **two official paths** to connect any React, Next.js, or Vite frontend to your backend agent:
1. **Path A: Zero-Dependency ADK API Server (`adk api_server` + `/run_sse`)** — Built directly into `google-adk`.
2. **Path B: Rich Generative UI & Shared State via `AG-UI` Protocol & `CopilotKit` (`ag-ui-adk`)** — Drop-in React components and bidirectional frontend tools.

**Official Documentation:** [ADK API Server](https://adk.dev/runtime/api-server/) · [AG-UI Integration for ADK](https://adk.dev/integrations/ag-ui/) · [CopilotKit for ADK](https://adk.dev/integrations/copilotkit/)

---

## 1. Path A: Built-In ADK REST & SSE Server (`adk api_server`)

Every [ADK 2.0](agent_development_kit_adk_and_skills.md) project can run as a production-ready FastAPI + Server-Sent Events (SSE) backend with zero extra Python code.

### Step 1: Launch `adk api_server` with Vertex AI ADC
```bash
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT="your-hackathon-project-id"
export GOOGLE_CLOUD_LOCATION="global"

# Start the REST + SSE server on port 8000 with CORS enabled for your frontend:
adk api_server --allow_origins="*" --host 0.0.0.0 --port 8000 .
```
*(Interactive OpenAPI / Swagger docs are automatically served at `http://localhost:8000/docs`).*

### Step 2: Create a Session & Stream Events (`/run_sse`) from Your Frontend
```typescript
const API_BASE = "http://localhost:8000";
const APP_NAME = "my_agent"; // Folder name containing agent.py
const USER_ID = "demo_user";
const SESSION_ID = "session_001";

// 1. Initialize or fetch the session
await fetch(`${API_BASE}/apps/${APP_NAME}/users/${USER_ID}/sessions/${SESSION_ID}`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ state: { tier: "enterprise" } }),
});

// 2. Stream real-time agent events (thoughts, tool calls, node outputs, text) via SSE
const response = await fetch(`${API_BASE}/run_sse`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Accept": "text/event-stream",
  },
  body: JSON.stringify({
    app_name: APP_NAME,
    user_id: USER_ID,
    session_id: SESSION_ID,
    new_message: {
      role: "user",
      parts: [{ text: "Analyze our Q3 Cloud Run latency and suggest fixes." }],
    },
    streaming: true,
  }),
});

const reader = response.body!.getReader();
const decoder = new TextDecoder();
while (true) {
  const { value, done } = await reader.read();
  if (done) break;
  const chunk = decoder.decode(value, { stream: true });
  for (const line of chunk.split("\n")) {
    if (line.startsWith("data: ")) {
      const event = JSON.parse(line.slice(6));
      // Render tool calls, graph node_info, or text parts in your UI
      console.log("ADK Event:", event);
    }
  }
}
```

---

## 2. Path B: Interactive Web UIs with `AG-UI` Protocol & `CopilotKit`

**Official Guides:** [AG-UI for ADK](https://adk.dev/integrations/ag-ui/) · [CopilotKit for ADK](https://adk.dev/integrations/copilotkit/)

The open **AG-UI protocol** (`ag-ui-adk`) connects ADK agents to rich React frontends, allowing the agent to render custom UI components for tool calls (`useRenderToolCall`), synchronize application state, and invoke browser-side frontend tools.

### Step 1: Install Backend & Frontend Packages
```bash
# Backend (Python)
pip install google-adk ag-ui-adk fastapi "uvicorn[standard]"

# Frontend (React / Next.js)
npm install @copilotkit/react-core @copilotkit/react-ui @copilotkit/runtime @ag-ui/client
```

### Step 2: Expose Your Vertex AI ADK Agent Over `/ag-ui` (`agent_server.py`)
Always authenticate via Google Cloud Agent Platform (`GOOGLE_GENAI_USE_VERTEXAI=true`, `location="global"`) and use [`gemini-3.8-flash`](agent_platform_models.md) or [`gemini-4-argon`](agent_platform_models.md):

```python
import os
from fastapi import FastAPI
from google.adk.agents import Agent
from google.adk.apps import App, ResumabilityConfig
from ag_ui_adk import ADKAgent, AGUIToolset, add_adk_fastapi_endpoint

os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "true")
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")

root_agent = Agent(
    model="gemini-3.8-flash",
    name="poc_copilot_agent",
    instruction="You are a Google Cloud assistant. Use backend and frontend tools to assist the user.",
    tools=[AGUIToolset()],
)

adk_app = App(
    name="poc_copilot_app",
    root_agent=root_agent,
    resumability_config=ResumabilityConfig(is_resumable=True),
)

ag_ui_agent = ADKAgent.from_app(
    adk_app,
    user_id="hackathon_user",
    use_in_memory_services=True,
)

app = FastAPI()
add_adk_fastapi_endpoint(app, ag_ui_agent, path="/ag-ui")
```

Run the backend server:
```bash
GOOGLE_GENAI_USE_VERTEXAI=true \
GOOGLE_CLOUD_PROJECT="$GOOGLE_CLOUD_PROJECT" \
GOOGLE_CLOUD_LOCATION="global" \
uvicorn agent_server:app --host 0.0.0.0 --port 8000
```

### Step 3: Render Live Tool Calls as Custom React Components
In your React frontend, use `useRenderToolCall` so tool executions appear as interactive status cards or charts directly in the stream:

```tsx
import { useRenderToolCall } from "@copilotkit/react-core";

export function AgentToolRenderer() {
  useRenderToolCall({
    name: "query_spanner_graph",
    description: "Executes a multi-hop Spanner Graph query.",
    parameters: [{ name: "entity", type: "string", required: true }],
    render: ({ status, args, result }) => (
      <div className="border p-4">
        <div className="font-mono text-xs">
          {status === "executing" ? `Querying Spanner Graph for ${args.entity}...` : "Graph Query Complete"}
        </div>
        {result && <pre className="text-xs mt-2">{JSON.stringify(result, null, 2)}</pre>}
      </div>
    ),
  });
  return null;
}
```

---

## Related Concepts

- [ADK 2.0 Graph Workflows, Human-in-the-Loop & Pause/Resume](adk_graph_workflows_and_hitl.md) — Combining `/run_sse` and `AG-UI` with `ResumabilityConfig` and human approvals.
- [One-Command PoC Scaffolding: Agents CLI & Templates](poc_scaffolding_agents_cli_and_templates.md) — Scaffolding full-stack agent + UI templates.
- [Google Cloud Run: Serverless Containers & GPUs](cloud_run_serverless_and_gpus.md) — Deploying your FastAPI + React PoC to Cloud Run.
