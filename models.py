import re
import json
import logging
from typing import Dict, List, Any, Optional
import google.generativeai as genai
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

import config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global cache for local models to enable lazy-loading
_local_model = None
_local_tokenizer = None

# Initialize Gemini Client if API key is present
gemini_initialized = False
if config.GEMINI_API_KEY:
    try:
        genai.configure(api_key=config.GEMINI_API_KEY)
        gemini_initialized = True
        logger.info("Google Gemini SDK configured successfully.")
    except Exception as e:
        logger.error(f"Failed to configure Gemini SDK: {e}")
else:
    logger.warning("GEMINI_API_KEY not found. Gemini services will be unavailable until a key is provided.")


def get_gemini_model():
    """Returns the initialized Gemini model instance."""
    if not gemini_initialized:
        raise ValueError("Gemini API key is not configured. Please add GEMINI_API_KEY to your .env file.")
    return genai.GenerativeModel(config.GEMINI_MODEL_NAME)


def generate_gemini_content(prompt: str) -> str:
    """Helper to generate content using Gemini with error handling."""
    try:
        model = get_gemini_model()
        response = model.generate_content(prompt)
        if not response or not response.text:
            raise ValueError("Empty response received from Gemini API.")
        return response.text
    except Exception as e:
        logger.error(f"Gemini generation error: {e}")
        raise e


def load_local_model():
    """Lazy-loads the local tokenizer and model on CPU."""
    global _local_model, _local_tokenizer
    if _local_model is None or _local_tokenizer is None:
        logger.info(f"Loading local model '{config.LAMINI_MODEL_NAME}' and tokenizer...")
        try:
            _local_tokenizer = AutoTokenizer.from_pretrained(config.LAMINI_MODEL_NAME)
            _local_model = AutoModelForSeq2SeqLM.from_pretrained(config.LAMINI_MODEL_NAME)
            logger.info("Local model and tokenizer loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load local model/tokenizer: {e}")
            raise e


def generate_local_content(prompt: str, max_length: int = 256) -> str:
    """Generates content using the local LaMini-Flan-T5 model."""
    try:
        load_local_model()
        logger.info("Generating content using local model...")
        
        # Tokenize prompt
        inputs = _local_tokenizer(prompt, return_tensors="pt")
        
        # Generate output (sampling is enabled)
        with torch.no_grad():
            outputs = _local_model.generate(
                **inputs,
                max_length=max_length,
                do_sample=True,
                temperature=0.7,
                num_return_sequences=1
            )
            
        generated_text = _local_tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text
    except Exception as e:
        logger.error(f"Local model inference error: {e}")
        raise e


def clean_json_string(text: str) -> str:
    """Cleans markdown wrappers or extra characters from JSON strings before parsing."""
    text = text.strip()
    
    # Remove markdown code block fences if present
    # e.g., ```json [ ... ] ``` or ``` [ ... ] ```
    code_block_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if code_block_match:
        text = code_block_match.group(1).strip()
        
    # If the text has characters before [ or after ], find the actual array boundaries
    array_match = re.search(r"(\[[\s\S]*\])", text)
    if array_match:
        text = array_match.group(1).strip()
        
    return text


def parse_quiz_json(raw_text: str) -> List[Dict[str, Any]]:
    """Cleans and parses the generated quiz raw text into a valid JSON array."""
    cleaned = clean_json_string(raw_text)
    try:
        quiz_data = json.loads(cleaned)
        if not isinstance(quiz_data, list):
            raise ValueError("Quiz data must be a JSON array.")
        
        # Validate format of each item
        validated_quiz = []
        for index, item in enumerate(quiz_data):
            # Check structure
            question = item.get("question", f"Question {index + 1}")
            options = item.get("options", ["Option A", "Option B", "Option C", "Option D"])
            
            # Ensure exactly 4 options
            while len(options) < 4:
                options.append(f"Option {len(options) + 1}")
            options = options[:4]
            
            correct_option = item.get("correct_option", 0)
            try:
                correct_option = int(correct_option)
                if correct_option < 0 or correct_option > 3:
                    correct_option = 0
            except (ValueError, TypeError):
                correct_option = 0
                
            explanation = item.get("explanation", "No explanation provided.")
            
            validated_quiz.append({
                "id": index + 1,
                "question": question,
                "options": options,
                "correct_option": correct_option,
                "explanation": explanation
            })
            
        return validated_quiz
    except Exception as e:
        logger.error(f"JSON parsing error for raw output: {raw_text}. Error: {e}")
        # Return a fallback quiz item so the app does not break
        return [{
            "id": 1,
            "question": "Failed to generate quiz properly. Would you like to try again?",
            "options": ["Try Again", "Go to Dashboard", "Read Help", "Contact Support"],
            "correct_option": 0,
            "explanation": f"The raw text could not be parsed: {str(e)}"
        }]
