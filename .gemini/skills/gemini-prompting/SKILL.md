---
name: gemini-prompting
description: Expert guidance on crafting effective prompts for Gemini models. Use when the user needs help writing, optimizing, or understanding prompts for Gemini.
---

# Gemini Prompting Guide

This skill provides the latest best practices and strategies for prompting Google's Gemini models.

## Procedure

1.  **Fetch Latest Best Practices**
    Use the `web_fetch` tool to retrieve the most up-to-date prompting guides from the following official sources:
    -   `https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide`
    -   `https://ai.google.dev/gemini-api/docs/prompting-strategies`

    *Note: If the `web_fetch` tool is unavailable or fails, rely on your internal knowledge base regarding Large Language Model prompting, but inform the user that you could not retrieve the live documentation.*

2.  **Synthesize and Assist**
    Based on the user's specific request (e.g., "Help me write a prompt for code generation" or "Optimize this prompt"), synthesize the fetched information to provide:
    -   **Clear Instructions:** Step-by-step guidance tailored to their goal.
    -   **Concrete Examples:** Use the examples found in the documentation or create similar ones that apply the retrieved strategies.
    -   **Optimization Tips:** Highlight specific techniques (like few-shot prompting, chain-of-thought, or role prompting) mentioned in the guides that are relevant to the user's task.

3.  **Iterate**
    Ask the user for feedback on the generated prompt or advice and refine based on the best practices.