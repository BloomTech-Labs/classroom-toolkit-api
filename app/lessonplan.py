import os
import json

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


# Function to generate a lesson plan from the given topic and problems using GPT-3.5

def custom_lesson_plan(topic: str,
                    problems: str,
                    template_num: int):
    """Generates a lesson plan based on the given topic and problems."""

    # Path to your JSON template file
    file_path = f"./assets/bt_template_{template_num}.json"

    problem_file_path = f"./assets/problem.json"

    # Read the JSON file and convert it to a string
    with open(file_path, 'r') as file:
        json_data = json.load(file)  # This loads the JSON as a Python dictionary
        
    with open(problem_file_path, 'r') as problem_file_path:
        problem_data = json.load(problem_file_path)

    # Convert the Python dictionary to a JSON string
    json_string = json.dumps(json_data)
    problem_string = json.dumps(problem_data)

    context = "You are a master at writing lesson plans. You have been teaching for 10 years."
    prompt = f"Today, you will be building a lesson plan that aims to teach {topic}." \
             f"Keep in mind, the ultimate goal of this lesson is to teach students" \
             f"how to solve the following problems/questions: {problems}." \
             f"Remember to use clear and straigtforward language in the lesson plan." \
             f"Any instructor should be able to understand and implement this lesson plan easily." \
             f"Your output must be JSON and exactly match the following schema: {json_string}." \
             f"The output has 2 sections: input_problems and derivative_problems." \
             f"The input_problems section contains the problems/questions that exactly match the problems/questions provided by the user." \
             f"The derivative_problems section contains problems/questions and their solutions that are derived from the problems/questions provided by the user." \
             f"Both of these sections are lists of object that looks exactly like this: {problem_string}."
    res = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt},
        ]
    )
    
    lesson_plan =  res.choices[0].message.content


    return lesson_plan