from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json

from app.lessonplan import custom_lesson_plan

with open("README.md", "r") as file:
    next(file)
    description = file.read()

VERSION = "0.0.1"
API = FastAPI(
    title='Classroom Toolkit API',
    description=description,
    version=VERSION,
    docs_url='/',
)
API.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@API.get("/version", tags=["General"])
async def version():
    """<h3>Version</h3>
    Returns the current version of the API
    <pre><code>
    @return: String </code></pre>"""
    return VERSION


templates = Jinja2Templates(directory="app/templates")

@API.get("/lesson_plan", tags=["Toolkit"], response_class=HTMLResponse)
async def lesson_plan(request: Request, topic: str, problems: str, template_num: int):
    """
    <h3>Lesson Plan</h3>
    Generates a lesson plan based on a designated template for a given topic and problems.
    <pre><code>
    @param request: Request object for context inclusion.
    @param topic: Topic of the lesson plan.
    @param problems: Problems to include in the lesson plan.
    @param template_num: Template number to use for generating the lesson plan.
    @return: HTMLResponse containing the rendered lesson plan.</code></pre>
    """
    # Call a synchronous version of your custom_lesson_plan function
    lesson_plan_content = json.loads(custom_lesson_plan(topic, problems, template_num))

    print(lesson_plan_content)

    # Render the HTML template with the lesson plan content
    return templates.TemplateResponse("lesson_plan_1.html", {"request": request, **lesson_plan_content})