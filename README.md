
# Premium Claude Telegram AI

A Telegram AI assistant powered exclusively by
Anthropic Claude.

## Features
- Claude premium model
- Persistent PostgreSQL memory
- Conversation history
- Telegram commands
- Railway deployment

## Environment Variables

BOT_TOKEN=
ANTHROPIC_API_KEY=
DATABASE_URL=
CLAUDE_MODEL=claude-fable-5-2
MAX_OUTPUT_TOKENS=8192
SYSTEM_PROMPT=
ALLOWED_USER_IDS=

## Start

python -m bot.main
