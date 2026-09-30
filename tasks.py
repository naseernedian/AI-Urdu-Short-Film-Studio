from crewai import Task


def create_tasks(agents, idea, genre, language, duration):
    context = (
        f"Idea: {idea}\n"
        f"Genre: {genre}\n"
        f"Language: {language}\n"
        f"Duration: {duration}"
    )

    t1 = Task(
        description=f"Create a concise film concept from:\n{context}\nReturn title, logline, theme, conflict and a 3-part story arc.",
        expected_output="A concise film concept in under 250 words.",
        agent=agents["idea"],
    )
    t2 = Task(
        description="Expand the concept into a concise story with setup, conflict, climax and ending. Do not repeat the concept unnecessarily.",
        expected_output="A short complete story in under 350 words.",
        agent=agents["story"],
        context=[t1],
    )
    t3 = Task(
        description="Create the essential main and supporting characters. Give each role, motivation, relationship and short arc.",
        expected_output="A concise character list in under 250 words.",
        agent=agents["character"],
        context=[t2],
    )
    t4 = Task(
        description="Improve emotional conflict, stakes and character development. Keep the existing story concise and practical.",
        expected_output="A concise dramatic structure in under 300 words.",
        agent=agents["drama"],
        context=[t2, t3],
    )
    t5 = Task(
        description="Convert the story into a concise scene-by-scene screenplay. Include scene heading, action and short dialogue placeholders.",
        expected_output="A screenplay draft with 5 to 8 scenes.",
        agent=agents["screenplay"],
        context=[t4, t3],
    )
    t6 = Task(
        description=f"Rewrite the screenplay using natural, culturally appropriate {language} dialogue for a {genre} film. Keep scenes concise.",
        expected_output="A concise screenplay with natural dialogue.",
        agent=agents["dialogue"],
        context=[t5],
    )
    t7 = Task(
        description="Add only important camera shots, movement, mood, sound and visual directions. Avoid excessive directing notes.",
        expected_output="A concise directed screenplay.",
        agent=agents["director"],
        context=[t6],
    )
    t8 = Task(
        description="Organize the screenplay into a clean production-ready scene breakdown while preserving the story and dialogue.",
        expected_output="A clean 5 to 8 scene breakdown.",
        agent=agents["scene"],
        context=[t7],
    )
    t9 = Task(
        description="Perform final quality control. Fix continuity, logic, repetition, pacing and language. Return ONLY the polished final screenplay.",
        expected_output="The final polished short-film screenplay.",
        agent=agents["review"],
        context=[t8],
    )

    return [t1, t2, t3, t4, t5, t6, t7, t8, t9]
