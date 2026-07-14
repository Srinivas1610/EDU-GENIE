import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Gemini Config
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-flash")

# Local Model Config
LAMINI_MODEL_NAME = os.getenv("LAMINI_MODEL_NAME", "MBZUAI/LaMini-Flan-T5-77M")

# Application Settings
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
