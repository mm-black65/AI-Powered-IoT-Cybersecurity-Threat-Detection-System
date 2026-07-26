import os
from dotenv import load_dotenv

load_dotenv()  # expects a .env file with GEMINI_API_KEY=... or GOOGLE_API_KEY=...

if not os.getenv("GEMINI_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
    raise EnvironmentError(
        "No Gemini API key found in environment. "
        "Create a .env file with GEMINI_API_KEY=your_key_here"
    )

from backend.llm_service import generate_security_analysis

sample_telemetry = {
    "temperature": 31,
    "cpu_usage": 42,
    "packet_rate": 180,
    "failed_login": 3,
    "wifi_signal": -58,
}

try:
    result = generate_security_analysis(
        "DDoS-TCP_Flood",   # prediction
        99.96,              # confidence
        "HIGH",             # threat_level
        sample_telemetry,   # telemetry dict
    )

    print("LLM call succeeded.\n")
    print(result)

except Exception as e:
    print("LLM call failed.")
    print(f"Error: {e}")
    print("\nCheck: is the API key valid? Is backend/llm_service.py implemented "
          "and returning a string/dict as expected by app.py's 'ai_analysis' field?")