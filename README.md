# EduGenie

EduGenie is a lightweight AI-powered educational assistant built with FastAPI. It supports:

- Q&A for educational questions
- Concept explanations by level
- Quiz generation by topic and difficulty
- Text summarization
- Personalized learning roadmap recommendations

## Tech Stack

- FastAPI
- Jinja2 templates
- Google Gemini API (optional, for premium features)
- Local LaMini-Flan-T5 model (fallback/local tasks)

## Project Structure

- `main.py` - FastAPI app and API routes
- `models.py` - model integration and inference logic
- `prompts.py` - prompt templates
- `config.py` - runtime configuration
- `templates/` - HTML templates
- `static/` - CSS and JavaScript assets

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file (optional for Gemini features):

```env
GEMINI_API_KEY=your_api_key
GEMINI_MODEL_NAME=gemini-1.5-flash
```

## Run

```bash
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000` in your browser.
