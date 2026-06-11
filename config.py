import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
DOCS_DIR = BASE_DIR / "docs"
TEMPLATES_DIR = BASE_DIR / "templates"
SCRIPTS_DIR = BASE_DIR / "scripts"

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Factory settings
AUTO_APPROVE_WAIT_MINUTES = 5
PUBLIC_BASE_URL = f"https://{os.getenv('GITHUB_REPOSITORY_OWNER', 'fadeleke246-tech0')}.github.io/{os.getenv('GITHUB_REPOSITORY', 'Deathroll-Game-Factory-2.0').split('/')[-1]}"
