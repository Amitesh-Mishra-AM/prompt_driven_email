import os
import google.generativeai as genai
import json
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

CACHED_MODEL_NAME = None

def configure_llm():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except:
            raise ValueError("GEMINI_API_KEY not found in .env or Streamlit Secrets")
    genai.configure(api_key=api_key)

def get_active_model_name():
    global CACHED_MODEL_NAME
    if CACHED_MODEL_NAME:
        return CACHED_MODEL_NAME
    configure_llm()
    # Priority list: We prefer Flash (fast/high quota) -> Pro (stable)
    # We avoid "experimental" models if possible as they have low limits
    preferred_keywords = ["flash", "gemini-pro", "gemini-1.5-pro"]
    try:
        print("🔍 Scanning for available Gemini models...")
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)

        if not available_models:
            return "models/gemini-pro" # Fallback default
        # 1. Try to find a preferred model in the list
        for keyword in preferred_keywords:
            for model_name in available_models:
                if keyword in model_name and "exp" not in model_name:
                    print(f"✅ Auto-selected model: {model_name}")
                    CACHED_MODEL_NAME = model_name
                    return model_name
        # 2. If no preferred model found, take the first available one
        first_available = available_models[0]
        print(f"⚠️ Using fallback model: {first_available}")
        CACHED_MODEL_NAME = first_available
        return first_available
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        return "models/gemini-pro"


def get_gemini_response(prompt_text):
    try:
        model_name = get_active_model_name()
        model = genai.GenerativeModel(model_name) 
        response = model.generate_content(prompt_text)
        return response.text.strip()
    except Exception as e:
        if "429" in str(e):
            return "Error: Rate limit exceeded. Please wait."
        return f"Error accessing Gemini: {str(e)}"


def process_email_with_llm(email_body, prompt_template):
    full_prompt = f"{prompt_template}\n\nEMAIL CONTENT:\n{email_body}"
    return get_gemini_response(full_prompt)



def parse_json_output(response_text):
    clean_text = response_text.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(clean_text)
    except json.JSONDecodeError:
        return {"task": None, "deadline": None, "raw_error": clean_text}