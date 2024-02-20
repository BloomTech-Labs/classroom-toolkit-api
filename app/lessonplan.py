import os
import json
from openai import OpenAI
from openai.types.chat.completion_create_params import ResponseFormat
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize the OpenAI client with the API key from environment variables
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

# Set the response format for the OpenAI API to JSON
response_format = ResponseFormat(type="json_object")

def custom_lesson_plan(topic: str, problems: str, objectives: str, quiz: str, challenge: str):
    """
    Generates a lesson plan for teaching a specific topic, with given problems, objectives, and a quiz.
    The lesson plan is generated using GPT-4 and is structured as a JSON object.
    """

    # Specify the path to the JSON template file
    file_path = "./assets/template_0206.json"

    # Load the JSON template file and convert it to a dictionary
    with open(file_path, 'r') as file:
        json_template = json.load(file)

    # Convert the JSON template dictionary back to a JSON string for inclusion in the prompt
    json_template_string = json.dumps(json_template)

    # Define the context for the GPT-4 prompt, explaining the task and the JSON schema"
    context = (
        f"As an expert JavaScript educator with ten years of experience, your task is to create a lesson plan "
        f"that leverages JSON-based structuring. This plan should be encapsulated in a JSON object, following "
        f"a specific schema, and should be crafted to not only educate but also engage students through creative "
        f"and practical learning problems. The schema must exactly match the following: {json_template_string}."
        f"Lets breakdown the schema key by key: (1)'intro` is a string that introduces the lesson, (2) `problems`"
        f"is an array of `problem` objects, and (3) `conclusion` is a string that concludes the lesson. The `problem` "
        f"object has the following keys: (1) `core competency` is an objective that directly matches an objective inputted "
        f"by the user, (2) `relevance` is a string that explains the relevance of the problem, (2) `problem` is a string"
        f"that is a problem prompt that directly matches a problem inputted by the user, (3) `solution` is an array of "
        f"5-7 detailed steps to solving the problem, and (4) `code` is a string that gives a code snippet that"
        f"directly solves the problem. The `check_for_understanding` is a string that is a question that directly matches"
        f"a quiz inputted by the user. There must be at least 10 problems in the `problems` array. The `challenge` object"
        f"has the following keys: (1) `name`, (2) `objective`, (3) `functionality`, (4) `conditions`, (5) `hints`, (6)"
        f"`procedure`, and (7) `code`. The `name` is a string that is the name of the challenge."
        f"The objective` is a string that is the objective of the challenge. The `functionality` is a string that explains"
        f"what the challenge should do. The `conditions` is a string that explains the conditions of the challenge. The `hints`"
        f"is an array of strings that are hints to solving the challenge. The `procedure` is an array of strings that are steps"
        f"to solving the challenge. The `code` is a string that is a code snippet that solves the challenge."
    )

    # Define the prompt for GPT-4, detailing the requirements for the lesson plan
    prompt = (
        f"Your objective today is to devise a lesson plan dedicated to teaching {topic}. The core aim is to equip "
        f"students with the skills to tackle the following coding challenges: {problems}. Use these example problems "
        f"to build the `problems` array in the JSON schema, specifically `problem`, `solution`, and `code` inside "
        f"the `problem` object. Ensure the lesson plan is articulated in clear, straightforward language, making it "
        f"accessible for any instructor to comprehend and execute. The introduction should set the stage, offering a "
        f"glimpse into what the lesson entails and sparking curiosity among the students. The `relevance` key inside "
        f"`problem` should detail an on-the-job scenario when you might solve a similar problem. It should be in the form "
        f"of a short story, detailing how and when you might see the problem in real life. The `core_competency` in the "
        f"`problem` object should directly match one of the following objectives: {objectives}. The `check_for_understanding` "
        f"in the `problem` object must be similar to the following quiz: {quiz}. The `challenge` object must be similar to"
        f"{challenge}. Ensure the problem is unique to the topic, but formatted like the example. The conclusion should wrap up the lesson."
        f"Remember, the goal is not just to teach JavaScript, but to inspire a deeper understanding and appreciation for the "
        f"power of coding in solving real-world problems. With creativity, clarity, and a focus on practical applications, "
        f"your lesson plan will not just educate; it will illuminate."
    )

    # Use the OpenAI API to generate the lesson plan based on the provided context and prompt
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format=response_format,
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt},
        ]
    )

    # Extract the generated lesson plan from the API response
    lesson_plan = response.choices[0].message.content

    # Print the generated lesson plan
    print(lesson_plan)

    # Return the generated lesson plan
    return lesson_plan
