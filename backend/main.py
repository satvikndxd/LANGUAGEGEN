"""FastAPI backend for the language generation system."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from language_core.config import load_config
from language_core.phonology import PhonologyGenerator

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranslationRequest(BaseModel):
    text: str

# Store active languages
active_languages = {}

@app.get("/")
async def root():
    return {"message": "Language Generator API is running"}

@app.post("/api/create-language")
async def create_language():
    """Create a new language and return its characteristics."""
    try:
        config = load_config()
        generator = PhonologyGenerator(config)
        
        # Generate some example words
        example_words = [generator.generate_word() for _ in range(5)]
        
        # Create a unique ID for this language
        import uuid
        language_id = str(uuid.uuid4())
        
        # Store the generator
        active_languages[language_id] = generator
        
        # Get all phonemes (both consonants and vowels)
        all_phonemes = [str(p) for p in generator.consonants + generator.vowels]
        
        return {
            "id": language_id,
            "phonemes": all_phonemes,
            "syllable_structure": generator.syllable_structure,
            "example_words": example_words
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/translate/{language_id}")
async def translate_text(language_id: str, request: TranslationRequest):
    """Translate English text into the constructed language."""
    if language_id not in active_languages:
        return {"error": "Language not found"}
    
    try:
        generator = active_languages[language_id]
        
        # Split the text into words
        words = request.text.strip().lower().split()
        
        # Generate a unique word for each English word
        translated_words = [generator.generate_word() for _ in words]
        
        return {
            "original": request.text,
            "translated": " ".join(translated_words),
            "word_mapping": dict(zip(words, translated_words))
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("Starting server on http://127.0.0.1:9000")
    import logging
    logging.basicConfig(level=logging.DEBUG)
    uvicorn.run(app, host="127.0.0.1", port=9000, workers=1, log_level="debug")
