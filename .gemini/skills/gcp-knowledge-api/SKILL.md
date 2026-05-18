---
name: gcp-knowledge-api
description: Mandates using the Google Developer Knowledge API for any Google Cloud Platform (GCP) related implementation, brainstorming, or technical research. Use this skill 100% of the time when dealing with GCP tasks to ensure accurate, up-to-date documentation is consulted.
---

# Google Developer Knowledge API Mandate

When working on any task related to Google Cloud Platform (GCP) - including brainstorming, architecture design, implementation, or debugging - you MUST consult the Google Developer Knowledge API.

## Core Rules

1. **Always Search First:** Before writing code, configuring resources, or offering definitive advice about GCP, you must use the `mcp_google-developer-knowledge_search_documents` or `mcp_google-developer-knowledge_answer_query` tools to find the latest documentation and best practices.
2. **Never Guess:** GCP APIs and configurations change frequently. Do not rely solely on your pre-trained knowledge for specific GCP implementations.
3. **Deep Dives:** If `search_documents` provides relevant results but lacks sufficient detail, follow up with `mcp_google-developer-knowledge_get_documents` to retrieve the full context.
4. **Integration:** Use this knowledge to enrich your brainstorming sessions and ensure all suggested implementations adhere to Google's official, current guidelines.

By following this skill, you ensure all GCP solutions are grounded in official documentation.
