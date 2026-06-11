import json
import re
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any

import requests
import google.generativeai as genai
import groq
from PIL import Image, ImageDraw

import config

# ---------- LLM with fallback ----------
groq_client = groq.Groq(api_key=config.GROQ_API_KEY) if config.GROQ_API_KEY else None

def call_llm_with_fallback(
    prompt: str,
    gemini_model: str = "gemini-1.5-flash",
    groq_model: str = "mixtral-8x7b-32768",
    max_retries: int = 2,
) -> str:
    errors = []
    # Gemini
    if config.GEMINI_API_KEY:
        for attempt in range(max_retries):
            try:
                genai.configure(api_key=config.GEMINI_API_KEY)
                model = genai.GenerativeModel(gemini_model)
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                errors.append(f"Gemini attempt {attempt+1}: {e}")
                time.sleep(2)
    else:
        errors.append("Gemini key missing")
    # Groq
    if groq_client:
        for attempt in range(max_retries):
            try:
                completion = groq_client.chat.completions.create(
                    model=groq_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                )
                return completion.choices[0].message.content
            except Exception as e:
                errors.append(f"Groq attempt {attempt+1}: {e}")
                time.sleep(2)
    else:
        errors.append("Groq key missing")
    raise Exception(f"All LLMs failed:\n" + "\n".join(errors))

# ---------- JSON extraction ----------
def extract_json_from_text(text: str) -> Optional[Dict]:
    match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
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
        url = f"https://image.pollinations.ai/prompt/{encoded}?width=512&height=512"
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(resp.content)
            return True
    except Exception:
        pass
    # Fallback coloured image
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
        return json.loads(path.read_text())
    except:
        return {}

def save_json(data: Any, path: Path) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))
    return True

# ---------- Git ----------
def commit_and_push(message: str, paths: List[str]):
    subprocess.run(["git", "add"] + paths, check=False)
    subprocess.run(["git", "commit", "-m", message], check=False)
    subprocess.run(["git", "push"], check=False)
