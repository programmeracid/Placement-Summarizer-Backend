from google import genai
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access environment variables
gemini_api_key = os.getenv("gemini-api-key")
model = os.getenv("model")

# Configure your API key
# You can also set it as an environment variable (e.g., GOOGLE_API_KEY)
client=genai.Client(api_key=gemini_api_key)

def strict_check(details):
    instructions = """
    If the email subject presented above is related to any college placements activites including the following:
    Physical Process/Selection Process/Online Assessment/Online Test/Interview/Placement Registration/others
    then return True 
    else, return False

    ONLY return True for emails STRICTLY related to COLLEGE PLACEMENT ACTIVITIES

    Remember that you must RESPOND ONLY with True or False
    """
    response = client.models.generate_content(
        model=model,
        contents=details["subject"]+instructions
    )
    if response.text.strip()=="True":
        return True
    elif response.text.strip()=="False":
        return False
    raise ValueError(f"Incorrect response format:{response.text}")