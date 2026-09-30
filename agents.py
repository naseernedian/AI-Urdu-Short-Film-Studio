from crewai import Agent, LLM


def create_agents(llm: LLM):
    return {
        "idea": Agent(role="Film Concept Developer", goal="Turn a simple film idea into a strong short-film concept.", backstory="Experienced Pakistani film concept developer.", llm=llm, verbose=False),
        "story": Agent(role="Story Writer", goal="Develop a coherent beginning, conflict, climax and ending.", backstory="Specialist in concise South Asian storytelling.", llm=llm, verbose=False),
        "character": Agent(role="Character Designer", goal="Create believable characters with motivations, relationships and arcs.", backstory="Character designer for realistic Pakistani short films.", llm=llm, verbose=False),
        "drama": Agent(role="Drama Specialist", goal="Strengthen emotion, conflict, tension and character development.", backstory="Experienced drama-development specialist.", llm=llm, verbose=False),
        "screenplay": Agent(role="Screenplay Writer", goal="Convert the story into a practical scene-by-scene screenplay.", backstory="Screenwriter who creates production-friendly short-film scripts.", llm=llm, verbose=False),
        "dialogue": Agent(role="Urdu Dialogue Writer", goal="Write natural, culturally appropriate Urdu or Roman Urdu dialogue.", backstory="Writer specializing in natural Pakistani dialogue.", llm=llm, verbose=False),
        "director": Agent(role="Film Director", goal="Add practical camera, movement, sound, location and mood directions.", backstory="Short-film director focused on practical production.", llm=llm, verbose=False),
        "scene": Agent(role="Scene Breakdown Specialist", goal="Organize the screenplay into clear production-ready scenes.", backstory="Production planner for short films.", llm=llm, verbose=False),
        "review": Agent(role="Script Review Agent", goal="Check continuity, logic, pacing, character consistency and language quality.", backstory="Strict screenplay quality-control editor.", llm=llm, verbose=False),
    }
