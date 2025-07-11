import google.generativeai as genai
import os
import dotenv
import re

# Load environment variables from .env file
dotenv.load_dotenv()
# Configure the Gemini API key
if "GEMINI_API_KEY" not in os.environ:  
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

def clean_gemini_output(raw_cmd):
    # Removes markdown formatting and backticks
    cleaned = re.sub(r"```(bash|shell)?", "", raw_cmd)
    cleaned = cleaned.replace("```", "").strip()
    
    # Remove anything before 'kubectl' if explanation comes first
    if "kubectl" in cleaned:
        cleaned = cleaned[cleaned.find("kubectl"):]
    return cleaned


def get_kubectl_command(user_input):
    try:
        response = chat.send_message(
            f"""
You are a Kubernetes assistant. Your job is to:
- Convert user instructions into kubectl commands
- Ask questions if more details (like pod name or namespace) are needed
- Only return the final command after getting complete info
- Do not assume names unless explicitly provided

Now handle this:
User: "{user_input}"
"""
        )
        return response.text.strip()
    except Exception as e:
        return f"error: {str(e)}"
   
    