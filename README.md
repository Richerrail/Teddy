# Secure Messenger Telegram Bot

## ⚠️ Security Warning

**NEVER** commit your Telegram bot token to GitHub!

This repo uses `.gitignore` to block `.env` files. Always set the token via environment variables.

## Commands

- `/start` – Show welcome message and how to use
- `/app` – Open the **Mini App** (secure in-app web interface)
- `/encrypt <message>` – Encrypt a message via command
- `/decrypt <encrypted>` – Decrypt a message via command

## Local Development

```bash
pip install -r requirements.txt

# Option 1: Export directly (not saved to any file)
export TELEGRAM_BOT_TOKEN="ton_token"
export RENDER_EXTERNAL_URL="https://your-ngrok-url.ngrok.io"  # Optional, for webhook and app button

# Option 2: Use .env file (already gitignored)
cp .env.example .env
# Edit .env and add your real token, then:
python app.py
```

The Flask server runs on port `5000` by default. Visit `http://localhost:5000/` to test the Mini App.

## Deploy on Render (free Web Service)

The bot auto-detects Render and switches to **webhook mode**.

1. Push ce repo sur GitHub (sans token !)
2. Sur [render.com](https://render.com) → New → **Web Service**
3. Connecte ton repo GitHub
4. Va dans l'onglet **Environment** et ajoute :
   - `TELEGRAM_BOT_TOKEN` = ton vrai token
   - `RENDER_EXTERNAL_URL` = ton URL Render (ex: `https://teddy-tedu.onrender.com`)
5. Clique sur **Manual Deploy** → **Deploy latest commit**

**Important** : le token et l'URL restent sur Render uniquement, jamais dans le code.

### Mini App

Once deployed, the `/app` command will show a button to open the **Telegram Mini App**. This opens the web UI directly inside Telegram for encrypting and decrypting messages.

## File Structure

| File | Description |
|------|-------------|
| `app.py` | Flask server, API endpoints, and Telegram webhook handler |
| `secure_messenger.py` | Core encryption/decryption logic |
| `static/index.html` | Mini App HTML interface |
| `static/style.css` | Mini App styles |
| `static/app.js` | Mini App logic |
| `telegram_bot.py` | Standalone bot (for polling mode, used by old render.yaml) |
| `requirements.txt` | Python dependencies |
| `render.yaml` | Render configuration |
