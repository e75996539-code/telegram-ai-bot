import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from google import genai

# 🔐 Environment variables (Render se aayenge)
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 🤖 Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# 💬 Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message
        )

        reply = response.text

    except Exception as e:
        reply = "⚠️ Error aa gaya bhai, thoda baad me try kar"

    # Telegram message limit fix (4000 chars)
    for i in range(0, len(reply), 4000):
        await update.message.reply_text(reply[i:i+4000])

# 🚀 Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot chal raha hai...")

    app.run_polling()

if _name_ == "_main_":
    main()
