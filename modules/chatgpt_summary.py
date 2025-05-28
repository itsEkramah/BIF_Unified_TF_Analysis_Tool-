# modules/chatgpt_summary.py

import os
from dotenv import load_dotenv
import openai
import wikipedia

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if openai.api_key is None:
    raise Exception("❌ OPENAI_API_KEY is missing. Add it to your .env file.")

def get_chatgpt_summary(tf_name):
    """
    Generates a biological summary of the transcription factor using ChatGPT.
    """
    prompt = (
        f"Provide a detailed biological summary of the human transcription factor '{tf_name}'. "
        f"Include known functions, regulatory role, binding domains, and disease associations."
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=300
        )
        summary = response.choices[0].message.content.strip()
        print("[Summary] ChatGPT summary received.")
        return summary
    except Exception as e:
        print(f"[Summary] ChatGPT error: {e}")
        return None

def get_tf_summary(tf_name):
    """
    Returns TF summary using ChatGPT or falls back to Wikipedia.
    """
    print(f"[Summary] Looking up TF: {tf_name}")
    chatgpt_summary = get_chatgpt_summary(tf_name)

    if chatgpt_summary:
        return chatgpt_summary

    print("[Summary] Falling back to Wikipedia...")
    try:
        return wikipedia.summary(tf_name, sentences=2)
    except Exception as e:
        print(f"[Summary] Wikipedia error: {e}")
        return "No summary available."
