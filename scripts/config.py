import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
DOCS_DIR = BASE_DIR / "docs"
TEMPLATES_DIR = BASE_DIR / "templates"
SCRIPTS_DIR = BASE_DIR / "scripts"

# Ensure directories exist
for dir_path in [DATA_DIR, OUTPUT_DIR, DOCS_DIR, TEMPLATES_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL = os.getenv("TELEGRAM_CHANNEL", "@deathrollprod")
TELEGRAM_ADMIN_CHAT_ID = os.getenv("TELEGRAM_ADMIN_CHAT_ID")

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 10

REPO_OWNER = os.getenv("GITHUB_REPOSITORY_OWNER", "fadeleke246-tech0")
REPO_NAME = os.getenv("GITHUB_REPOSITORY", "Deathroll-Game-Factory-2.0").split("/")[-1]
PUBLIC_BASE_URL = f"https://{REPO_OWNER}.github.io/{REPO_NAME}"
