from google import genai
from menu import return_as_str
 

def call_to_gemini(prompt):
    client = genai.Client(api_key=)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    return response.text 