from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks

from app.utilities import custom_outreach

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
async def outreach(queue: BackgroundTasks,
                   topic: str,
                   problems: str,
                   template_num: str):
    """<h3>Outreach</h3>
    Sends an AI Generated Cold Outreach Email
    <pre><code>
    @param queue: Automatic FastAPI BackgroundTasks.
    @param your_name: String.
    @param your_email: String.
    @param company: String.
    @param job_title: String.
    @param job_description: String.
    @param key_points_from_resume: String.
    @return: String.</code></pre>"""
    queue.add_task(topic,
                   problems,
                   template_num)
    return {"status": 200, "message": "job started"}