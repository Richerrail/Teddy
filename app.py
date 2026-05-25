#!/usr/bin/env python3
"""
Discord Protect Bot - Flask Web Server
Serves the Telegram Mini App and API endpoints.
"""

import json
import logging
import os
import sys

from flask import Flask, request, send_from_directory, jsonify
from telegram import Update, WebAppInfo, KeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes

from secure_messenger import encrypt_message, decrypt_message

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# CORS and security headers for Telegram WebView
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'ALLOWALL'
    return response

# Telegram bot token
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    print("Error: TELEGRAM_BOT_TOKEN not set", file=sys.stderr)
    sys.exit(1)

# Website URL for Mini App - auto-detect on Render
WEB_URL = os.environ.get("RENDER_EXTERNAL_URL")
if not WEB_URL:
    # Try to detect from Render environment
    render_service = os.environ.get("RENDER_SERVICE_NAME")
    if render_service:
        WEB_URL = f"https://{render_service}.onrender.com"
    elif os.environ.get("RENDER_EXTERNAL_HOSTNAME"):
        WEB_URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}"
    else:
        WEB_URL = "http://localhost:5000"

logger.info(f"Mini App URL: {WEB_URL}")

# Build Telegram Application (same as before but for webhook + commands)
application = Application.builder().token(TOKEN).build()


# ---------- Handlers ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🔐 *Secure Messenger Bot*\n\n"
        "Use the button below to open the secure messenger app.\n\n"
        "Or use commands:\n"
        "`/encrypt <message>`\n"
        "`/decrypt <encrypted>`",
        parse_mode="Markdown",
    )


async def open_app(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Open the Mini App via inline keyboard button."""
    await update.message.reply_text(
        "🚀 Open the Secure Messenger app:",
        reply_markup={
            "inline_keyboard": [[
                {
                    "text": "🔐 Open Secure Messenger",
                    "web_app": {"url": f"{WEB_URL}/"}
                }
            ]]
        },
    )


async def encrypt_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: `/encrypt <message>`")
        return
    message = " ".join(context.args)
    try:
        encrypted = encrypt_message(message)
        await update.message.reply_text(f"🔒 *Encrypted:*\n`{encrypted}`", parse_mode="Markdown")
    except Exception:
        await update.message.reply_text("❌ Encryption failed.")


async def decrypt_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: `/decrypt <encrypted>`")
        return
    encrypted = " ".join(context.args)
    try:
        decrypted = decrypt_message(encrypted)
        await update.message.reply_text(f"🔓 *Decrypted:*\n`{decrypted}`", parse_mode="Markdown")
    except Exception:
        await update.message.reply_text("❌ Decryption failed.")


# Register handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("app", open_app))
application.add_handler(CommandHandler("encrypt", encrypt_cmd))
application.add_handler(CommandHandler("decrypt", decrypt_cmd))


# ---------- Flask Routes ----------
@app.route("/api/encrypt", methods=["POST"])
def api_encrypt():
    data = request.get_json(force=True)
    text = data.get("text", "")
    if not text:
        return jsonify({"detail": "Missing text"}), 400
    try:
        result = encrypt_message(text)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"detail": str(e)}), 500


@app.route("/api/decrypt", methods=["POST"])
def api_decrypt():
    data = request.get_json(force=True)
    text = data.get("text", "")
    if not text:
        return jsonify({"detail": "Missing text"}), 400
    try:
        result = decrypt_message(text)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"detail": str(e)}), 500


@app.route("/", methods=["GET"])
def index():
    return send_from_directory("static", "index.html")


@app.route("/static/<path:path>")
def static_files(path):
    return send_from_directory("static", path)


@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    """Receive updates from Telegram."""
    if request.headers.get("content-type") == "application/json":
        json_string = request.get_data().decode("utf-8")
        update = Update.de_json(json.loads(json_string), application.bot)
        application.update_queue.put_nowait(update)
        return "", 200
    return "", 403


@app.route("/set_webhook", methods=["GET"])
def set_webhook():
    webhook_url = f"{WEB_URL}/webhook"
    application.bot.set_webhook(url=webhook_url)
    return f"Webhook set to {webhook_url}", 200


# ---------- Main ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Set webhook on Render
    if os.environ.get("RENDER") or os.environ.get("RENDER_EXTERNAL_URL"):
        webhook_url = f"{WEB_URL}/webhook"
        application.bot.set_webhook(url=webhook_url)
        logger.info(f"Webhook set to {webhook_url}")
    app.run(host="0.0.0.0", port=port, debug=False)
