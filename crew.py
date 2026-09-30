import os
import time

from crewai import Crew, Process, LLM
from agents import create_agents
from tasks import create_tasks


MODEL_NAME = "groq/openai/gpt-oss-120b"
MAX_COMPLETION_TOKENS = 600


def build_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing. Add it to your environment or Streamlit Secrets.")

    return LLM(
        model=MODEL_NAME,
        api_key=api_key,
        temperature=0.7,
        max_completion_tokens=MAX_COMPLETION_TOKENS,
        reasoning_effort="low",
    )


def create_crew(idea, genre, language, duration):
    llm = build_llm()
    agents = create_agents(llm)
    tasks = create_tasks(agents, idea, genre, language, duration)

    return Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=False,
        max_rpm=5,
    )


def run_crew_with_retry(idea, genre, language, duration, retries=2):
    """Run the crew and wait automatically if Groq returns a TPM rate-limit error."""
    last_error = None

    for attempt in range(retries + 1):
        try:
            return create_crew(idea, genre, language, duration).kickoff()
        except Exception as exc:
            last_error = exc
            message = str(exc).lower()

            if "rate_limit" not in message and "rate limit" not in message:
                raise

            if attempt < retries:
                # Groq commonly tells us how long to wait. A safe 45-second pause
                # gives the 1-minute TPM window time to reset before retrying.
                time.sleep(45)

    raise last_error
