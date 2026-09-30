import os
import streamlit as st
from crew import run_crew_with_retry

st.set_page_config(page_title="AI Urdu Short Film Studio", page_icon="🎬", layout="wide")

# Streamlit Cloud stores secrets in st.secrets; local development can use an environment variable.
if "GROQ_API_KEY" not in os.environ and "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

st.title("🎬 AI Urdu Short Film Studio")
st.write("Turn a simple film idea into a complete Urdu short-film screenplay using a CrewAI multi-agent workflow.")

with st.sidebar:
    st.header("Film Settings")
    genre = st.selectbox("Genre", ["Drama", "Comedy", "Horror", "Thriller", "Social"])
    language = st.selectbox("Output Language", ["Urdu", "Roman Urdu", "Urdu + Roman Urdu"])
    duration = st.selectbox("Approximate Duration", ["5 minutes", "10 minutes", "15 minutes"])

idea = st.text_area(
    "💡 Enter your film idea",
    placeholder="Example: Aik ghareeb baap apni beti ki taleem ke liye apni motorcycle bech deta hai.",
    height=150,
)

if st.button("🎬 Generate Short Film", type="primary", use_container_width=True):
    if not idea.strip():
        st.warning("Please enter a film idea first.")
    else:
        with st.spinner("AI agents are developing your film... This may take some time."):
            try:
                result = run_crew_with_retry(idea.strip(), genre, language, duration)
                output = getattr(result, "raw", str(result))
                st.success("Your short-film screenplay is ready!")
                st.markdown(output)
                st.download_button(
                    "⬇️ Download Script",
                    data=output,
                    file_name="urdu_short_film_script.md",
                    mime="text/markdown",
                    use_container_width=True,
                )
            except Exception as exc:
                st.error(f"Something went wrong: {exc}")
                st.info("If Groq rate limiting occurs, the app automatically waits and retries. Do not press Generate repeatedly while a run is active.")
