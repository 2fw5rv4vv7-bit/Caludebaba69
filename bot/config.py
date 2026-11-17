
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

# Premium Claude model
CLAUDE_MODEL = os.getenv(
    "CLAUDE_MODEL",
    "claude-fable-5-2"
)

DATABASE_URL = os.getenv("DATABASE_URL", "")

SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    """You are a highly capable Claude AI assistant
inside Telegram.

Be intelligent, accurate, helpful, thoughtful,
and detailed when necessary.

Help with programming, research, writing,
reasoning, mathematics, and general questions.

Never invent facts. Clearly communicate uncertainty.
Format answers using Telegram-compatible Markdown."""
)

MAX_OUTPUT_TOKENS = int(
    os.getenv("MAX_OUTPUT_TOKENS", "8192")
)

# Optional owner-controlled access restriction.
ALLOWED_USER_IDS = {
    int(x.strip())
    for x in os.getenv("ALLOWED_USER_IDS", "").split(",")
    if x.strip()
}
