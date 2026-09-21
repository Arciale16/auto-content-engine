import os
import json
from google import genai


def generate(prompt):

    client = genai.Client(
        api_key=os.environ["GEMINI_API_KEY"]
    )

    models = [
        "gemini-3.8-flash",
        "gemini-3.7-flash",
        "gemini-3.6-flash",
        "gemini-flash-latest"
    ]

    last_error = None

    for model in models:

        try:
            print("Trying Gemini:", model)

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            return json.loads(response.text)

        except Exception as error:
            print("Failed:", model)
            last_error = error

    raise last_error