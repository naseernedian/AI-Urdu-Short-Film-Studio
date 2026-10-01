from crewai import Task


def create_tasks(
    agents,
    idea,
    genre,
    language,
    duration
):

    context = (
        f"Idea: {idea}\n"
        f"Genre: {genre}\n"
        f"Language: {language}\n"
        f"Duration: {duration}"
    )


    # ---------------- TASK 1 ----------------
    # Film Idea Agent

    t1 = Task(

        description=(
            f"Create the core short-film concept from:\n"
            f"{context}\n\n"

            "Return:\n"
            "1. Title\n"
            "2. Logline\n"
            "3. Theme\n"
            "4. Central conflict\n"
            "5. Beginning, middle and ending\n\n"

            "Keep the concept concise."
        ),

        expected_output=(
            "A concise film concept in under 180 words."
        ),

        agent=agents["idea"]
    )


    # ---------------- TASK 2 ----------------
    # Story + Characters

    t2 = Task(

        description=(
            "Expand the film concept into a complete and "
            "coherent short story.\n\n"

            "Also create the essential characters.\n\n"

            "For each important character include:\n"
            "- Name\n"
            "- Role\n"
            "- Motivation\n"
            "- Relationship\n"
            "- Character development\n\n"

            "Keep the story practical for the requested "
            "film duration."
        ),

        expected_output=(
            "A concise story and essential character profiles "
            "in under 300 words."
        ),

        agent=agents["story"],

        context=[t1]
    )


    # ---------------- TASK 3 ----------------
    # Screenplay

    t3 = Task(

        description=(
            "Convert the story into a practical "
            "scene-by-scene screenplay.\n\n"

            "Use 5 to 8 scenes.\n\n"

            "Every scene should contain:\n"
            "- Scene heading\n"
            "- Location\n"
            "- Time\n"
            "- Short action\n"
            "- Dialogue placeholders\n\n"

            "Keep the pacing suitable for the requested "
            "film duration."
        ),

        expected_output=(
            "A 5 to 8 scene screenplay draft."
        ),

        agent=agents["screenplay"],

        context=[t2]
    )


    # ---------------- TASK 4 ----------------
    # Dialogue + Direction

    t4 = Task(

        description=(
            f"Rewrite the screenplay using natural and "
            f"culturally appropriate {language} dialogue.\n\n"

            f"The film genre is {genre}.\n\n"

            "Add only important:\n"
            "- Camera shots\n"
            "- Camera movement\n"
            "- Sound\n"
            "- Mood\n"
            "- Visual directions\n\n"

            "Do not change the main story."
            "Keep scenes concise."
        ),

        expected_output=(
            "A concise directed screenplay with "
            "natural dialogue."
        ),

        agent=agents["dialogue"],

        context=[t3]
    )


    # ---------------- TASK 5 ----------------
    # Scene Organization

    t5 = Task(

        description=(
            "Organize the directed screenplay into a clean "
            "production-ready scene breakdown.\n\n"

            "Preserve all important:\n"
            "- Dialogue\n"
            "- Actions\n"
            "- Camera directions\n"
            "- Sounds\n"
            "- Locations\n\n"

            "Remove unnecessary repetition."
        ),

        expected_output=(
            "A clean 5 to 8 scene production-ready screenplay."
        ),

        agent=agents["scene"],

        context=[t4]
    )


    # ---------------- TASK 6 ----------------
    # Final Review

    t6 = Task(

        description=(
            "Perform final quality control on the screenplay.\n\n"

            "Check and fix:\n"
            "- Continuity\n"
            "- Logic\n"
            "- Repetition\n"
            "- Pacing\n"
            "- Character consistency\n"
            "- Language mistakes\n"
            "- Dialogue quality\n\n"

            "Return ONLY the polished final short-film "
            "screenplay.\n\n"

            "Do not explain the review process."
        ),

        expected_output=(
            "The final polished short-film screenplay."
        ),

        agent=agents["review"],

        context=[t5]
    )


    return [
        t1,
        t2,
        t3,
        t4,
        t5,
        t6
    ]
