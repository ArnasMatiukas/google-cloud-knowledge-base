---
type: Tool
title: "Google Cloud Native Integrated & Local MCP Servers"
description: "Complete endpoint catalog and step-by-step connection guide for Google Cloud Native Integrated (Remote) MCP Servers (BigQuery, Spanner, AlloyDB, Cloud SQL, Firestore, Cloud Run, GKE, Logging) and Local CLI MCP Servers."
category: "8. MCP & Guardrails"
tags: [mcp, remote-mcp, bigquery-mcp, spanner-mcp, cloud-run-mcp, gcloud-mcp, developer-knowledge, adk-docs]
resource: "https://docs.cloud.google.com/mcp/supported-products"
timestamp: "2026-10-16T11:52:00Z"
aliases: ["Google Cloud MCP", "Remote MCP Servers", "Native Integrated MCP", "cloud-run-mcp"]
status: "active"
---

# Google Cloud Native Integrated & Local MCP Servers

Google Cloud natively integrates **managed Remote Model Context Protocol (MCP) endpoints** (`https://<service>.googleapis.com/mcp`) directly into its managed services ([Official Overview](https://docs.cloud.google.com/mcp/overview)). Instead of deploying or maintaining separate database/service MCP middleware, your coding agents ([Antigravity 2.0](antigravity_2_paygo_and_ide_setup.md), Gemini CLI) and runtime [ADK 2.0 agents](agent_development_kit_adk_and_skills.md) can connect directly over **Streamable HTTP** governed by Google Cloud IAM.

---

## 1. Google Cloud Native Integrated (Remote) MCP Endpoints

Each managed service exposes a stateless Streamable HTTP MCP server on `*.googleapis.com/mcp`. Full catalog: [Supported Products](https://docs.cloud.google.com/mcp/supported-products).

| Google Cloud Service | Native Remote MCP Endpoint (`Streamable HTTP`) | Service API to Enable (`gcloud services enable`) | Guide / Reference |
| :--- | :--- | :--- | :--- |
| **BigQuery** | `https://bigquery.googleapis.com/mcp` | `bigquery.googleapis.com` | [BigQuery MCP Guide](https://docs.cloud.google.com/bigquery/docs/use-bigquery-mcp) |
| **Spanner (Relational & Graph)** | `https://spanner.googleapis.com/mcp` | `spanner.googleapis.com` | [Spanner MCP Guide](https://docs.cloud.google.com/spanner/docs/use-spanner-mcp) |
| **AlloyDB for PostgreSQL** | `https://alloydb.googleapis.com/mcp` *(or `https://alloydb.REGION.rep.googleapis.com/mcp`)* | `alloydb.googleapis.com` | [Supported Products](https://docs.cloud.google.com/mcp/supported-products) |
| **Cloud SQL (PG / MySQL / MSSQL)** | `https://sqladmin.googleapis.com/mcp` | `sqladmin.googleapis.com` | [Supported Products](https://docs.cloud.google.com/mcp/supported-products) |
| **Firestore** | `https://firestore.googleapis.com/mcp` | `firestore.googleapis.com` | [Supported Products](https://docs.cloud.google.com/mcp/supported-products) |
| **Bigtable** | `https://bigtableadmin.googleapis.com/mcp` | `bigtableadmin.googleapis.com` | [Supported Products](https://docs.cloud.google.com/mcp/supported-products) |
| **Cloud Storage (GCS)** | `https://storage.googleapis.com/storage/mcp` | `storage.googleapis.com` | [Supported Products](https://docs.cloud.google.com/mcp/supported-products) |
| **Cloud Run** | `https://run.googleapis.com/mcp` | `run.googleapis.com` | [Supported Products](https://docs.cloud.google.com/mcp/supported-products) |
| **GKE (Kubernetes Engine)** | `https://container.googleapis.com/mcp` | `container.googleapis.com` | [Supported Products](https://docs.cloud.google.com/mcp/supported-products) |
| **Compute Engine** | `https://compute.googleapis.com/mcp` | `compute.googleapis.com` | [Supported Products](https://docs.cloud.google.com/mcp/supported-products) |
| **Cloud Logging, Monitoring & Trace** | `https://logging.googleapis.com/mcp`<br>`https://monitoring.googleapis.com/mcp`<br>`https://cloudtrace.googleapis.com/mcp` | `logging.googleapis.com`<br>`monitoring.googleapis.com`<br>`cloudtrace.googleapis.com` | [Supported Products](https://docs.cloud.google.com/mcp/supported-products) |
| **Pub/Sub & Managed Kafka** | `https://pubsub.googleapis.com/mcp`<br>`https://managedkafka.googleapis.com/mcp` | `pubsub.googleapis.com`<br>`managedkafka.googleapis.com` | [Supported Products](https://docs.cloud.google.com/mcp/supported-products) |
| **Resource Manager & IAM** | `https://cloudresourcemanager.googleapis.com/mcp`<br>`https://iam.googleapis.com/mcp` | `cloudresourcemanager.googleapis.com`<br>`iam.googleapis.com` | [Supported Products](https://docs.cloud.google.com/mcp/supported-products) |
| **Gemini Enterprise Agent Platform** | `https://aiplatform.googleapis.com/mcp/generate`<br>`https://aiplatform.googleapis.com/mcp/models`<br>`https://aiplatform.googleapis.com/mcp/retrieval`<br>`https://aiplatform.googleapis.com/mcp/evaluation` | `aiplatform.googleapis.com` | [Supported Products](https://docs.cloud.google.com/mcp/supported-products) |
| **Agent Search (Vertex AI Search)** | `https://discoveryengine.googleapis.com/mcp` | `discoveryengine.googleapis.com` | [Supported Products](https://docs.cloud.google.com/mcp/supported-products) |
| **Customer Experience Agent Studio** | `https://ces.us.rep.googleapis.com/mcp` | `ces.googleapis.com` | [Supported Products](https://docs.cloud.google.com/mcp/supported-products) |
| **Developer Knowledge API** | `https://developerknowledge.googleapis.com/mcp` | `developerknowledge.googleapis.com` | [Developer Knowledge Docs](https://developers.google.com/knowledge/api) |
| **Maps Grounding Lite** | `https://mapstools.googleapis.com/mcp` | `mapstools.googleapis.com` | [Supported Products](https://docs.cloud.google.com/mcp/supported-products) |

---

## 2. How to Connect to Google Cloud Native Integrated MCPs

Follow the official 4-step workflow ([Enable Products](https://docs.cloud.google.com/mcp/enable-disable-mcp-servers) · [Set Up Authentication](https://docs.cloud.google.com/mcp/set-up-authentication-mcp-servers) · [Configure AI Applications](https://docs.cloud.google.com/mcp/configure-mcp-ai-application)):

### Step 1: Enable the Product API in Your GCP Project
Enable the Google Cloud API for each service you want to access via MCP:

```bash
export GOOGLE_CLOUD_PROJECT="$(gcloud config get-value project)"

gcloud services enable \
  bigquery.googleapis.com \
  spanner.googleapis.com \
  alloydb.googleapis.com \
  sqladmin.googleapis.com \
  firestore.googleapis.com \
  run.googleapis.com \
  logging.googleapis.com \
  monitoring.googleapis.com \
  --project="$GOOGLE_CLOUD_PROJECT"
```

### Step 2: Grant the `roles/mcp.toolUser` IAM Role
Calling any Google Cloud remote MCP endpoint requires the `mcp.tools.call` permission (granted by **`roles/mcp.toolUser`**) alongside the underlying product role (e.g., `roles/bigquery.user`, `roles/spanner.databaseUser`, `roles/run.admin`):

```bash
export USER_EMAIL="$(gcloud config get-value account)"

gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
  --member="user:${USER_EMAIL}" \
  --role="roles/mcp.toolUser"
```

> [!TIP]
> **Service Accounts for Deployed Agents:** When running an agent on [Cloud Run](cloud_run_serverless_and_gpus.md) or [Vertex AI Agent Engine](vertex_ai_agent_engine.md), bind `roles/mcp.toolUser` to the agent's runtime service account (`--member="serviceAccount:AGENT_SA_EMAIL"`).

### Step 3: Connect Your Coding Agent (Antigravity 2.0 / IDE / Gemini CLI)

#### Option A: Antigravity 2.0 / VS Code via Application Default Credentials (ADC) Bearer Header
Generate an ADC access token (or extend its lifetime up to 12 hours if supported by your org policy) and pass `Authorization: Bearer <TOKEN>` alongside `x-goog-user-project`:

```bash
gcloud auth application-default login
export ADC_TOKEN="$(gcloud auth application-default print-access-token)"
```

Add the remote server to your MCP client configuration:
```json
{
  "mcpServers": {
    "gcp-bigquery-remote": {
      "serverUrl": "https://bigquery.googleapis.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_ADC_ACCESS_TOKEN",
        "x-goog-user-project": "your-hackathon-project-id"
      }
    },
    "gcp-spanner-remote": {
      "serverUrl": "https://spanner.googleapis.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_ADC_ACCESS_TOKEN",
        "x-goog-user-project": "your-hackathon-project-id"
      }
    }
  }
}
```

#### Option B: Antigravity 2.0 via OAuth 2.0 Client ID & Secret
If you prefer automatic token refresh in Antigravity 2.0 ([Set Up Authentication](https://docs.cloud.google.com/mcp/set-up-authentication-mcp-servers)), create an OAuth 2.0 Client ID in **Google Cloud Console -> Google Auth Platform -> Clients** with Antigravity's callback URI (`https://antigravity.google/oauth-callback`):

```json
{
  "mcpServers": {
    "gcp-cloudrun-remote": {
      "serverUrl": "https://run.googleapis.com/mcp",
      "oauth": {
        "clientId": "YOUR_CLIENT_ID.apps.googleusercontent.com",
        "clientSecret": "${MY_OAUTH_CLIENT_SECRET}",
        "scopes": ["https://www.googleapis.com/auth/cloud-platform"],
        "callbackPort": "https://antigravity.google/oauth-callback"
      }
    }
  }
}
```

#### Option C: Native `google_credentials` Extension (`~/.gemini/extensions/<name>/gemini-extension.json`)
```json
{
  "name": "gcp-native-mcp",
  "version": "1.0.0",
  "mcpServers": {
    "bigquery": {
      "httpUrl": "https://bigquery.googleapis.com/mcp",
      "authProviderType": "google_credentials",
      "oauth": {
        "scopes": ["https://www.googleapis.com/auth/bigquery"]
      },
      "timeout": 30000,
      "headers": {
        "x-goog-user-project": "your-hackathon-project-id"
      }
    }
  }
}
```

### Step 4: Connect Runtime ADK 2.0 Agents (`McpToolset` + `StreamableHTTPConnectionParams`)
In [Google ADK 2.0](agent_development_kit_adk_and_skills.md), connect your Python agent directly to any Google Cloud native remote MCP server using `google.auth.default()` (ADC) and `StreamableHTTPConnectionParams`:

```python
import os
import google.auth
import google.auth.transport.requests
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams


def build_gcp_native_mcp_toolset(mcp_url: str) -> McpToolset:
    """Connects an ADK agent to a Google Cloud native integrated MCP endpoint using ADC."""
    credentials, project_id = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    credentials.refresh(google.auth.transport.requests.Request())
    quota_project = os.environ.get("GOOGLE_CLOUD_PROJECT", project_id)

    return McpToolset(
        connection_params=StreamableHTTPConnectionParams(
            url=mcp_url,
            headers={
                "Authorization": f"Bearer {credentials.token}",
                "x-goog-user-project": quota_project,
            },
            timeout=60,
        )
    )


bigquery_mcp = build_gcp_native_mcp_toolset("https://bigquery.googleapis.com/mcp")
spanner_mcp = build_gcp_native_mcp_toolset("https://spanner.googleapis.com/mcp")

root_agent = LlmAgent(
    name="data_analyst_agent",
    model="gemini-3.8-flash",
    instruction="Use BigQuery and Spanner native MCP tools to inspect schemas and answer questions.",
    tools=[bigquery_mcp, spanner_mcp],
)
```

### Step 5: Test Connectivity with `curl`
Verify that your API enablement, `roles/mcp.toolUser` binding, and ADC token work by listing the remote server's tools:

```bash
curl -sS --location 'https://bigquery.googleapis.com/mcp' \
  --header "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
  --header "x-goog-user-project: $(gcloud config get-value project)" \
  --header 'Content-Type: application/json' \
  --header 'Accept: application/json, text/event-stream' \
  --data '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}'
```

---

## 3. Official Local CLI MCP Servers (Pre-Wired in `.agents/mcp_config.json`)

For local source-code deployments and offline documentation lookup, you can also run `./scripts/setup_antigravity_mcp.sh` from the repository root to merge these local stdio MCP servers into `~/.gemini/config/mcp_config.json`:

| Local MCP Server | Command / Package | What It Enables Your Agent To Do | Official Repository |
| :--- | :--- | :--- | :--- |
| **Cloud Run MCP** | `npx -y @google-cloud/cloud-run-mcp` | Deploy local source directories/Dockerfiles to [Cloud Run](cloud_run_serverless_and_gpus.md), list services, and inspect logs. | [GoogleCloudPlatform/cloud-run-mcp](https://github.com/GoogleCloudPlatform/cloud-run-mcp) |
| **gcloud CLI MCP** | `npx -y @google-cloud/gcloud-mcp` | Run `gcloud` CLI commands to inspect project configuration, enabled APIs, and IAM policies. | [googleapis/gcloud-mcp](https://github.com/googleapis/gcloud-mcp) |
| **GKE MCP** | `npx -y @google-cloud/gke-mcp` | Inspect and manage Google Kubernetes Engine (GKE) clusters and `kubectl` contexts. | [GoogleCloudPlatform/gke-mcp](https://github.com/GoogleCloudPlatform/gke-mcp) |
| **ADK Docs MCP** | `uvx --from mcpdoc --with "mcp<2" mcpdoc --urls AgentDevelopmentKit:https://adk.dev/llms.txt --transport stdio` | Search and read live [Google ADK 2.0 documentation](agent_development_kit_adk_and_skills.md) (`https://adk.dev/llms.txt`). | [adk.dev/tutorials/coding-with-ai](https://adk.dev/tutorials/coding-with-ai/) |

---

## Related Concepts

- [Agentic Protocols: MCP & A2A](protocols_mcp_and_a2a.md) — Connecting ADK agents to MCP servers via `McpToolset` and exposing A2A endpoints.
- [Antigravity 2.0 Pay-As-You-Go & IDE Setup](antigravity_2_paygo_and_ide_setup.md) — Configuring MCP servers in Antigravity 2.0.
- [Agent Development Kit (ADK 2.0) & Official Skills](agent_development_kit_adk_and_skills.md) — Combining MCP tools with ADK skills.
