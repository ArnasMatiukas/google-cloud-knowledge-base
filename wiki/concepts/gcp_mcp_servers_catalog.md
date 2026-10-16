---
type: Tool
title: "Google Cloud MCP Servers Catalog (Local & Remote)"
description: "Complete catalog and configuration guide for Google Cloud Local MCP Servers (cloud-run-mcp, gcloud-mcp, gke-mcp, mcp-toolbox), Official ADK Docs MCP, and Google Cloud Hosted Remote MCP Servers."
category: "8. MCP & Guardrails"
tags: [mcp, cloud-run-mcp, gcloud-mcp, mcp-toolbox, developer-knowledge, remote-mcp, adk-docs]
resource: "https://docs.cloud.google.com/mcp/supported-products"
timestamp: "2026-10-16T10:25:00Z"
aliases: ["Google Cloud MCP", "Remote MCP Servers", "MCP Toolbox", "cloud-run-mcp"]
status: "active"
---

# Google Cloud MCP Servers Catalog (Local & Remote)

Google Cloud provides both **Local MCP Servers** (which run via `npx` or `uvx` on your machine using your local [Application Default Credentials](gcp_cli_and_project_setup.md)) and **Hosted Remote MCP Servers** (managed HTTPS endpoints on Google Cloud).

---

## 1. Official Local MCP Servers (Pre-Wired in `.agents/mcp_config.json`)

Run `./scripts/setup_antigravity_mcp.sh` from the repository root to merge the core local MCP servers into `~/.gemini/config/mcp_config.json` for [Antigravity 2.0](antigravity_2_paygo_and_ide_setup.md).

| Local MCP Server | Command / Package | What It Enables Your Agent To Do | Official Repository |
| :--- | :--- | :--- | :--- |
| **Cloud Run MCP** | `npx -y @google-cloud/cloud-run-mcp` | Deploy apps from source/containers, list services, inspect logs, and manage revisions on [Cloud Run](cloud_run_serverless_and_gpus.md). | [GoogleCloudPlatform/cloud-run-mcp](https://github.com/GoogleCloudPlatform/cloud-run-mcp) |
| **gcloud CLI MCP** | `npx -y @google-cloud/gcloud-mcp` | Inspect project configuration, enabled APIs, IAM policies, and Cloud Logging entries via `gcloud`. | [googleapis/gcloud-mcp](https://github.com/googleapis/gcloud-mcp) |
| **GKE MCP** | `npx -y @google-cloud/gke-mcp` | Inspect and manage Google Kubernetes Engine (GKE) clusters and workloads. | [GoogleCloudPlatform/gke-mcp](https://github.com/GoogleCloudPlatform/gke-mcp) |
| **MCP Toolbox for Databases** | `googleapis/mcp-toolbox` | Connect AI agents safely to [Cloud SQL, AlloyDB, Spanner](datastores_cloudsql_alloydb_spanner_firestore_gcs.md), [BigQuery](bigquery_ai_and_analytics.md), and Firestore with parameterized SQL/GQL tools. | [googleapis/mcp-toolbox](https://github.com/googleapis/mcp-toolbox) |
| **ADK Docs MCP** | `uvx --from mcpdoc --with "mcp<2" mcpdoc --urls AgentDevelopmentKit:https://adk.dev/llms.txt --transport stdio` | Search and read live [Google ADK 2.0 documentation](agent_development_kit_adk_and_skills.md) (`https://adk.dev/llms.txt`). | [adk.dev/tutorials/coding-with-ai](https://adk.dev/tutorials/coding-with-ai/) |

---

## 2. Google Cloud Hosted Remote MCP Servers

Google Cloud hosts managed, IAM-authenticated **Remote MCP Servers** so your agents can interact with cloud services without spawning local Node.js/Python subprocesses.

**Official Documentation:** [Google Cloud Remote MCP Supported Products](https://docs.cloud.google.com/mcp/supported-products)

### Supported Google Cloud Remote MCP Products:
- **Developer Knowledge API** ([https://developers.google.com/knowledge/api](https://developers.google.com/knowledge/api)) — Search and retrieve official Google Cloud documentation.
- **BigQuery** — Discover dataset schemas and run serverless SQL queries.
- **Cloud Run** — Manage and inspect Cloud Run services remotely.
- **Spanner** — Query relational tables and [Spanner Graph (`GRAPH_TABLE`)](graphrag_architectures_on_gcp.md).
- **AlloyDB for PostgreSQL** & **Cloud SQL** — Execute managed database queries and vector searches.
- **Firestore** & **Bigtable** — Read and write NoSQL documents and wide-column tables.
- **Vertex AI Search** — Query enterprise RAG data stores.
- **Maps Grounding Lite** — Ground agents in live geospatial places, routes, and coordinates.
- **Customer Experience Agent Studio** — Integrate with CX Agent Studio workflows.
- **Cloud Logging** & **Cloud Monitoring** — Query logs, metrics, and alerts.
- **Compute Engine**, **GKE**, **Resource Manager**, **Managed Service for Apache Kafka**, and **Google Security Operations**.

### IAM Requirement for Remote MCP Servers
To call any Google Cloud Remote MCP server, ensure the calling user or service account has:
- `roles/mcp.toolUser` (*MCP Tool User*)
- Plus the underlying service role (e.g., `roles/bigquery.user`, `roles/run.admin`, `roles/spanner.databaseUser`).

---

## Related Concepts

- [Agentic Protocols: MCP & A2A](protocols_mcp_and_a2a.md) — Connecting ADK agents to MCP servers via `McpToolset`.
- [Antigravity 2.0 Pay-As-You-Go & IDE Setup](antigravity_2_paygo_and_ide_setup.md) — Configuring MCP servers in Antigravity 2.0.
- [Agent Development Kit (ADK 2.0) & Official Skills](agent_development_kit_adk_and_skills.md) — Combining MCP tools with ADK skills.
