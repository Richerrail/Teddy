#!/usr/bin/env python3
"""
Secure Messenger Telegram Bot.
Encrypts and decrypts messages using the secure_messenger module.
"""

import os
import logging
import sys

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from secure_messenger import encrypt_message, decrypt_message

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message."""
    await update.message.reply_text(
        "🔐 *Secure Messenger Bot*\n\n"
        "Commands:\n"
        "`/encrypt <message>` - Encrypt a message\n"
        "`/decrypt <encrypted>` - Decrypt a message\n"
        "Or just send me a message to encrypt it.",
        parse_mode="Markdown",
    )


async def encrypt_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Encrypt a message from command args."""
    if not context.args:
        await update.message.reply_text(
            "Usage: `/encrypt <your secret message>`",
            parse_mode="Markdown",
        )
        return

    message = " ".join(context.args)
    try:
        encrypted = encrypt_message(message)
        await update.message.reply_text(
            f"🔒 *Encrypted:*\n`{encrypted}`",
            parse_mode="Markdown",
        )
    except Exception as e:
        logger.error(f"Encryption error: {e}")
        await update.message.reply_text("❌ Encryption failed.")


async def decrypt_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Decrypt a message from command args."""
    if not context.args:
        await update.message.reply_text(
            "Usage: `/decrypt <encrypted text>`",
            parse_mode="Markdown",
        )
        return

    encrypted = " ".join(context.args)
    try:
        decrypted = decrypt_message(encrypted)
        await update.message.reply_text(
            f"🔓 *Decrypted:*\n`{decrypted}`",
            parse_mode="Markdown",
        )
    except ValueError:
        await update.message.reply_text(
            "❌ Decryption failed. This bot is required for decryption.",
        )
    except Exception as e:
        logger.error(f"Decryption error: {e}")
        await update.message.reply_text("❌ Decryption failed.")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Encrypt any plain text message received."""
    message = update.message.text
    try:
        encrypted = encrypt_message(message)
        await update.message.reply_text(
            f"🔒 *Encrypted:*\n`{encrypted}`\n\n"
            "Send me the encrypted text with `/decrypt` to decrypt it.",
            parse_mode="Markdown",
        )
    except Exception as e:
        logger.error(f"Encryption error: {e}")
        await update.message.reply_text("❌ Encryption failed.")


def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        print(
            "Error: TELEGRAM_BOT_TOKEN environment variable not set.\n"
            "Get your token from @BotFather on Telegram.",
            file=sys.stderr,
        )
        sys.exit(1)

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("encrypt", encrypt_cmd))
    application.add_handler(CommandHandler("decrypt", decrypt_cmd))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Detect if running on Render (web service) or locally
    render_url = os.environ.get("RENDER_EXTERNAL_URL")
    if render_url:
        port = int(os.environ.get("PORT", 10000))
        webhook_url = f"{render_url}/webhook"
        logger.info(f"Starting webhook on port {port}, URL: {webhook_url}")
        application.run_webhook(
            listen="0.0.0.0",
            port=port,
            webhook_url=webhook_url,
        )
    else:
        logger.info("Bot started in polling mode. Press Ctrl+C to stop.")
        application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
