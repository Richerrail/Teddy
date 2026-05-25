# Secure Messenger Telegram Bot

## ⚠️ Security Warning

**NEVER** commit your Telegram bot token to GitHub!

This repo uses `.gitignore` to block `.env` files. Always set the token via environment variables.

## Local Development

```bash
pip install -r requirements.txt

# Option 1: Export directly (not saved to any file)
export TELEGRAM_BOT_TOKEN="ton_token"

# Option 2: Use .env file (already gitignored)
cp .env.example .env
# Edit .env and add your real token, then:
python telegram_bot.py
```

## Deploy on Render (free Web Service)

The bot auto-detects Render and switches to **webhook mode**.

1. Push ce repo sur GitHub (sans token !)
2. Sur [render.com](https://render.com) → New → **Web Service**
3. Connecte ton repo GitHub
4. Va dans l'onglet **Environment** et ajoute :
   - `TELEGRAM_BOT_TOKEN` = ton vrai token
5. Clique sur **Manual Deploy** → **Deploy latest commit**

**Important** : le token reste sur Render uniquement, jamais dans le code.

**Limitation** : le tier gratuit Web Service s'endort après 15 min d'inactivité. Ton bot peut manquer des messages pendant qu'il dort.

Pour un bot 24/7 sans interruption, utilise un **Background Worker** à la place (toujours gratuit sur Render).
