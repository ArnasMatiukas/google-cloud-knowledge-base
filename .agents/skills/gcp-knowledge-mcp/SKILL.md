---
name: gcp-knowledge-mcp
description: >-
  Query official Google Cloud documentation and manage cloud resources using
  Google Developer Knowledge MCP, ADK Docs MCP (`adk-docs-mcp`), and Google
  Cloud Local & Remote MCP servers (`cloud-run`, `gcloud`, `mcp-toolbox`). Use
  whenever you need live documentation beyond `wiki/concepts/` or need to
  inspect/deploy GCP resources via MCP.
---

# Google Cloud Knowledge & Service MCPs Skill

When working on Google Cloud tasks that require live API reference lookups or direct resource inspection beyond the local `wiki/concepts/` pages, use the configured Model Context Protocol (MCP) servers.

## 1. Documentation & Knowledge MCPs

### A. Google Developer Knowledge API MCP
- **Official Docs:** [https://developers.google.com/knowledge/api](https://developers.google.com/knowledge/api)
- **When to Use:** Whenever you need exact IAM permission strings, CLI flags, API request schemas, or newly released Google Cloud product details.
- **Workflow:**
  1. Call `search_documents` or `answer_query` (e.g., `mcp_google-developer-knowledge_search_documents`) first.
  2. Follow up with `get_documents` (`mcp_google-developer-knowledge_get_documents`) to read the full official documentation page.
  3. **Use Google Cloud / Vertex AI Documentation Only:** Always prefer the **Google Cloud / Vertex AI (`docs.cloud.google.com`)** specification with Application Default Credentials (ADC) over consumer API-key documentation.

### B. Official ADK Docs MCP (`adk-docs-mcp`)
- **Configured in:** `.agents/mcp_config.json` (serves `https://adk.dev/llms.txt`).
- **When to Use:** When inspecting Agent Development Kit (ADK 2.0) classes (`LlmAgent`, `SequentialAgent`, `ParallelAgent`, `LoopAgent`, `SkillToolset`, `McpToolset`) across Python, TypeScript, Go, Java, or Kotlin.

## 2. Operational Google Cloud MCP Servers

### A. Local MCP Servers (Pre-Wired in `.agents/mcp_config.json`)
- **Cloud Run MCP (`@google-cloud/cloud-run-mcp`):** Deploy applications, list Cloud Run services, inspect revisions, and fetch service URLs.
- **gcloud MCP (`@google-cloud/gcloud-mcp`):** Inspect active project configuration, enabled APIs, IAM bindings, and Cloud Logging entries.
- **MCP Toolbox for Databases (`googleapis/mcp-toolbox`):** Connect agents to Cloud SQL for PostgreSQL, AlloyDB, Spanner, BigQuery, and Firestore using ADC.

### B. Google Cloud Remote (Hosted) MCP Servers
Google Cloud provides hosted remote MCP endpoints (`https://docs.cloud.google.com/mcp/supported-products`) for BigQuery, Cloud Run, Spanner, AlloyDB, Cloud SQL, Firestore, GKE, Vertex AI Search, Developer Knowledge API, and Maps Grounding Lite.
- **IAM Requirement:** Ensure the user or service account has `roles/mcp.toolUser` enabled on the target GCP project.

## 3. Enabling MCPs in Antigravity 2.0
If MCP tools are not yet visible in the current Antigravity 2.0 session, run:
```bash
./scripts/setup_antigravity_mcp.sh
```
See [`wiki/concepts/gcp_mcp_servers_catalog.md`](../../../wiki/concepts/gcp_mcp_servers_catalog.md) for full configuration details.
