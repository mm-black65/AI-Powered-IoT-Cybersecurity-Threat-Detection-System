import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Gemini model
model = genai.GenerativeModel("gemini-3.5-flash")

def generate_security_analysis(
    attack,
    confidence,
    telemetry,
    rag_information
):

    prompt = f"""
You are an AI Cybersecurity Expert.

Prediction:
{attack}

Confidence:
{confidence:.2f}%

Live Device Data:
{telemetry}

Knowledge Base Information:
{rag_information}

Using ONLY the above information,

Explain:

1. What attack is happening?
2. Why is it dangerous?
3. How severe is it?
4. Recommended mitigation.
5. Should the administrator take immediate action?

Keep the answer professional but easy to understand.
"""

    response = model.generate_content(prompt)

    return response.text