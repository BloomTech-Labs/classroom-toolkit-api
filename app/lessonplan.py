import os
import json
from time import sleep

import openai
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")


def dict_to_str(data) -> str:
    return f"""{{{', '.join(f'"{k}": "{v}"' for k, v in data.items())}}}"""


def try_retry_openai(context, prompt):

    def worker():
        return openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": prompt}
            ],
        )

    result = worker()
    while not result:
        sleep(5)
        result = worker()
    return result


def custom_lesson_plan(topic: str,
                    problems: str,
                    template_num: int):
    # Path to your JSON template file
    file_path = f"./app/template_{template_num}.json"

    # Read the JSON file and convert it to a string
    with open(file_path, 'r') as file:
        json_data = json.load(file)  # This loads the JSON as a Python dictionary

    # Convert the Python dictionary to a JSON string
    json_string = json.dumps(json_data)

    context = "You are a master at writing lesson plans. You have been teaching for 10 years."
    prompt = f"Today, you will be building a lesson plan that aims to teach {topic}." \
             f"Keep in mind, the ultimate goal of this lesson is to teach students" \
             f"how to solve the following problems/questions: {problems}." \
             f"Remember to use clear and straigtforward language in the lesson plan." \
             f"Any instructor should be able to understand and implement it easily." \
             f"You must output JSON data. The output should be in the following format: {json_string}." 
    result, *_ = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt},
        ],
    ).choices
    lesson_plan = result.get("message").get("content")
    print(lesson_plan)
