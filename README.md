# Google Cloud Knowledge Base (Hackathon & Workshop Edition)

Concise starter repository, **Open Knowledge Format (OKF v0.2) LLM Wiki** (`wiki/`), and out-of-the-box **Antigravity 2.0** skill pack (`.agents/skills/`) for Google Cloud hackathons and workshops. All guides and tools use **Google Cloud Agent Platform (Vertex AI)** with Application Default Credentials (ADC).

---

## 1. Quick Start: GCP CLI & Project Setup (5 Minutes)

Hackathon participants receive a **Google Cloud user account** and a **pre-created fresh GCP project**. Run the following commands to configure CLI and SDK access:

- **Sign in with your provided Google Cloud account:**
  ```bash
  gcloud auth login
  ```
- **Set your pre-created GCP Project ID:**
  ```bash
  gcloud projects list
  export GOOGLE_CLOUD_PROJECT="your-hackathon-project-id"
  gcloud config set project "$GOOGLE_CLOUD_PROJECT"
  ```
- **Configure Application Default Credentials (ADC) & Quota Project:**
  ```bash
  gcloud auth application-default login
  gcloud auth application-default set-quota-project "$GOOGLE_CLOUD_PROJECT"
  ```
- **Enable core hackathon APIs and verify setup in one command:**
  ```bash
  ./scripts/verify_gcp_setup.sh --enable-apis
  ```
- **Export Agent Platform (Vertex AI) environment variables:**
  ```bash
  export GOOGLE_GENAI_USE_VERTEXAI=true
  export GOOGLE_CLOUD_PROJECT="your-hackathon-project-id"
  export GOOGLE_CLOUD_LOCATION="global"
  ```

**Source:** [Local CLI & Project Setup Guide](wiki/concepts/gcp_cli_and_project_setup.md) | [Agent Platform Overview](https://docs.cloud.google.com/gemini-enterprise-agent-platform/overview)

---

## 2. Using Antigravity 2.0 as Pay-As-You-Go (PayGo)

Open this repository in **Antigravity 2.0** (Desktop App, `agy` CLI, or VS Code / JetBrains IDE extension) to automatically load all workspace skills from `.agents/skills/` and bill usage Pay-As-You-Go to your hackathon GCP project:

- **Click "Login with Business" (Never "Continue with Google"):** On the Antigravity 2.0 login screen, click **"Login with Business" / "Use business account"** (or *"Prefer to use a GCP project?"*), sign in with your hackathon Google Cloud account, and enter your `$GOOGLE_CLOUD_PROJECT` (location: `global`). Never click *"Continue with Google"*, which routes to consumer free-tier rate limits.
- **Using Antigravity CLI (`agy`) with ADC:** After running `gcloud auth application-default login` and `gcloud config set project "$GOOGLE_CLOUD_PROJECT"`, run `agy` in this directory to inherit ADC credentials automatically.
- **Enable AI Developer Tools Overages:** In Cloud Console (`https://console.cloud.google.com/gemini-enterprise/settings/ai-developer-tools?project=YOUR_PROJECT_ID`), turn **On** AI Developer Tools, enable **Overages / Pay-As-You-Go**, and toggle on **Gemini 4 Argon**.
- **Wire Up Pre-Configured MCP Servers & Official ADK Skills:**
  ```bash
  ./scripts/setup_antigravity_mcp.sh --with-adk-skills
  ```

**Source:** [Antigravity 2.0 PayGo & IDE Setup Guide](wiki/concepts/antigravity_2_paygo_and_ide_setup.md) | [Download Antigravity 2.0](https://antigravity.google/download)

---

## 3. Local OKF (LLM Wiki) Knowledge Base & Built-In Agent Skills

This repository includes a 3-layer **Open Knowledge Format (OKF v0.2) LLM Wiki** in [`wiki/index.md`](wiki/index.md) and 8 auto-discovered skills in `.agents/skills/`. Search the wiki from your terminal or agent via `./scripts/okf_wiki_cli.py search "<topic>"`:

- **Onboarding & Setup:** [Google Cloud CLI & Project Access Setup](wiki/concepts/gcp_cli_and_project_setup.md) | [Antigravity 2.0 PayGo & IDE Setup](wiki/concepts/antigravity_2_paygo_and_ide_setup.md)
- **Models & SDKs (Single Latest Model Per Tier):** [Agent Platform Latest Models Catalog](wiki/concepts/agent_platform_models.md) | [Google GenAI SDK on Vertex AI](wiki/concepts/google_genai_sdk_vertex.md) | [Gemini Embedding 2 (Multimodal Embeddings)](wiki/concepts/gemini_embedding_2_multimodal.md)
- **Agentic Frameworks & Skills:** [Agent Development Kit (ADK 2.0) & Official ADK Skills](wiki/concepts/agent_development_kit_adk_and_skills.md) | [Vertex AI Agent Engine](wiki/concepts/vertex_ai_agent_engine.md) | [Agentic Protocols: MCP & A2A](wiki/concepts/protocols_mcp_and_a2a.md)
- **Compute, Data & Storage:** [Google Cloud Run: Serverless Containers & GPUs](wiki/concepts/cloud_run_serverless_and_gpus.md) | [Google BigQuery: AI & Analytics](wiki/concepts/bigquery_ai_and_analytics.md) | [Operational Data Stores: Spanner, AlloyDB, Cloud SQL, Firestore & GCS](wiki/concepts/datastores_cloudsql_alloydb_spanner_firestore_gcs.md)
- **RAG, GraphRAG & Multimodal:** [RAG, Grounding & Search on Google Cloud](wiki/concepts/rag_grounding_and_search.md) | [How to Build GraphRAGs on Google Cloud](wiki/concepts/graphrag_architectures_on_gcp.md) | [Multimodal Live API, Voice, Image & Video](wiki/concepts/multimodal_live_voice_and_media.md)
- **MCP Ecosystem & Guardrails:** [Google Cloud MCP Servers Catalog](wiki/concepts/gcp_mcp_servers_catalog.md) | [Security, FinOps & Quota Guardrails](wiki/concepts/security_finops_and_quotas.md)
- **Out-of-the-Box `.agents/skills/`:** `llm-wiki-search`, `gcp-knowledge-mcp`, `gcp-project-bootstrap`, `vertex-adk-builder`, `graphrag-and-embeddings`, `cloud-run-deploy`, `llm-wiki-ops`, and `brainstorming`.

**Source:** [OKF Wiki Master Index](wiki/index.md) | [OKF Wiki Schema](wiki/SCHEMA.md)

---

## 4. Google Cloud Agentic Tools, Models, Services & Frameworks

### Antigravity 2.0
Antigravity 2.0 is Google's agentic software engineering platform (Desktop Hub, `agy` CLI, and IDE extensions for VS Code and JetBrains) that natively loads `.agents/skills/` and bills Pay-As-You-Go against Google Cloud projects.

**Source:** [Official Website](https://antigravity.google/) | [Download](https://antigravity.google/download) | [Local PayGo Setup Guide](wiki/concepts/antigravity_2_paygo_and_ide_setup.md)

### Gemini CLI
Gemini CLI is an interactive command-line interface agent specializing in software engineering tasks, enabling developers to write code, execute commands, and manage Google Cloud projects directly from the terminal.

**Source:** [GitHub Repository](https://github.com/google-gemini/gemini-cli) | [Web Version](https://geminicli.com/)

### Google Cloud Agent Platform Models (Latest Model Per Tier)
Google Cloud Agent Platform (Vertex AI) provides enterprise access to Google's latest frontier models via the `global` endpoint. Use only the single latest model of each tier so your team never has to guess which model ID is most capable:

- **Frontier Reasoning, Coding & Video (Pro Tier):** `gemini-4-argon` (1M input / 1M output context)
- **High-Throughput Agent Workhorse (Flash Tier):** `gemini-3.8-flash` (1M input / 65K output context)
- **Ultra-Fast / High-Volume (Flash-Lite Tier):** `gemini-3.5-flash-lite` (1M input / 65K output context)
- **Multimodal Embeddings Tier:** `gemini-embedding-2` (Text, Image, Audio, Video, PDF in one vector space)
- **Text-to-Speech (TTS) Tier:** `gemini-3.8-flash-tts` and `gemini-3.8-flash-lite-tts`
- **Speech-to-Text / Transcription (ASR) Tier:** `gemini-3.5-transcribe-live` (streaming) and `gemini-3.5-transcribe` (batch)
- **Real-Time Bidirectional Voice & Video (Live API):** `gemini-3.8-live` and `gemini-3.8-live-extended-thinking`
- **Image Generation & Editing Tier:** `gemini-nano-banana-2.1` and `gemini-3.1-flash-lite-image`
- **Video & Audio Generation / Editing Tier:** `gemini-omni-1.1-flash`
- **Music & Song Generation Tier:** `lyria-3.5`
- **Open-Weight Models (Cloud Run GPUs):** `gemma-4-31b-it` and `gemma-4-26b-a4b-it`

**Source:** [Agent Platform Google Models](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/google-models) | [Gemini 4 Argon](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/4-argon) | [Gemini 3.8 Flash](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-8-flash) | [Local Models Catalog](wiki/concepts/agent_platform_models.md)

### Google GenAI SDK (`google-genai`)
The unified `google-genai` SDK is the standard client library for calling all Agent Platform models on Vertex AI (`GOOGLE_GENAI_USE_VERTEXAI=true`), supporting Pydantic structured outputs, tool calling, context caching, and Live API streaming.

**Source:** [GitHub Repository](https://github.com/googleapis/python-genai) | [Local SDK Guide](wiki/concepts/google_genai_sdk_vertex.md)

### Gemini Embedding 2 (`gemini-embedding-2`)
Gemini Embedding 2 is Google Cloud's native multimodal embedding model that maps text, images, audio, video, and PDF documents (up to 8,192 tokens) into a single unified vector space with Matryoshka dimensionality (`256`–`3072`).

**Source:** [Official Documentation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/embeddings) | [Local Multimodal Embeddings Guide](wiki/concepts/gemini_embedding_2_multimodal.md)

### Agent Development Kit (ADK 2.0) & Official ADK Skills
The Agent Development Kit (ADK) is Google's framework for building, evaluating, and deploying multi-agent systems. You can install official ADK coding skills into Antigravity 2.0 or Gemini CLI via `uvx google-agents-cli setup`, connect to `https://adk.dev/llms.txt`, and equip runtime agents with modular `SKILL.md` folders via `SkillToolset`.

**Source:** [Official Website](https://adk.dev/) | [Coding with AI & ADK CLI Skills](https://adk.dev/tutorials/coding-with-ai/) | [Runtime Skills for ADK Agents](https://adk.dev/skills/) | [Agents CLI](https://google.github.io/agents-cli/) | [ADK Python](https://github.com/google/adk-python) | [ADK Recipes](https://github.com/google/adk-recipes)

### Vertex AI Agent Engine
Vertex AI Agent Engine (`ReasoningEngine`) is a fully managed runtime on Google Cloud Agent Platform for deploying ADK and custom agents with managed sessions (`VertexAiSessionService`), long-term Memory Bank, code execution sandboxes, and OpenTelemetry tracing.

**Source:** [Official Documentation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale) | [Local Agent Engine Guide](wiki/concepts/vertex_ai_agent_engine.md)

### Agent2Agent (A2A) Protocol
The Agent2Agent (A2A) protocol is an open standard enabling independent AI agents to discover capabilities via an Agent Card (`/.well-known/agent-card.json`) and delegate tasks across services and organizations.

**Source:** [GitHub Repository](https://github.com/a2aproject/A2A) | [Local Protocols Guide](wiki/concepts/protocols_mcp_and_a2a.md)

### Google Developer Knowledge API
The Google Developer Knowledge API and its official MCP server enable AI agents to search and retrieve authoritative answers directly from live Google Cloud documentation.

**Source:** [Documentation](https://developers.google.com/knowledge/api)

### Google Cloud Run
Google Cloud Run is a fully managed serverless compute platform that deploys containerized web apps, APIs, ADK agents, remote MCP servers, and GPU-backed open-weight models (`gemma-4-31b-it` on NVIDIA L4) in seconds.

**Source:** [Official Website](https://cloud.google.com/run) | [Documentation](https://docs.cloud.google.com/run/docs) | [Local Cloud Run Guide](wiki/concepts/cloud_run_serverless_and_gpus.md)

### Google BigQuery
Google BigQuery is a serverless, multimodal data warehouse with built-in Gemini SQL functions (`AI.GENERATE`, `AI.GENERATE_TABLE`), GCS Object Tables, and native `VECTOR_SEARCH` powered by `gemini-embedding-2`.

**Source:** [Official Website](https://cloud.google.com/bigquery) | [Documentation](https://docs.cloud.google.com/bigquery/docs) | [Local BigQuery Guide](wiki/concepts/bigquery_ai_and_analytics.md)

### GraphRAG on Google Cloud (Spanner Graph, AlloyDB AI & Cloud SQL)
GraphRAG combines `gemini-embedding-2` vector similarity search with multi-hop knowledge graph traversal to answer complex relational queries across documents. Google Cloud supports four GraphRAG architectures:

- **Cloud Spanner Graph:** Zero-ETL multi-model database combining ISO GQL (`GRAPH_TABLE`) and native vector search (`COSINE_DISTANCE` / `APPROX_COSINE_DISTANCE`).
- **AlloyDB AI & Cloud SQL for PostgreSQL:** Relational tables paired with `pgvector` / `alloydb_scann` and recursive SQL CTEs or the `apache_age` openCypher extension.
- **BigQuery Serverless GraphRAG:** Batch entity-edge extraction with `AI.GENERATE_TABLE` and `VECTOR_SEARCH` joins in standard SQL.
- **Rapid Hackathon In-Memory GraphRAG:** Python `NetworkX` property graphs with `gemini-embedding-2` seed lookup and $k$-hop ego-graph expansion.

**Source:** [Spanner Graph Documentation](https://docs.cloud.google.com/spanner/docs/graph/overview) | [AlloyDB AI Documentation](https://docs.cloud.google.com/alloydb/docs/ai) | [Cloud SQL Vector Documentation](https://docs.cloud.google.com/sql/docs/postgres/generate-manage-vector-embeddings) | [Local GraphRAG Blueprint](wiki/concepts/graphrag_architectures_on_gcp.md)

### Google Cloud Firestore & Cloud Storage (GCS)
Firestore provides a zero-configuration serverless document database with real-time listeners and KNN vector search for agent state, while Cloud Storage (`gs://`) stores multimodal media passed directly to Gemini models.

**Source:** [Firestore Documentation](https://docs.cloud.google.com/firestore/native/docs) | [Cloud Storage Documentation](https://docs.cloud.google.com/storage/docs) | [Local Data Stores Guide](wiki/concepts/datastores_cloudsql_alloydb_spanner_firestore_gcs.md)

---

## 5. Community Skill Directories & Workspace Extensions

### Skills.sh Gallery
A community-driven directory showcasing reusable skills, prompts, and configurations for extending coding agents.

**Source:** [https://www.skills.sh/](https://www.skills.sh/)

### Antigravity Kit (AG-Kit)
A community template toolkit providing ready-to-use skills, agents, and workflows for rapid project bootstrapping.

**Source:** [https://github.com/vudovn/ag-kit](https://github.com/vudovn/ag-kit)

### Gemini Kit
An extension kit tailored for Gemini CLI featuring pre-configured agents and commands for automated planning, testing, and security reviews.

**Source:** [https://github.com/nth5693/gemini-kit](https://github.com/nth5693/gemini-kit)

### Gemini CLI Workspace Extension
A dedicated extension for Gemini CLI that leverages a local MCP server to query and interact with Google Workspace data such as emails, docs, and calendars.

**Source:** [https://github.com/gemini-cli-extensions/workspace](https://github.com/gemini-cli-extensions/workspace)

---

## 6. Google Cloud Local MCP Servers

### Cloud Run MCP
An MCP server that enables AI coding agents to deploy, inspect, and manage applications on Google Cloud Run.

**Source:** [https://github.com/GoogleCloudPlatform/cloud-run-mcp](https://github.com/GoogleCloudPlatform/cloud-run-mcp)

### GKE MCP
An MCP server that allows compatible AI agents to interact with and manage Google Kubernetes Engine (GKE) clusters.

**Source:** [https://github.com/GoogleCloudPlatform/gke-mcp](https://github.com/GoogleCloudPlatform/gke-mcp)

### gcloud MCP
An MCP server that exposes the functionality of the Google Cloud CLI (`gcloud`), allowing AI agents to inspect and manage Google Cloud resources directly.

**Source:** [https://github.com/googleapis/gcloud-mcp](https://github.com/googleapis/gcloud-mcp)

---

## 7. Google Cloud Native Integrated (Remote) MCP Servers

### Managed Google Cloud Remote MCP Endpoints
Google Cloud provides native, fully managed remote MCP servers hosted directly on each service's HTTP endpoint (`https://<service>.googleapis.com/mcp`) using Streamable HTTP transport and Google Cloud IAM (`roles/mcp.toolUser`), eliminating the need to self-host database or infrastructure MCP middleware. Supported products and endpoints include:

- **BigQuery:** `https://bigquery.googleapis.com/mcp`
- **Spanner (Relational & Spanner Graph):** `https://spanner.googleapis.com/mcp`
- **AlloyDB for PostgreSQL:** `https://alloydb.googleapis.com/mcp`
- **Cloud SQL (PostgreSQL, MySQL, SQL Server):** `https://sqladmin.googleapis.com/mcp`
- **Firestore:** `https://firestore.googleapis.com/mcp`
- **Bigtable:** `https://bigtableadmin.googleapis.com/mcp`
- **Cloud Storage (GCS):** `https://storage.googleapis.com/storage/mcp`
- **Cloud Run:** `https://run.googleapis.com/mcp`
- **Google Kubernetes Engine (GKE):** `https://container.googleapis.com/mcp`
- **Compute Engine:** `https://compute.googleapis.com/mcp`
- **Cloud Logging, Monitoring & Trace:** `https://logging.googleapis.com/mcp`, `https://monitoring.googleapis.com/mcp`, `https://cloudtrace.googleapis.com/mcp`
- **Pub/Sub & Managed Kafka:** `https://pubsub.googleapis.com/mcp`, `https://managedkafka.googleapis.com/mcp`
- **Resource Manager & IAM:** `https://cloudresourcemanager.googleapis.com/mcp`, `https://iam.googleapis.com/mcp`
- **Gemini Enterprise Agent Platform & Vertex AI Search:** `https://aiplatform.googleapis.com/mcp/generate`, `https://discoveryengine.googleapis.com/mcp`
- **Customer Experience Agent Studio:** `https://ces.us.rep.googleapis.com/mcp`
- **Developer Knowledge API & Maps Grounding Lite:** `https://developerknowledge.googleapis.com/mcp`, `https://mapstools.googleapis.com/mcp`

**Source:** [Supported Products & Endpoints](https://docs.cloud.google.com/mcp/supported-products) | [Google Cloud MCP Overview](https://docs.cloud.google.com/mcp/overview) | [Local MCP Catalog & Connection Guide](wiki/concepts/gcp_mcp_servers_catalog.md)

### Connecting to Google Cloud Native Integrated MCP Servers
To connect Antigravity 2.0, Gemini CLI, or custom ADK agents (`McpToolset`) to any native Google Cloud remote MCP endpoint, enable the target service API, grant `roles/mcp.toolUser`, and pass your Application Default Credentials (ADC) token with the `x-goog-user-project` header:

- **Enable the product API and grant the MCP Tool User role:**
  ```bash
  gcloud services enable bigquery.googleapis.com spanner.googleapis.com sqladmin.googleapis.com alloydb.googleapis.com firestore.googleapis.com
  gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
    --member="user:$(gcloud config get-value account)" \
    --role="roles/mcp.toolUser"
  ```
- **Authenticate via ADC Headers (`Authorization` + `x-goog-user-project`) or OAuth:** Point your MCP client or ADK `StreamableHTTPConnectionParams` to `https://<service>.googleapis.com/mcp` with `Authorization: Bearer $(gcloud auth application-default print-access-token)` and `x-goog-user-project: $GOOGLE_CLOUD_PROJECT`.

**Source:** [Configure MCP in an AI Application](https://docs.cloud.google.com/mcp/configure-mcp-ai-application) | [Set Up Authentication to MCP Servers](https://docs.cloud.google.com/mcp/set-up-authentication-mcp-servers) | [Enable Supported Products](https://docs.cloud.google.com/mcp/enable-disable-mcp-servers) | [Local Step-by-Step Connection Guide](wiki/concepts/gcp_mcp_servers_catalog.md)
