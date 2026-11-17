
import asyncio

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ChatAction

from bot.claude import ask_claude
from bot.config import (
    CLAUDE_MODEL,
    ALLOWED_USER_IDS
)

router = Router()


def is_allowed(user_id):
    return (
        not ALLOWED_USER_IDS
        or user_id in ALLOWED_USER_IDS
    )


async def send_long_message(message, text):
    # Keep messages safely below Telegram's limit.
    while text:
        chunk = text[:4000]

        if len(text) > 4000:
            split_at = chunk.rfind("\n")
            if split_at > 1000:
                chunk = text[:split_at]

        await message.answer(chunk)
        text = text[len(chunk):]


@router.message(Command("start"))
async def start(message: Message):
    if not is_allowed(message.from_user.id):
        return

    await message.answer(
        "Welcome to Premium Claude AI!\n\n"
        "I am powered exclusively by Claude.\n\n"
        "Send me a message to start chatting.\n\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/reset - Clear your conversation\n"
        "/model - Show active Claude model"
    )


@router.message(Command("model"))
async def model(message: Message):
    if not is_allowed(message.from_user.id):
        return

    await message.answer(
        f"Active AI: Claude\n"
        f"Model: {CLAUDE_MODEL}"
    )


@router.message(Command("reset"))
async def reset(message: Message, memory):
    if not is_allowed(message.from_user.id):
        return

    await memory.reset(message.from_user.id)

    await message.answer(
        "Your conversation history has been cleared."
    )


@router.message()
async def chat(message: Message, memory):
    if not is_allowed(message.from_user.id):
        return

    if not message.text:
        await message.answer(
            "For now, please send a text message."
        )
        return

    user_id = message.from_user.id
    question = message.text.strip()

    if not question:
        return

    if len(question) > 30000:
        await message.answer(
            "That message is too long. Please shorten it."
        )
        return

    await memory.add(user_id, "user", question)

    history = await memory.get_history(
        user_id,
        limit=20
    )

    try:
        await message.bot.send_chat_action(
            message.chat.id,
            ChatAction.TYPING
        )

        answer = await ask_claude(history)

        if not answer:
            answer = "Claude returned an empty response."

        await memory.add(user_id, "assistant", answer)

        await send_long_message(message, answer)

    except Exception:
        # Log detailed errors privately in Railway logs.
        import logging
        logging.exception("Claude request failed")

        await message.answer(
            "Sorry, Claude could not process that request. "
            "Please try again shortly."
        )
