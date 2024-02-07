import os
import json

from openai import OpenAI
from openai.types.chat.completion_create_params import ResponseFormat
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
response_format = ResponseFormat(type="json_object")

# Function to generate a lesson plan from the given topic and problems using GPT-3.5

def custom_lesson_plan(topic: str,
                    problems: str):
    """Generates a lesson plan based on the given topic and problems."""

    # Path to your JSON template file
    file_path = f"./assets/template_0206.json"

    # Read the JSON file and convert it to a string
    with open(file_path, 'r') as file:
        json_data = json.load(file)  # This loads the JSON as a Python dictionary

    # Convert the Python dictionary to a JSON string
    json_string = json.dumps(json_data)

    context = f"As a seasoned JavaScript educator with a decade of experience, you excel at crafting lesson plans with a focus on JSON-based structuring. Your task is to develop a lesson plan that aligns with the following schema: {json_string}."

    prompt = f"Your objective today is to devise a lesson plan dedicated to teaching {topic}. The core aim is to equip students with the skills to tackle the following questions: {problems}. Ensure the lesson plan is articulated in clear, straightforward language, making it accessible for any instructor to comprehend and execute." \
            f"\n\nThe lesson plan must be structured as per a JSON schema provided by us. Here's the schema you need to follow: {json_string}." \
            f"\n\nLet's delve into the schema details:" \
            f"\n- 'topic': A string indicating the lesson's subject." \
            f"\n- 'intro': A brief introduction to the lesson." \
            f"\n- 'problems': This should outline the challenges or questions the lesson aims to address, akin to the examples given above." \
            f"\n- There must be at least 6 problems in problems array. Generate more problems if needed. The new problems" \
            f"\n- must be the same level of difficulty as the examples. The directions/solution should be clear." \
            f"\n- 'conclusion': A summarization of the lesson, wrapping up the key points." \
            f"\n\nYour lesson plan should be formatted as JSON, adhering to the schema above."

    res = client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format=response_format,
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt},
        ]
    )
    
    lesson_plan =  res.choices[0].message.content

    print(lesson_plan)


    return lesson_plan