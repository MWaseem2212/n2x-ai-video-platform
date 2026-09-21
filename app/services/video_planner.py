import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from app.models.assets import VideoBrief, VideoPlan

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROQ_API_KEY"))
structured_llm = llm.with_structured_output(VideoPlan)


def generate_video_plan(brief: VideoBrief) -> VideoPlan:
    prompt = f"""
You are a video production planner for {brief.sector.value} sector content.

Create a structured video plan based on this brief:
- Country: {brief.country}
- Audience: {brief.audience}
- Tone: {brief.tone}
- Duration: {brief.duration_seconds} seconds
- Description: {brief.description}

Break the video into a clear scene-by-scene structure with approximate durations
that add up to the total duration.
"""
    return structured_llm.invoke(prompt)


if __name__ == "__main__":
    from app.models.assets import Sector

    test_brief = VideoBrief(
        sector=Sector.ADULT_CARE,
        country="United Kingdom",
        audience="Employees",
        tone="Professional, Reassuring",
        video_type="Training",
        duration_seconds=60,
        description="Adult social care video for UK care workers explaining the five signs of safeguarding concern",
    )

    plan = generate_video_plan(test_brief)
    print(f"Title: {plan.title}")
    print("Structure:")
    for item in plan.proposed_structure:
        print(f"  - {item}")
    print(f"Total duration: {plan.estimated_total_duration}s")