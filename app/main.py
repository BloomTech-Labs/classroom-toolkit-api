# Import necessary modules from FastAPI, Jinja2, and other libraries
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import json

# Import custom lesson plan generator function
from app.lessonplan import custom_lesson_plan

# Read the API description from README.md, skipping the first line
with open("README.md", "r") as file:
    next(file)  # Skip the first line
    api_description = file.read()

# Define API metadata
API_VERSION = "0.0.3"
API_TITLE = 'Classroom Toolkit API'
API_DESCRIPTION = api_description
DOCS_URL = '/'

# Initialize the FastAPI application with metadata
api_app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url=DOCS_URL,
)

# Configure CORS policy for the API to allow requests from any origin
api_app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Allow all origins
    allow_credentials=True,
    allow_methods=['*'],  # Allow all methods
    allow_headers=['*'],  # Allow all headers
)

# Define an endpoint to get the API version
@api_app.get("/version", tags=["General"])
async def get_api_version():
    """Returns the current version of the API."""
    return API_VERSION

@api_app.get("/lesson_plan", tags=["Toolkit"], response_class=PlainTextResponse)
async def generate_lesson_plan(topic: str, problems: str, objectives: str, quiz: str, challenge: str):
    """
    Generates a lesson plan in Markdown format, based on given parameters.
    
    Parameters:
    - topic: The main subject of the lesson plan.
    - problems: Problems to be addressed in the lesson plan.
    - objectives: Learning objectives for the lesson, separated by commas.
    - quiz: Quiz questions related to the topic.
    - challenge: Challenge question related to the topic in JSON format (not an array, just a single challenge).
    
    Returns:
    A PlainTextResponse containing the lesson plan in Markdown format.
    """
    # Get the lesson plan content as a JSON string from the generate function
    lesson_plan_json = custom_lesson_plan(topic, problems, objectives, quiz, challenge)

    # Parse the JSON string into a Python dictionary
    lesson_plan_data = json.loads(lesson_plan_json)

    # Start Markdown content with the topic and intro
    markdown_content = f"# {topic}\n\n## Introduction\n\n{lesson_plan_data['intro']}\n"

    # Split objectives into a list and create the Core Competencies section
    objectives_list = objectives.split(',')
    markdown_content += "## Core Competencies\n\n"
    for index, objective in enumerate(objectives_list, start=1):
        markdown_content += f"{index}. {objective.strip()}\n"

    # Iterate over problems and add their details to the Markdown content
    for problem in lesson_plan_data['problems']:
        # Add problem title as a subheading
        markdown_content += f"\n## {problem['core_competency']}\n\n"

        # Add relevance, problem statement
        markdown_content += f"**Relevance:** {problem['relevance']}\n\n"
        markdown_content += f"**Problem:** {problem['problem']}\n\n"

        # Check if there's a solution procedure
        if 'solution' in problem:
            markdown_content += "**Procedure:**\n\n"
            for step in problem['solution']:
                markdown_content += f"- {step}\n"
            markdown_content += "\n"

        # Add code snippet if it exists
        if 'code' in problem:
            markdown_content += f"**Code:**\n\n```javascript\n{problem['code']}\n```\n"

        # Add check for understanding
        if 'check_for_understanding' in problem:
            markdown_content += f"**Check For Understanding:** {problem['check_for_understanding']}\n"

    # Parse the challenge JSON string into a Python dictionary
    challenge_data = json.loads(challenge)

    # Add the Sprint Challenge Preview section
    markdown_content += f"\n## {challenge_data['title']}\n\n{challenge_data['intro']}\n"

    # Add details for the challenge
    ch = challenge_data['challenge']  # Directly access the challenge object
    markdown_content += f"\n### {ch['name']}\n\n**Objective:** {ch['objective']}\n\n**Functionality:**\n"
    for func in ch['functionality']:
        markdown_content += f"- {func}\n"
    markdown_content += "\n**Conditions:**\n"
    for cond in ch['conditions']:
        markdown_content += f"- {cond}\n"
    markdown_content += "\n**Hints:**\n"
    for hint in ch['hints']:
        markdown_content += f"- {hint}\n"
    markdown_content += "\n**Procedure:**\n"
    for proc in ch['procedure']:
        markdown_content += f"- {proc}\n"
    markdown_content += f"\n**Code:**\n\n```javascript\n{ch['code']}\n```\n"
    markdown_content += f"\n**Check For Understanding:** {ch['check_for_understanding']}\n"

    # Add conclusion
    markdown_content += f"\n## Conclusion\n\n{lesson_plan_data['conclusion']}\n"

    # Return the Markdown content
    return markdown_content
