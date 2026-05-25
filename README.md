# Secure Messenger Telegram Bot

## Local

```bash
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN="ton_token"
python telegram_bot.py
```

## Deploy on Render (free)

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New → Blueprint
3. Connect your GitHub repo
4. In Render dashboard, go to your service → Environment → add `TELEGRAM_BOT_TOKEN`
5. Deploy

The bot runs 24/7 on Render's free worker tier.
# Teddy
