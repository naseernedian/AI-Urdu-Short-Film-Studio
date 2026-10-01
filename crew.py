import os
import time

from crewai import Crew, Process, LLM
from agents import create_agents
from tasks import create_tasks


# Groq model
MODEL_NAME = "groq/openai/gpt-oss-120b"

# Keep responses reasonably small to reduce token usage
MAX_COMPLETION_TOKENS = 650


def build_llm():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. "
            "Add it to Streamlit Secrets."
        )

    return LLM(
        model=MODEL_NAME,
        api_key=api_key,
        temperature=0.7,
        max_completion_tokens=MAX_COMPLETION_TOKENS,
        reasoning_effort="low",
    )


def create_crew(
    idea,
    genre,
    language,
    duration
):

    llm = build_llm()

    agents = create_agents(llm)

    tasks = create_tasks(
        agents,
        idea,
        genre,
        language,
        duration
    )

    # Use only the agents needed by our optimized workflow
    active_names = [
        "idea",
        "story",
        "screenplay",
        "dialogue",
        "scene",
        "review"
    ]

    return Crew(
        agents=[
            agents[name]
            for name in active_names
        ],
        tasks=tasks,
        process=Process.sequential,
        verbose=False,
        max_rpm=5
    )


def run_crew_with_retry(
    idea,
    genre,
    language,
    duration,
    retries=2
):

    last_error = None

    for attempt in range(retries + 1):

        try:

            crew = create_crew(
                idea,
                genre,
                language,
                duration
            )

            return crew.kickoff()

        except Exception as exc:

            last_error = exc

            message = str(exc).lower()

            # If it is not a rate-limit problem,
            # immediately show the real error.
            if (
                "rate_limit" not in message
                and "rate limit" not in message
            ):
                raise

            # Detect requests that are too large
            request_too_large = (
                "request too large" in message
                or (
                    "requested" in message
                    and "tokens per minute" in message
                    and "limit" in message
                )
            )

            if request_too_large:

                raise RuntimeError(
                    "Groq rejected one AI request because it was "
                    "too large for the current token-per-minute "
                    "limit. Try a shorter film idea or use a "
                    "Groq model/account with a higher TPM limit."
                ) from exc

            # Wait before retrying
            if attempt < retries:

                time.sleep(65)

    raise last_error
