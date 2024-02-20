# Classroom Toolkit API

Welcome to the Classroom Toolkit API, a powerful tool designed to assist teachers in generating comprehensive lesson plans tailored to their specific classroom needs. Utilizing the capabilities of Python, FastAPI, and the advanced natural language processing of GPT-4, our API provides a unique platform where educators can input the desired outcomes, problems, and learning objectives they wish students to tackle by the end of the lesson, and receive a customized lesson plan in return.

## Features

- **Custom Lesson Plans**: Generate lesson plans tailored to the specific topics, problems, and objectives you want to address in your classroom. Our API takes into consideration the complexities and nuances of educational content to produce practical and engaging lesson plans.

- **FastAPI Framework**: Built on the modern, fast web framework FastAPI, our API ensures high performance, easy testing, and quick implementation into existing systems or workflows.

- **GPT-4 Integration**: Leverage the cutting-edge language model for generating detailed, coherent, and contextually relevant lesson plans that can adapt to a wide range of subjects and learning objectives.

- **Flexible and Easy to Use**: Designed with simplicity in mind, our API offers straightforward endpoints that make it easy for developers and educators to integrate and use within their applications or digital classroom environments.

- **Cross-Origin Resource Sharing (CORS) Enabled**: Ensures your web applications can securely interact with our API from any client-side domain.

## API Endpoints

### `/version` - Get API Version
Retrieve the current version of the Classroom Toolkit API. This endpoint helps in tracking updates and changes to the API functionality.

### `/lesson_plan` - Generate Lesson Plan
Create a customized lesson plan based on the provided topic, problems to solve, learning objectives, quiz questions, and a challenge question. This endpoint accepts the topic, problems, objectives, quiz, and a single challenge in JSON format as inputs and utilizes background tasks to process and generate a lesson plan in Markdown format, allowing for asynchronous operation and efficient handling of resource-intensive tasks.

## Version

The current version of the API is 0.0.4. We are continuously working on improving and expanding the API's capabilities, so stay tuned for future updates!

For more information on how to use the API and to explore its full capabilities, please refer to the API documentation available at the root URL (`/`).

---