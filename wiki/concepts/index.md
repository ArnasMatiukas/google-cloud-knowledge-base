# Google Cloud Concepts Index

> Auto-generated concept catalog. Last updated: 2026-10-16

### 1. Onboarding & Setup

| Concept | Type | Description | Tags |
| :--- | :--- | :--- | :--- |
| [Antigravity 2.0 Pay-As-You-Go (PayGo) & IDE Setup](antigravity_2_paygo_and_ide_setup.md) | `Guide` | How to configure Antigravity 2.0 Desktop App, CLI (agy), and IDE extensions as Pay-As-You-Go with hackathon Google Cloud accounts and pre-created GCP projects, and how .agents/skills/ loads out of the box. | antigravity, paygo, agy, ide, skills, mcp, gemini-enterprise |
| [Google Cloud CLI & Project Access Setup](gcp_cli_and_project_setup.md) | `Guide` | Step-by-step 5-minute guide for hackathon and workshop attendees to authenticate gcloud CLI, configure Application Default Credentials (ADC), bind a pre-created GCP project, and enable core Agent Platform APIs. | gcloud, cli, adc, authentication, iam, quota-project, onboarding |

### 2. Models & SDKs

| Concept | Type | Description | Tags |
| :--- | :--- | :--- | :--- |
| [Agent Platform Latest Models Catalog (Single Model Per Tier)](agent_platform_models.md) | `Concept` | Authoritative reference of the single latest, most capable Google Cloud Agent Platform (Vertex AI) model for every capability tier: Gemini 4 Argon, Gemini 3.8 Flash, Gemini 3.5 Flash-Lite, Gemini Embedding 2, TTS, Live API, Image, Video, Music, and Gemma 4. | models, gemini-4-argon, gemini-3-8-flash, gemini-embedding-2, gemini-3-8-live, nano-banana, omni, vertex-ai |
| [Gemini Embedding 2 (Multimodal Embeddings)](gemini_embedding_2_multimodal.md) | `Guide` | Complete guide to gemini-embedding-2 on Google Cloud Agent Platform: unified multimodal embeddings across text, images, audio, video, and PDFs (8,192 tokens), Matryoshka dimensionality, and task-specific optimization. | gemini-embedding-2, embeddings, multimodal, rag, graphrag, matryoshka, vector-search |
| [Google GenAI SDK on Vertex AI](google_genai_sdk_vertex.md) | `Guide` | How to use the unified google-genai SDK in Google Cloud Agent Platform (Vertex AI) mode for text generation, Pydantic structured outputs, function calling, GCS multimodal inputs, and context caching. | google-genai, python, sdk, vertex-ai, structured-outputs, function-calling, caching |

### 3. Agentic Frameworks

| Concept | Type | Description | Tags |
| :--- | :--- | :--- | :--- |
| [ADK 2.0 Graph Workflows, Human-in-the-Loop (HITL) & Pause/Resume](adk_graph_workflows_and_hitl.md) | `Architecture` | How to build deterministic, stateful multi-step processes in ADK 2.0 using Graph-based Workflows (Workflow, edges), Human Input nodes (RequestInput), Tool Confirmations (require_confirmation), and ResumabilityConfig. | adk, graphs, workflow, hitl, human-in-the-loop, confirmation, resume, state-machine |
| [Agent Development Kit (ADK 2.0) & Official ADK Skills](agent_development_kit_adk_and_skills.md) | `Guide` | Complete guide to Google's Agent Development Kit (ADK 2.0) on Vertex AI: LlmAgent, workflow orchestrators, where to find and install official ADK coding skills (google-agents-cli, adk.dev/llms.txt), and runtime SkillToolset. | adk, agents, skills, skill-toolset, google-agents-cli, llms-txt, multi-agent |
| [Agentic Protocols: MCP & A2A](protocols_mcp_and_a2a.md) | `Concept` | How Model Context Protocol (MCP) and the Agent2Agent (A2A) protocol work together on Google Cloud to connect agents to tools, databases, and remote specialist agents. | mcp, a2a, agent2agent, protocols, interoperability, adk, streamable-http |
| [Custom Frontend UI & Real-Time Agent Streaming (adk api_server, SSE & AG-UI)](agent_frontend_streaming_ag_ui.md) | `Guide` | How to connect custom React, Next.js, or Vite web frontends to ADK 2.0 agents on Vertex AI using the built-in ADK REST/SSE API Server (adk api_server / /run_sse) or the AG-UI protocol and CopilotKit. | frontend, streaming, sse, ag-ui, copilotkit, api-server, react, adk |
| [One-Command PoC Scaffolding: Agents CLI, Starter Pack & ADK Samples](poc_scaffolding_agents_cli_and_templates.md) | `Guide` | How to bootstrap full-stack, deployable Google Cloud multi-agent PoCs in under 60 seconds using Google Agents CLI (google-agents-cli), Agent Starter Pack, and official ADK Samples & Recipes. | agents-cli, agent-starter-pack, adk-samples, scaffolding, poc, cloud-run, agent-engine |
| [Vertex AI Agent Engine (Managed Agent Runtime)](vertex_ai_agent_engine.md) | `Architecture` | Deploying and scaling ADK and custom agents on Google Cloud's managed Vertex AI Agent Engine (ReasoningEngine) with managed Sessions, long-term Memory Bank, Code Execution Sandbox, and Cloud Trace. | agent-engine, reasoning-engine, vertex-ai, sessions, memory-bank, opentelemetry, adk |

### 4. Compute & Hosting

| Concept | Type | Description | Tags |
| :--- | :--- | :--- | :--- |
| [Google Cloud Run: Serverless Containers, Agents & GPUs](cloud_run_serverless_and_gpus.md) | `Guide` | Rapidly deploying web frontends, FastAPI backends, ADK 2.0 agents, remote MCP servers, and GPU-accelerated Gemma 4 open-weight models on Google Cloud Run. | cloud-run, serverless, containers, gpu, gemma-4, oidc, jobs, deployment |

### 5. Data & Analytics

| Concept | Type | Description | Tags |
| :--- | :--- | :--- | :--- |
| [Google BigQuery: Serverless Analytics, In-SQL Gemini & Vector Search](bigquery_ai_and_analytics.md) | `Guide` | How to use Google BigQuery in hackathons for serverless analytics, calling gemini-3.8-flash and gemini-embedding-2 directly inside SQL (AI.GENERATE, ML.GENERATE_EMBEDDING), Object Tables over GCS media, and VECTOR_SEARCH. | bigquery, bqml, ai-generate, vector-search, object-tables, sql, analytics |
| [Operational Data Stores: Spanner Graph, AlloyDB, Cloud SQL, Firestore & GCS](datastores_cloudsql_alloydb_spanner_firestore_gcs.md) | `Concept` | Decision matrix and quick-start patterns for choosing the right Google Cloud operational database or storage service in hackathons: Cloud Spanner Graph, AlloyDB AI, Cloud SQL for PostgreSQL (pgvector), Firestore, and Cloud Storage (GCS). | spanner, alloydb, cloud-sql, pgvector, firestore, gcs, storage, databases |

### 6. RAG & Knowledge

| Concept | Type | Description | Tags |
| :--- | :--- | :--- | :--- |
| [How to Build GraphRAGs on Google Cloud](graphrag_architectures_on_gcp.md) | `Architecture` | Complete architectural blueprint and implementation guide for building GraphRAG (Graph Retrieval-Augmented Generation) on Google Cloud using gemini-3.8-flash entity extraction, gemini-embedding-2 multimodal vectors, and 4 storage options: Cloud Spanner Graph, AlloyDB/Cloud SQL pgvector + AGE, BigQuery GraphRAG, and rapid NetworkX/OKF Wiki graphs. | graphrag, spanner-graph, alloydb, pgvector, bigquery, gemini-embedding-2, knowledge-graph |
| [RAG, Grounding & Search on Google Cloud](rag_grounding_and_search.md) | `Architecture` | Complete decision framework and implementation guide for Grounding and Retrieval-Augmented Generation (RAG) on Google Cloud: OKF LLM Wiki, Google Search & Maps Grounding, Vertex AI Search, Multimodal Vector RAG, and GraphRAG. | rag, grounding, google-search, google-maps, vertex-ai-search, gemini-embedding-2, okf-wiki |

### 7. Multimodal & Live

| Concept | Type | Description | Tags |
| :--- | :--- | :--- | :--- |
| [Multimodal Live API, Voice (TTS/ASR), Image & Video Generation](multimodal_live_voice_and_media.md) | `Guide` | How to build real-time voice, video, image, and music experiences on Google Cloud Agent Platform using only the latest models per tier: gemini-3.8-live, gemini-3.8-flash-tts, gemini-3.5-transcribe-live, gemini-nano-banana-2.1, gemini-omni-1.1-flash, and lyria-3.5. | live-api, gemini-3-8-live, tts, asr, nano-banana, omni, lyria, multimodal, voice |

### 8. MCP & Guardrails

| Concept | Type | Description | Tags |
| :--- | :--- | :--- | :--- |
| [Google Cloud Native Integrated & Local MCP Servers](gcp_mcp_servers_catalog.md) | `Tool` | Complete endpoint catalog and step-by-step connection guide for Google Cloud Native Integrated (Remote) MCP Servers (BigQuery, Spanner, AlloyDB, Cloud SQL, Firestore, Cloud Run, GKE, Logging) and Local CLI MCP Servers. | mcp, remote-mcp, bigquery-mcp, spanner-mcp, cloud-run-mcp, gcloud-mcp, developer-knowledge, adk-docs |
| [Security, FinOps & Quota Guardrails for Hackathons](security_finops_and_quotas.md) | `Guide` | Essential hackathon survival guide for avoiding 429 RESOURCE_EXHAUSTED quota errors on Vertex AI, managing third-party secrets in Secret Manager, protecting agents with Model Armor, and keeping GCP costs under control. | quotas, 429, global-endpoint, secret-manager, model-armor, finops, security, iam |

---
## Navigation
- [Root Wiki Index](../index.md)
- [Wiki Schema & Governance](../SCHEMA.md)
- [Changelog](../log.md)
