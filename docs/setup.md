# Setup Guide

This page walks you through setting up your environment for the workshop.

## Option A: GitHub Codespaces (Recommended)

The fastest way to get started — no local setup required. Everything is pre-configured.

1. Go to the repository on GitHub
2. Click **Code** → **Codespaces** → **Create codespace on main**
3. Wait for the environment to build (~2 minutes)
4. Dependencies are installed automatically — just configure your `.env` file (see [Step 4](#4-configure-your-provider) below)
5. Run the connection test:

```bash
python exercises/00_setup/01_test_connection.py
```

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/{{repository}}?quickstart=1)

---

## Option B: Local Setup

## Prerequisites

- **Python 3.11+** installed
- A terminal (bash, zsh, PowerShell)
- An API key for at least one LLM provider (see below)

## 1. Clone the Repository

```bash
git clone <repository-url>
cd AI_Workshop_Agentic_Patterns
```

## 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:

- `openai` — The OpenAI Python SDK (works with all 3 providers)
- `python-dotenv` — Loads environment variables from `.env`
- `pydantic` — Data validation and structured output schemas
- `mkdocs-material` — Documentation site (for reading these docs locally)

## 4. Configure Your Provider

Copy the example environment file:

```bash
cp .env.example .env
```

Then edit `.env` with your provider credentials:

=== "GitHub Models (Recommended for Getting Started)"

    ```dotenv
    LLM_PROVIDER=github
    GITHUB_TOKEN=your_github_token_here
    MODEL_NAME=gpt-4o-mini
    ```

    **How to get a token:**

    1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
    2. Generate a new token (classic) with no special scopes needed
    3. GitHub Models provides free-tier access to GPT-4o, GPT-4o-mini, and other models

=== "OpenAI"

    ```dotenv
    LLM_PROVIDER=openai
    OPENAI_API_KEY=sk-your-key-here
    MODEL_NAME=gpt-4o-mini
    ```

    **How to get a key:**

    1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
    2. Create a new API key
    3. Add billing/credits to your account

=== "Azure AI Foundry"

    ```dotenv
    LLM_PROVIDER=azure
    AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
    AZURE_OPENAI_API_KEY=your-key-here
    AZURE_OPENAI_DEPLOYMENT=your-deployment-name
    AZURE_OPENAI_API_VERSION=2024-12-01-preview
    MODEL_NAME=gpt-4o-mini
    ```

    **How to set up:**

    1. Create an Azure OpenAI resource in the Azure Portal
    2. Deploy a model (e.g., `gpt-4o-mini`) in Azure AI Foundry
    3. Copy the endpoint, key, and deployment name

## 5. Test Your Connection

```bash
python exercises/00_setup/01_test_connection.py
```

You should see output like:

```
[INFO] Testing connection to LLM provider...
[INFO] Provider: github
[INFO] Model: gpt-4o-mini
[INFO] Response: Hello! How can I help you today?
[INFO] Connection successful!
```

If you see errors, check:

- Is your `.env` file in the project root?
- Are your API credentials correct?
- Is the model name valid for your provider?

## 6. (Optional) Serve the Documentation Locally

```bash
mkdocs serve
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Environment Variables Reference

| Variable | Required For | Description |
|----------|-------------|-------------|
| `LLM_PROVIDER` | All | `openai`, `azure`, or `github` |
| `OPENAI_API_KEY` | OpenAI | Your OpenAI API key |
| `GITHUB_TOKEN` | GitHub Models | Your GitHub personal access token |
| `AZURE_OPENAI_ENDPOINT` | Azure | Your Azure OpenAI endpoint URL |
| `AZURE_OPENAI_API_KEY` | Azure | Your Azure OpenAI key |
| `AZURE_OPENAI_DEPLOYMENT` | Azure | Your deployed model name |
| `AZURE_OPENAI_API_VERSION` | Azure | API version (e.g., `2024-12-01-preview`) |
| `MODEL_NAME` | Optional | Override the default model name |
| `LOG_LEVEL` | Optional | `DEBUG`, `INFO` (default), `WARNING` |

## Next Steps

Once your connection test passes, proceed to [Chat Completions API](concepts/chat-completions-api.md) to start learning.
