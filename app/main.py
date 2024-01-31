from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks

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


@API.get("/lesson_plan", tags=["Lesson Plans"])
async def lessonplan(queue: BackgroundTasks,
                   topic: str,
                   problems: str,
                   template_num: int):
    """<h3>Lesson Plan 1</h3>
    Generates a lesson plan based on template 1 for a given topic and problems.
    <pre><code>
    @param queue: Automatic FastAPI BackgroundTasks.
    @param topic: String.
    @param problems: String.
    @param template_num: Integer.
    @return: String.</code></pre>"""
    queue.add_task(custom_lesson_plan,
                   topic,
                   problems,
                   template_num)
    return {"status": 200, "message": "job started"}