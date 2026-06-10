import os

# ========== TELEGRAM ==========
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_ADMIN_CHAT_ID = os.getenv("TELEGRAM_ADMIN_CHAT_ID")   # Your DM
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")         # @drolltech

# ========== AI APIs ==========
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Fix common typo: OPENA_API_KEY -> OPENAI_API_KEY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("OPENA_API_KEY")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")   # optional fallback

# ========== GitHub ==========
# Use GH_TOKEN if provided, else fallback to GITHUB_TOKEN (auto-set by Actions)
GITHUB_TOKEN = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")

# ========== Paths ==========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# ========== Game Queue ==========
GAMES_QUEUE_FILE = os.path.join(DATA_DIR, "games_queue.json")
PORTFOLIO_FILE = os.path.join(DATA_DIR, "portfolio.json")
RUN_STATE_FILE = os.path.join(DATA_DIR, "run_state.json")
SAR_FILE = os.path.join(DATA_DIR, "sar_analysis.json")

# ========== Phase Delays (minutes) ==========
AUTO_APPROVE_WAIT_MINUTES = 60   # after Day 1 report, auto-approve if no /approve
