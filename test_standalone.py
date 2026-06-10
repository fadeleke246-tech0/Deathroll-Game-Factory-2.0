#!/usr/bin/env python3
"""Standalone test – no imports from scripts/"""
import os
import sys
import requests

print("=== Starting standalone test ===")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Files here: {os.listdir('.')}")

# Test 1: Environment variables
print("\n--- Environment variables ---")
for key in ["GEMINI_API_KEY", "TELEGRAM_BOT_TOKEN", "TELEGRAM_ADMIN_CHAT_ID"]:
    val = os.getenv(key)
    if val:
        # Mask most of the key for security
        masked = val[:5] + "..." + val[-4:] if len(val) > 10 else "***"
        print(f"{key}: {masked} (length {len(val)})")
    else:
        print(f"{key}: MISSING")

# Test 2: Import requests and PIL
print("\n--- Testing imports ---")
try:
    import requests
    print("✅ requests imported")
except Exception as e:
    print(f"❌ requests import failed: {e}")

try:
    from PIL import Image
    print("✅ PIL imported")
except Exception as e:
    print(f"❌ PIL import failed: {e}")

# Test 3: Gemini API call (if key present)
gemini_key = os.getenv("GEMINI_API_KEY")
if gemini_key:
    print("\n--- Testing Gemini API ---")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
    payload = {"contents": [{"parts": [{"text": "Say 'Hello Deathroll Factory' in one word."}]}]}
    try:
        resp = requests.post(url, json=payload, timeout=30)
        print(f"Status code: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            print(f"✅ Gemini response: {text}")
        else:
            print(f"❌ Gemini error: {resp.text[:200]}")
    except Exception as e:
        print(f"❌ Exception: {e}")

# Test 4: Telegram (send a simple message)
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
admin_id = os.getenv("TELEGRAM_ADMIN_CHAT_ID")
if bot_token and admin_id:
    print("\n--- Testing Telegram ---")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": admin_id, "text": "🧪 Deathroll Factory standalone test successful!"}
    try:
        resp = requests.post(url, json=payload, timeout=30)
        print(f"Telegram status: {resp.status_code}")
        if resp.status_code == 200:
            print("✅ Message sent to your DM")
        else:
            print(f"❌ Failed: {resp.text[:100]}")
    except Exception as e:
        print(f"❌ Exception: {e}")

print("\n=== Test finished ===")
