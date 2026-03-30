from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from google import genai
import random

# 🔑 API KEYS (3 daal)
API_KEYS = [
    "AIzaSyDa9quuDFktPnTMLJUnIjwuxQvcC7nZbpU",
    "AIzaSyDG78OfBi2f76G1BVRsRAUHABYl7DoJBRo",
    "AIzaSyDG78OfBi2f76G1BVRsRAUHABYl7DoJBRo"
]

BOT_TOKEN = "8717190254:AAH-1BmJ4A1P27rlDXG7nby6ll42OUH1WUI"

# 👤 User usage tracking
user_usage = {}

# 🔄 Random client generator
def get_client():
    key = random.choice(API_KEYS)
    return genai.Client(api_key=key)

# ✂️ Split long messages
def split_message(text, limit=4000):
    return [text[i:i+limit] for i in range(0, len(text), limit)]

# 🚀 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello bhai 😎\nMain tera AI bot hoon 🤖\nKuch bhi puch le!")

# 💬 Main handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_message = update.message.text

    # 🧠 user limit check
    if user_id not in user_usage:
        user_usage[user_id] = 0

    if user_usage[user_id] >= 6:
        await update.message.reply_text("Bhai aaj ka limit khatam ho gaya 😅\nKal fir aana 👋")
        return

    user_usage[user_id] += 1

    try:
        client = get_client()

        # 🧠 Short answer prompt
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Answer in short and clear (max 150 words): {user_message}"
        )

        reply = response.text

        # ✂️ Split if long
        parts = split_message(reply)

        for part in parts:
            await update.message.reply_text(part)

    except Exception as e:
        await update.message.reply_text("Thoda error aa gaya bhai 😅\nBaad me try karna")

# 🚀 App setup
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot chal raha hai... 💀🔥")

app.run_polling()