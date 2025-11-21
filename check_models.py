import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found in .env file")
else:
    print(f"API Key found: {api_key[:5]}...******")
    try:
        genai.configure(api_key=api_key)
        print("\nListing available models for this key...")
        found = False
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"   - {m.name}")
                found = True
        if not found:
            print("No models found that support 'generateContent'. Check if 'Generative Language API' is enabled in Google Cloud Console.")
    except Exception as e:
        print(f"Connection Error: {e}")