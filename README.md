# EduGenie - AI-Powered Educational Assistant

EduGenie is an end-to-end educational assistant that combines a cloud LLM (Google Gemini) with a local fallback model (LaMini-Flan-T5) to deliver reliable learning support through a FastAPI web application.

It is designed to stay usable even when premium API access is unavailable by routing supported tasks to a local model.

## What It Does

EduGenie provides five core learning workflows:

- Answers academic questions with cloud or local inference
- Explains concepts at multiple learner levels (Child, Teenager, College Student, Expert)
- Generates multiple-choice quizzes by topic and difficulty
- Summarizes educational text locally
- Recommends personalized learning roadmaps

## Problem Statement

Students often switch between multiple disconnected tools for asking questions, simplifying concepts, practicing with quizzes, and planning what to learn next. This slows down learning and creates inconsistent quality.

EduGenie solves this by offering a single assistant with two practical goals:

- Keep responses accessible and helpful across different learner levels
- Remain available with local inference when cloud AI is not configured

### User Perspectives

- A student wants quick, understandable explanations without searching across many websites.
- A self-learner wants practice quizzes and a clear roadmap for progressing from beginner to advanced.
- An educator wants a fast assistant to generate structured study material and summaries.

## Key Features

- Hybrid AI runtime: Gemini for premium capabilities plus local LaMini-Flan-T5 fallback
- Graceful degradation: core features still run without an API key
- Structured API design using Pydantic request models and validation
- JSON-safe quiz parsing with fallback protection for malformed model output
- Simple UI served with Jinja2 templates and static assets

## System Approach

EduGenie uses two inference paths:

- Cloud path (Gemini): used for high-quality generation tasks such as explanation, quiz generation, and roadmap recommendations
- Local path (LaMini-Flan-T5): used for summarization and fallback Q&A when Gemini is unavailable

At runtime, the app reloads environment values and can reconfigure the Gemini client on the fly, allowing key/model updates without restarting development flow.

## Technology Stack

| Layer | Technology | Why It Is Used |
|---|---|---|
| Web API | FastAPI, Uvicorn | Fast async API development with strong validation |
| UI Rendering | Jinja2 Templates, HTML/CSS/JS | Lightweight dashboard with no frontend build pipeline |
| Cloud AI | google-generativeai (Gemini) | High-quality educational generation |
| Local AI | transformers, torch (LaMini-Flan-T5) | Offline-capable and fallback inference |
| Config | python-dotenv | Runtime environment configuration |

## Repository Structure

```text
4.uma/
|- README.md
|- requirements.txt
|- .gitignore
|- config.py
|- prompts.py
|- models.py
|- main.py
|- templates/
|  \- index.html
|- static/
|  |- css/
|  |  \- style.css
|  \- js/
|     \- app.js
|- EduGenie_Project_Report_and_Viva_Guide.docx
\- EduGenie_Viva_Presentation.pptx
```

## API Overview

- GET / : dashboard page
- GET /api/status : health/status of Gemini and local model
- POST /api/qa : question answering (cloud or local)
- POST /api/explain : level-based concept explanation (Gemini)
- POST /api/quiz : quiz generation (Gemini + JSON normalization)
- POST /api/summarize : local summarization
- POST /api/recommend : personalized learning roadmap (Gemini)

## Local Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies.

```bash
pip install -r requirements.txt
```

4. Create a .env file in the project root.

```env
GEMINI_API_KEY=your_api_key
GEMINI_MODEL_NAME=gemini-1.5-flash
LAMINI_MODEL_NAME=MBZUAI/LaMini-Flan-T5-77M
HOST=127.0.0.1
PORT=8000
DEBUG=True
```

5. Run the application.

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Open http://127.0.0.1:8000 in your browser.

## Example Workflows

- Ask a question and force local inference when needed.
- Explain a concept for a specific level such as Teenager or College Student.
- Generate a quiz with custom topic, question count, and difficulty.
- Summarize a long educational paragraph with local processing.
- Request a structured roadmap for a new subject.

## Reliability Notes

- If GEMINI_API_KEY is not set, Gemini-only endpoints will return clear validation errors.
- Q&A and summarization can still work via local model inference.
- Quiz output is sanitized and validated before returning to the client.

## Documentation Assets

This repository also includes submission-ready project artifacts:

- EduGenie_Project_Report_and_Viva_Guide.docx
- EduGenie_Viva_Presentation.pptx

## Future Enhancements

- Add user accounts and learning history
- Persist quiz results and progress analytics
- Add streaming responses for faster perceived latency
- Add unit/integration tests and CI workflow
- Deploy with containerized production configuration
