"""
Configuration for the Deathroll Game Factory.
Centralized settings, paths, and constants.
"""

import os
from pathlib import Path

# ===== Paths =====
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
DOCS_DIR = BASE_DIR / "docs"
TEMPLATES_DIR = BASE_DIR / "templates"
SCRIPTS_DIR = BASE_DIR / "scripts"

# ===== API Keys (from GitHub Secrets) =====
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# OPENAI_API_KEY is not used – safe to remove from GitHub Secrets
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL = "@deathrollprod"

# ===== Factory Settings =====
AUTO_APPROVE_WAIT_MINUTES = 5      # Wait for manual approval before auto‑proceeding
MAX_RETRIES = 3
SLEEP_BETWEEN_RETRIES = 10

# ===== Game Genres =====
SUPPORTED_GENRES = ["shooter", "soccer", "racing", "platformer", "puzzle", "rpg"]

# ===== Image Generation =====
POLLINATIONS_BASE_URL = "https://image.pollinations.ai/prompt"
FALLBACK_IMAGE_SIZE = (512, 512)
DEFAULT_PROMO_COLOR = "#2c3e50"

# ===== GitHub Pages Settings =====
# These are automatically set by Actions, but you can override them
REPO_OWNER = os.getenv("GITHUB_REPOSITORY_OWNER", "your-username")
REPO_NAME = os.getenv("GITHUB_REPOSITORY", "").split("/")[-1]
PUBLIC_BASE_URL = f"https://{REPO_OWNER}.github.io/{REPO_NAME}"
