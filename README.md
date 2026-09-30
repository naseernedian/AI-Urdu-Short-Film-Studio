# AI Urdu Short Film Studio

A beginner-friendly CrewAI + Groq + Streamlit multi-agent application that turns a simple film idea into a short Urdu screenplay.

## Workflow

Idea → Story → Characters → Drama → Screenplay → Dialogue → Director → Scene Breakdown → Review → Final Script

## Important Groq rate-limit fix

The app is configured to reduce token usage and avoid sending large prompts unnecessarily. It also limits request frequency and automatically retries after a rate-limit error.

Groq rate limits are measured in tokens per minute (TPM), and the exact limit depends on the account/service tier. A free/on-demand organization can therefore receive a 429 error even when the API key is correct. The error is not a Python or Streamlit bug.

For this reason:

- Do not click **Generate Short Film** multiple times at once.
- Wait for the current generation to finish.
- The app uses `max_completion_tokens=600`.
- The app uses lower reasoning effort.
- Crew requests are limited with `max_rpm=5`.
- A rate-limit error triggers an automatic 45-second retry, up to two retries.

## Install

Use Python 3.11.

```bash
pip install -r requirements.txt
```

## API key

### Local

Set `GROQ_API_KEY` as an environment variable or create a `.env` file if you add dotenv support.

### Streamlit Community Cloud

In **Settings → Secrets**, add:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

## Run

```bash
streamlit run app.py
```

## If you still get a rate-limit error

The message will normally say how many seconds remain. Wait for that period before testing again. Groq documents TPM as a per-minute token limit. Increasing the API tier can provide higher limits, depending on the account and current Groq availability.
