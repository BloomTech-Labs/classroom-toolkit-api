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

def custom_lesson_plan(topic: str, problems: str, objectives: str, quiz: str):
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

    # Define the context for the GPT-4 prompt, explaining the task and the JSON schema
    context = (
        f"As an expert JavaScript educator with ten years of experience, your task is to create a lesson plan "
        f"that leverages JSON-based structuring. This plan should be encapsulated in a JSON object, following "
        f"a specific schema, and should be crafted to not only educate but also engage students through creative "
        f"and practical learning experiences. The schema must exactly match the following: {json_template_string}."
    )

    # Define the prompt for GPT-3.5, detailing the requirements for the lesson plan
    prompt = (
        f"Your objective today is to devise a lesson plan dedicated to teaching {topic}. The core aim is to equip "
        f"students with the skills to tackle the following questions: {problems}. Ensure the lesson plan is "
        f"articulated in clear, straightforward language, making it accessible for any instructor to comprehend "
        f"and execute. Your lesson plan should start with a clear topic, a subject that encapsulates the essence "
        f"of the lesson. The introduction should set the stage, offering a glimpse into what the lesson entails "
        f"and sparking curiosity among the students. The objectives you use must exactly match the following: "
        f"{objectives}. The problems you use must be similar to the following: {problems}. The quiz you use must "
        f"be similar to the following: {quiz}. Remember, the goal is not just to teach JavaScript, but to inspire "
        f"a deeper understanding and appreciation for the power of coding in solving real-world problems. With "
        f"creativity, clarity, and a focus on practical applications, your lesson plan will not just educate; it will illuminate."
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
