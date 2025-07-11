import google.generativeai as genai
import os
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()
# Configure the Gemini API key
if "GEMINI_API_KEY" not in os.environ:  
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def get_kubectl_command(user_input):
    prompt = f"Generate a kubectl command for the following task: {user_input}"
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating command: {str(e)}"
   
    