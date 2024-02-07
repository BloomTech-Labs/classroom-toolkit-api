# Import necessary modules from FastAPI, Jinja2, and other libraries
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json

# Import custom lesson plan generator function
from app.lessonplan import custom_lesson_plan

# Read the API description from README.md, skipping the first line
with open("README.md", "r") as file:
    next(file)  # Skip the first line
    api_description = file.read()

# Define API metadata
API_VERSION = "0.0.1"
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

# Set the directory for Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Define an endpoint to get the API version
@api_app.get("/version", tags=["General"])
async def get_api_version():
    """Returns the current version of the API."""
    return API_VERSION

# Define an endpoint to generate a lesson plan
@api_app.get("/lesson_plan", tags=["Toolkit"], response_class=HTMLResponse)
async def generate_lesson_plan(request: Request, topic: str, problems: str, objectives: str, quiz: str):
    """
    Generates a lesson plan based on a template, for a given topic and set of problems and objectives.
    
    Parameters:
    - request: FastAPI request object, needed for template context.
    - topic: The main subject of the lesson plan.
    - problems: Problems to be addressed in the lesson plan.
    - objectives: Learning objectives for the lesson.
    - quiz: Quiz questions related to the topic.
    
    Returns:
    An HTMLResponse containing the rendered lesson plan.
    """
    # Generate lesson plan content
    lesson_plan_data = json.loads(custom_lesson_plan(topic, problems, objectives, quiz))
    
    # Add objectives as a list and the topic to the lesson plan data
    lesson_plan_data["input_objectives"] = objectives.split(",")  # Convert objectives to a list
    lesson_plan_data["topic"] = topic  # Add topic

    # Render and return the HTML template for the lesson plan
    return templates.TemplateResponse("lesson_plan_1.html", {"request": request, **lesson_plan_data})
