"""
Utility functions: LLM calling with fallback (Gemini -> Groq), JSON extraction,
image generation, file I/O, Telegram messaging, and Git operations.
"""
import json
import re
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any

import requests
from google import genai  # new package
from google.genai import types
import groq
from PIL import Image, ImageDraw

import config

# ---------- LLM with fallback (Gemini -> Groq) ----------
_groq_client = groq.Groq(api_key=config.GROQ_API_KEY) if config.GROQ_API_KEY else None

# Gemini client (new style)
_gemini_client = genai.Client(api_key=config.GEMINI_API_KEY) if config.GEMINI_API_KEY else None
GEMINI_MODEL = "gemini-2.0-flash-lite"

def call_llm(prompt: str, max_retries: int = config.MAX_RETRIES) -> str:
    """
    Try Gemini (new genai.Client) first, then Groq. Raises exception if all fail.
    """
    errors = []
    # Gemini
    if _gemini_client:
        for attempt in range(max_retries):
            try:
                response = _gemini_client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt,
                    config=types.GenerateContentConfig(temperature=0.5)
                )
                return response.text
            except Exception as e:
                errors.append(f"Gemini attempt {attempt+1}: {e}")
                time.sleep(config.RETRY_DELAY_SECONDS)
    else:
        errors.append("Gemini API key missing or client not initialized")
    # Groq
    if _groq_client:
        for attempt in range(max_retries):
            try:
                completion = _groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                )
                return completion.choices[0].message.content
            except Exception as e:
                errors.append(f"Groq attempt {attempt+1}: {e}")
                time.sleep(config.RETRY_DELAY_SECONDS)
    else:
        errors.append("Groq API key missing")
    raise Exception(f"All LLM providers failed:\n" + "\n".join(errors))

# ---------- JSON extraction (unchanged) ----------
def extract_json_from_text(text: str) -> Optional[Dict]:
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        text = match.group(1)
    else:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            text = text[start:end+1]
        else:
            return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None

# ---------- Image generation ----------
def generate_image(prompt: str, output_path: Path) -> bool:
    try:
        encoded = requests.utils.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024"
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(resp.content)
            return True
    except Exception as e:
        print(f"Pollinations error: {e}")
    img = Image.new("RGB", (512,512), color="#2c3e50")
    draw = ImageDraw.Draw(img)
    draw.text((256,256), prompt[:50], fill="white", anchor="mm")
    img.save(output_path)
    return True

# ---------- File I/O ----------
def load_json(path: Path) -> Dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except:
        return {}

def save_json(data: Any, path: Path) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return True

# ---------- Git ----------
def commit_and_push(message: str, paths: List[str]) -> None:
    subprocess.run(["git", "add"] + paths, check=False)
    subprocess.run(["git", "commit", "-m", message], check=False)
    subprocess.run(["git", "push"], check=False)

# ---------- Telegram ----------
def send_telegram_message(text: str) -> bool:
    if not config.TELEGRAM_BOT_TOKEN:
        return False
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": config.TELEGRAM_CHANNEL, "text": text, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, json=payload, timeout=10)
        return r.status_code == 200
    except:
        return False
