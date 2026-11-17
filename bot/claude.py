
from anthropic import AsyncAnthropic

from bot.config import (
    ANTHROPIC_API_KEY,
    CLAUDE_MODEL,
    SYSTEM_PROMPT,
    MAX_OUTPUT_TOKENS
)


client = AsyncAnthropic(
    api_key=ANTHROPIC_API_KEY,
    timeout=180.0,
    max_retries=3
)


async def ask_claude(history):
    response = await client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=MAX_OUTPUT_TOKENS,
        system=SYSTEM_PROMPT,
        messages=history
    )

    return "\n".join(
        block.text
        for block in response.content
        if block.type == "text"
    )
