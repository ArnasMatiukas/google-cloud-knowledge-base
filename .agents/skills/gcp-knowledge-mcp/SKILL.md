---
name: gcp-knowledge-mcp
description: >-
  Query official Google Cloud documentation and connect to Google Cloud Native
  Integrated (Remote) MCP servers (`https://<service>.googleapis.com/mcp` for
  BigQuery, Spanner, AlloyDB, Cloud SQL, Firestore, Cloud Run, Logging, and
  Developer Knowledge API), ADK Docs MCP (`adk-docs-mcp`), and Local CLI MCP
  servers (`cloud-run`, `gcloud`). Use whenever you need live documentation
  beyond `wiki/concepts/` or need to connect/inspect GCP resources via MCP.
---

# Google Cloud Knowledge & Native Integrated MCPs Skill

When working on Google Cloud tasks that require live API reference lookups or direct resource inspection beyond the local `wiki/concepts/` pages, use Google Cloud's native integrated Model Context Protocol (MCP) endpoints and configured local MCP servers.

## 1. Documentation & Knowledge MCPs

### A. Google Developer Knowledge API MCP (`https://developerknowledge.googleapis.com/mcp`)
- **Official Docs:** [https://developers.google.com/knowledge/api](https://developers.google.com/knowledge/api)
- **When to Use:** Whenever you need exact IAM permission strings, CLI flags, API request schemas, or newly released Google Cloud product details.
- **Workflow:**
  1. Call `search_documents` or `answer_query` (e.g., `mcp_google-developer-knowledge_search_documents`) first.
  2. Follow up with `get_documents` (`mcp_google-developer-knowledge_get_documents`) to read the full official documentation page.
  3. **Use Google Cloud / Vertex AI Documentation Only:** Always prefer the **Google Cloud / Vertex AI (`docs.cloud.google.com`)** specification with Application Default Credentials (ADC) over consumer API-key documentation.

### B. Official ADK Docs MCP (`adk-docs-mcp`)
- **Configured in:** `.agents/mcp_config.json` (serves `https://adk.dev/llms.txt`).
- **When to Use:** When inspecting Agent Development Kit (ADK 2.0) classes (`LlmAgent`, `SequentialAgent`, `ParallelAgent`, `LoopAgent`, `SkillToolset`, `McpToolset`) across Python, TypeScript, Go, Java, or Kotlin.

## 2. Google Cloud Native Integrated (Remote) MCP Servers

Google Cloud natively integrates managed Streamable HTTP MCP endpoints (`https://<service>.googleapis.com/mcp`) directly into its services ([Supported Products](https://docs.cloud.google.com/mcp/supported-products)), eliminating the need for self-hosted database MCP middleware:
- **BigQuery:** `https://bigquery.googleapis.com/mcp`
- **Spanner (Relational & Graph):** `https://spanner.googleapis.com/mcp`
- **AlloyDB for PostgreSQL:** `https://alloydb.googleapis.com/mcp`
- **Cloud SQL:** `https://sqladmin.googleapis.com/mcp`
- **Firestore & Bigtable:** `https://firestore.googleapis.com/mcp`, `https://bigtableadmin.googleapis.com/mcp`
- **Cloud Run & Cloud Storage:** `https://run.googleapis.com/mcp`, `https://storage.googleapis.com/storage/mcp`
- **GKE & Compute Engine:** `https://container.googleapis.com/mcp`, `https://compute.googleapis.com/mcp`
- **Observability:** `https://logging.googleapis.com/mcp`, `https://monitoring.googleapis.com/mcp`, `https://cloudtrace.googleapis.com/mcp`
- **Gemini Enterprise Agent Platform & Vertex AI Search:** `https://aiplatform.googleapis.com/mcp/generate`, `https://discoveryengine.googleapis.com/mcp`

### How to Connect to Native Integrated GCP MCPs:
1. **Enable the Product API:** `gcloud services enable <service>.googleapis.com --project="$GOOGLE_CLOUD_PROJECT"`
2. **Grant `roles/mcp.toolUser`:** Ensure the calling user or agent service account has `roles/mcp.toolUser` (`mcp.tools.call`) plus the service role (e.g., `roles/bigquery.user`, `roles/spanner.databaseUser`).
3. **Authenticate via ADC Headers (`Streamable HTTP`):** Pass `Authorization: Bearer $(gcloud auth application-default print-access-token)` and `x-goog-user-project: $GOOGLE_CLOUD_PROJECT` in Antigravity 2.0 `mcp_config.json` or ADK `McpToolset(connection_params=StreamableHTTPConnectionParams(url=..., headers=...))`.

## 3. Local CLI MCP Servers (Pre-Wired in `.agents/mcp_config.json`)
- **Cloud Run MCP (`@google-cloud/cloud-run-mcp`):** Deploy local source directories to Cloud Run, list services, and inspect logs.
- **gcloud MCP (`@google-cloud/gcloud-mcp`):** Inspect active project configuration, enabled APIs, and IAM bindings.

If local MCP tools are not yet merged into `~/.gemini/config/mcp_config.json`, run:
```bash
./scripts/setup_antigravity_mcp.sh
```
See [`wiki/concepts/gcp_mcp_servers_catalog.md`](../../../wiki/concepts/gcp_mcp_servers_catalog.md) for full configuration snippets and examples.
