from typing import Optional

from pydantic import BaseModel, constr

class paragraph(BaseModel):
    topic: str(constr(min_length=5, max_length=100))
    description: Optional[str(constr(min_length=10, max_length=1000))]
    body: str

class bullet_points(BaseModel):
    topic: str(constr(min_length=5, max_length=100))
    points: list[str(constr(min_length=5, max_length=500))]

class numbered_list(BaseModel):
    topic: str(constr(min_length=5, max_length=100))
    points: list[str(constr(min_length=5, max_length=500))]

class problem(BaseModel):
    question: str
    answer: str(constr(min_length=5, max_length=1000))
    proceedure: numbered_list(constr(min_length=5))

class lesson_plan(BaseModel):
    title: str(constr(min_length=5, max_length=100))
    introduction: paragraph
    learning_objectives: numbered_list(constr(min_length=3, max_length=8))
    problems_to_be_addressed: list[problem]
    derivative_problems: list[problem](constr(min_length=5))
    conclusion: paragraph


default_paragraph = {
    "topic": "Your topic here",
    "description": "Your description here",
    "body": "Your body here"
}

default_bullet_points = {
    "topic": "Your topic here",
    "points": ["Your point here"]
}

default_numbered_list = {
    "topic": "Your topic here",
    "points": ["Your point here"]
}

default_problem = {
    "question": "Your question here",
    "answer": "Your answer here",
    "proceedure": {
        "topic": "Your topic here",
        "points": ["Your point here"]
    }
}

default_lesson_plan = {
    "title": "Your title here",
    "introduction": default_paragraph,
    "learning_objectives": default_numbered_list,
    "problems_to_be_addressed": [default_problem],
    "derivative_problems": [default_problem],
    "conclusion": default_paragraph
}
