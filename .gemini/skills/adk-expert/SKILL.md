---
name: adk-expert
description: You MUST use this when working with ADK (Agent Development Kit) to fetch up-to-date documentation, API referrence for any ADK related task or referrence.
---

# Instructions
The user needs accurate, up-to-date information about the Google ADK (Agent Development Kit). The documentation is split between **Concepts/Guides** (how-to) and **API Reference** (classes/methods).

1.  **Identify the User's Goal:**
    *   **Understanding/Architecture:** If the user asks "How do I...", "What is...", or needs examples/patterns, look in the **Guides & Concepts** section.
    *   **Implementation/Coding:** If the user asks for specific class methods, arguments, or signatures (e.g., "arguments for `BaseAgent`"), look in the **API Reference** section.

2.  **Fetch Documentation:**
    *   **For Guides:** Find the most relevant link in the **Guides & Concepts** map below and use `web_fetch`.
    *   **For API Reference:** Fetch the consolidated API page: `https://google.github.io/adk-docs/api-reference/python/google-adk.html` and search for the specific class/module within the fetched text.

3.  **Synthesize & Implement:**
    *   Read the fetched documentation carefully.
    *   For implementation, pay close attention to **required arguments**, **return types**, and **method names** from the API reference.
    *   Use this grounded information to write code. Do not hallucinate API methods.

4.  **Citation:** Mention which documentation page you referenced.

# Available resources
**Guides & Concepts:**

*   **Getting Started & Overview**
    *   Main: https://google.github.io/adk-docs/get-started
    *   Technical Overview: https://google.github.io/adk-docs/get-started/about
    *   Installation: https://google.github.io/adk-docs/get-started/installation
    *   Quickstart (Multi-tool): https://google.github.io/adk-docs/get-started/quickstart
    *   Python Guide: https://google.github.io/adk-docs/get-started/python
    *   Java Guide: https://google.github.io/adk-docs/get-started/java
    *   TypeScript Guide: https://google.github.io/adk-docs/get-started/typescript
    *   Go Guide: https://google.github.io/adk-docs/get-started/go

*   **Agents**
    *   Overview: https://google.github.io/adk-docs/agents
    *   Config: https://google.github.io/adk-docs/agents/config
    *   LLM Agents: https://google.github.io/adk-docs/agents/llm-agents
    *   Custom Agents: https://google.github.io/adk-docs/agents/custom-agents
    *   Multi-agent Systems: https://google.github.io/adk-docs/agents/multi-agents

*   **Workflow Agents**
    *   Overview: https://google.github.io/adk-docs/agents/workflow-agents
    *   Sequential: https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents
    *   Parallel: https://google.github.io/adk-docs/agents/workflow-agents/parallel-agents
    *   Loop: https://google.github.io/adk-docs/agents/workflow-agents/loop-agents

*   **Models**
    *   Overview: https://google.github.io/adk-docs/agents/models
    *   Google Gemini: https://google.github.io/adk-docs/agents/models/google-gemini
    *   Vertex AI: https://google.github.io/adk-docs/agents/models/vertex
    *   Anthropic Claude: https://google.github.io/adk-docs/agents/models/anthropic
    *   LiteLLM: https://google.github.io/adk-docs/agents/models/litellm
    *   Ollama: https://google.github.io/adk-docs/agents/models/ollama
    *   vLLM: https://google.github.io/adk-docs/agents/models/vllm
    *   Apigee AI Gateway: https://google.github.io/adk-docs/agents/models/apigee

*   **Tools (General & Custom)**
    *   Overview: https://google.github.io/adk-docs/tools
    *   Custom Tools: https://google.github.io/adk-docs/tools-custom
    *   Function Tools: https://google.github.io/adk-docs/tools-custom/function-tools
    *   OpenAPI Tools: https://google.github.io/adk-docs/tools-custom/openapi-tools
    *   MCP Tools: https://google.github.io/adk-docs/tools-custom/mcp-tools
    *   Authentication: https://google.github.io/adk-docs/tools-custom/authentication
    *   Confirmations: https://google.github.io/adk-docs/tools-custom/confirmation
    *   Performance: https://google.github.io/adk-docs/tools-custom/performance
    *   Limitations: https://google.github.io/adk-docs/tools/limitations

*   **Tools (Gemini & Google Cloud)**
    *   Gemini API Tools: https://google.github.io/adk-docs/tools/gemini-api
    *   Google Search: https://google.github.io/adk-docs/tools/gemini-api/google-search
    *   Code Execution: https://google.github.io/adk-docs/tools/gemini-api/code-execution
    *   Computer Use: https://google.github.io/adk-docs/tools/gemini-api/computer-use
    *   Google Cloud Tools: https://google.github.io/adk-docs/tools/google-cloud
    *   Vertex AI Search: https://google.github.io/adk-docs/tools/google-cloud/vertex-ai-search
    *   RAG Engine: https://google.github.io/adk-docs/tools/google-cloud/vertex-ai-rag-engine
    *   BigQuery: https://google.github.io/adk-docs/tools/google-cloud/bigquery
    *   Bigtable: https://google.github.io/adk-docs/tools/google-cloud/bigtable
    *   Spanner: https://google.github.io/adk-docs/tools/google-cloud/spanner
    *   Application Integration: https://google.github.io/adk-docs/tools/google-cloud/application-integration
    *   Apigee API Hub: https://google.github.io/adk-docs/tools/google-cloud/apigee-api-hub
    *   API Registry: https://google.github.io/adk-docs/tools/google-cloud/api-registry
    *   GKE Code Executor: https://google.github.io/adk-docs/tools/google-cloud/gke-code-executor
    *   Agent Engine Code Exec: https://google.github.io/adk-docs/tools/google-cloud/code-exec-agent-engine
    *   MCP Toolbox for Databases: https://google.github.io/adk-docs/tools/google-cloud/mcp-toolbox-for-databases
    *   Express Mode: https://google.github.io/adk-docs/tools/google-cloud/express-mode

*   **Tools (Third-Party)**
    *   Overview: https://google.github.io/adk-docs/tools/third-party
    *   GitHub: https://google.github.io/adk-docs/tools/third-party/github
    *   GitLab: https://google.github.io/adk-docs/tools/third-party/gitlab
    *   Atlassian: https://google.github.io/adk-docs/tools/third-party/atlassian
    *   Notion: https://google.github.io/adk-docs/tools/third-party/notion
    *   Linear: https://google.github.io/adk-docs/tools/third-party/linear
    *   Stripe: https://google.github.io/adk-docs/tools/third-party/stripe
    *   PayPal: https://google.github.io/adk-docs/tools/third-party/paypal
    *   Hugging Face: https://google.github.io/adk-docs/tools/third-party/hugging-face
    *   n8n: https://google.github.io/adk-docs/tools/third-party/n8n
    *   Qdrant: https://google.github.io/adk-docs/tools/third-party/qdrant
    *   Agentic UI: https://google.github.io/adk-docs/tools/third-party/ag-ui

*   **Sessions, Memory & State**
    *   Overview: https://google.github.io/adk-docs/sessions
    *   Session management: https://google.github.io/adk-docs/sessions/session
    *   Memory: https://google.github.io/adk-docs/sessions/memory
    *   State: https://google.github.io/adk-docs/sessions/state
    *   Rewind: https://google.github.io/adk-docs/sessions/rewind

*   **Streaming & Realtime**
    *   Overview: https://google.github.io/adk-docs/streaming
    *   Configuration: https://google.github.io/adk-docs/streaming/configuration
    *   Quickstart Java: https://google.github.io/adk-docs/get-started/streaming/quickstart-streaming-java
    *   Streaming Tools: https://google.github.io/adk-docs/streaming/streaming-tools
    *   Dev Guide Part 1 (Intro): https://google.github.io/adk-docs/streaming/dev-guide/part1
    *   Dev Guide Part 2 (Messages): https://google.github.io/adk-docs/streaming/dev-guide/part2
    *   Dev Guide Part 3 (Events): https://google.github.io/adk-docs/streaming/dev-guide/part3
    *   Dev Guide Part 4 (Run Config): https://google.github.io/adk-docs/streaming/dev-guide/part4
    *   Dev Guide Part 5 (Media): https://google.github.io/adk-docs/streaming/dev-guide/part5

*   **Context**
    *   Overview: https://google.github.io/adk-docs/context
    *   Caching: https://google.github.io/adk-docs/context/caching
    *   Compaction: https://google.github.io/adk-docs/context/compaction

*   **Deployment**
    *   Overview: https://google.github.io/adk-docs/deploy
    *   Agent Engine: https://google.github.io/adk-docs/deploy/agent-engine
    *   Standard Deploy: https://google.github.io/adk-docs/deploy/agent-engine/deploy
    *   Test Deployed: https://google.github.io/adk-docs/deploy/agent-engine/test
    *   Starter Pack: https://google.github.io/adk-docs/deploy/agent-engine/asp
    *   Cloud Run: https://google.github.io/adk-docs/deploy/cloud-run
    *   GKE: https://google.github.io/adk-docs/deploy/gke

*   **Observability**
    *   Logging: https://google.github.io/adk-docs/observability/logging
    *   Cloud Trace: https://google.github.io/adk-docs/observability/cloud-trace
    *   Agent Analytics: https://google.github.io/adk-docs/observability/bigquery-agent-analytics
    *   Arize AX: https://google.github.io/adk-docs/observability/arize-ax
    *   W&B Weave: https://google.github.io/adk-docs/observability/weave
    *   Phoenix: https://google.github.io/adk-docs/observability/phoenix
    *   AgentOps: https://google.github.io/adk-docs/observability/agentops
    *   Freeplay: https://google.github.io/adk-docs/observability/freeplay
    *   MLflow: https://google.github.io/adk-docs/observability/mlflow
    *   Monocle: https://google.github.io/adk-docs/observability/monocle

*   **Evaluation**
    *   Overview: https://google.github.io/adk-docs/evaluate
    *   Criteria: https://google.github.io/adk-docs/evaluate/criteria
    *   User Simulation: https://google.github.io/adk-docs/evaluate/user-sim

*   **Runtime**
    *   Overview: https://google.github.io/adk-docs/runtime
    *   CLI: https://google.github.io/adk-docs/runtime/command-line
    *   Web Interface: https://google.github.io/adk-docs/runtime/web-interface
    *   API Server: https://google.github.io/adk-docs/runtime/api-server
    *   Event Loop: https://google.github.io/adk-docs/runtime/event-loop
    *   Resume: https://google.github.io/adk-docs/runtime/resume
    *   RunConfig: https://google.github.io/adk-docs/runtime/runconfig

*   **Core Infrastructure**
    *   A2A Protocol: https://google.github.io/adk-docs/a2a
    *   A2A Intro: https://google.github.io/adk-docs/a2a/intro
    *   Apps: https://google.github.io/adk-docs/apps
    *   Artifacts: https://google.github.io/adk-docs/artifacts
    *   Callbacks: https://google.github.io/adk-docs/callbacks
    *   Events: https://google.github.io/adk-docs/events
    *   Plugins: https://google.github.io/adk-docs/plugins
    *   Reflect & Retry: https://google.github.io/adk-docs/plugins/reflect-and-retry
    *   Safety: https://google.github.io/adk-docs/safety
    *   Grounding Search: https://google.github.io/adk-docs/grounding/google_search_grounding
    *   Grounding Vertex: https://google.github.io/adk-docs/grounding/vertex_ai_search_grounding
    *   MCP: https://google.github.io/adk-docs/mcp

*   **Tutorials & Resources**
    *   Tutorials: https://google.github.io/adk-docs/tutorials
    *   Agent Team: https://google.github.io/adk-docs/tutorials/agent-team
    *   Coding with AI: https://google.github.io/adk-docs/tutorials/coding-with-ai
    *   Visual Builder: https://google.github.io/adk-docs/visual-builder
    *   Community: https://google.github.io/adk-docs/community
    *   Release Notes: https://google.github.io/adk-docs/release-notes
    *   Contributing: https://google.github.io/adk-docs/contributing-guide

**API Reference (Code & Signatures):**
*   **Consolidated Python API:** https://google.github.io/adk-docs/api-reference/python/google-adk.html
    *   *Contains details for:* `google.adk.agents`, `google.adk.tools`, `google.adk.memory`, `google.adk.models`, `google.adk.sessions`, `google.adk.runners`, `google.adk.planners`.
*   **Other References**
    *   CLI Reference: https://google.github.io/adk-docs/api-reference/cli
    *   Agent Config Reference: https://google.github.io/adk-docs/api-reference/agentconfig
    *   REST API Reference: https://google.github.io/adk-docs/api-reference/rest
    *   Java API Reference: https://google.github.io/adk-docs/api-reference/java
    *   TypeScript API Reference: https://google.github.io/adk-docs/api-reference/typescript
