import os
import json
from time import sleep

import openai
from PyPDF2 import PdfReader, PdfWriter
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")

def preprocess_data_dict(data_dict):
    """Preprocesses the data dictionary to replace <br> with new lines."""
    processed_data = {}
    for key, value in data_dict.items():
        if isinstance(value, str):
            # Replace <br> with \n for line breaks
            processed_value = value.replace('<br>', '\n')
            processed_data[key] = processed_value
        else:
            # Copy value as is if it's not a string
            processed_data[key] = value
    return processed_data

def fill_pdf(input_pdf_path, output_pdf_path, data_dict):
    # Preprocess data_dict to handle <br> tags
    preprocessed_data_dict = preprocess_data_dict(data_dict)

    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # Assuming there's only one page
    page = reader.pages[0]
    writer.add_page(page)

    # Update form fields with preprocessed data
    writer.update_page_form_field_values(writer.pages[0], preprocessed_data_dict)

    # Write to an output PDF file
    with open(output_pdf_path, 'wb') as output_pdf:
        writer.write(output_pdf)


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
    file_path = f"./template_{template_num}.json"

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
    res = result.get("message").get("content")
    
    # Assuming res is structured as originally provided
    data_to_fill = {
        'Content Area': None,
        'Difficulty': None,
        'Topic': None,
        'Duration': None,
        'cc1': None,
        'cc2': None,
        'cc3': None,
        'cc4': None,
        'cc5': None,
        'cc6': None,
        'o1': None,
        'o2': None,
        'o3': None,
        'o4': None,
        'a1': None,
        'a2': None,
        'a3': None,
        'a4': None,
        'Materials': None,
        'Instruction': None,
        'Home Study': None
    }

    # convert res to a dictionary
    res = json.loads(res)

    print(res)

    data_to_fill = {
        'Content Area': res['lesson_plan']['content_area'],
        'Difficulty': res['lesson_plan']['difficulty'],
        'Topic': res['lesson_plan']['topic'],
        'Duration': res['lesson_plan']['duration'],
        'Materials': ', '.join(res['lesson_plan']['materials']),
        'Instruction': res['lesson_plan']['instruction'].replace('\n', '<br>'),
        'Home Study': res['lesson_plan']['home_study']
    }

    # Mapping core competencies
    for i, cc in enumerate(res['lesson_plan']['core_competencies'], start=1):
        data_to_fill[f'cc{i}'] = cc
    
    for i, cc in enumerate(res['lesson_plan']['objective'], start=1):
        data_to_fill[f'o{i}'] = cc

    for i, cc in enumerate(res['lesson_plan']['assessment'], start=1):
        data_to_fill[f'a{i}'] = cc

    processed_data = preprocess_data_dict(data_to_fill)

    fill_pdf('./assets/mit-lesson-plan-template-fillable.pdf', './output/filled-mit-lesson-plan.pdf', processed_data)
