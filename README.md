# Secure Messenger Telegram Bot

## Local

```bash
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN="ton_token"
python telegram_bot.py
```

## Deploy on Render (free Web Service)

The bot auto-detects Render and switches to **webhook mode**.

1. Push ce repo sur GitHub
2. Sur [render.com](https://render.com) → New → **Web Service**
3. Connecte ton repo GitHub
4. Dans **Environment**, ajoute :
   - `TELEGRAM_BOT_TOKEN` = ton token
5. Deploy

**Limitation** : le tier gratuit Web Service s'endort après 15 min d'inactivité. Ton bot peut manquer des messages pendant qu'il dort.

Pour un bot 24/7 sans interruption, utilise un **Background Worker** à la place (toujours gratuit sur Render).
