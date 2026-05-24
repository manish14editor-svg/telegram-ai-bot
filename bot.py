import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import google.generativeai as genai

TOKEN = os.getenv("
8968685727:AAEs9ViZlOpknZOGpMpZO-wiWfaieRubDFw")
GEMINI_API = os.getenv("AIzaSyDTx796TfXOuOyFspuZcLh8o3i6_j9S0II")

genai.configure(api_key=GEMINI_API)

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):

    telegram_file = None

    if update.message.voice:
        telegram_file = await update.message.voice.get_file()

    elif update.message.audio:
        telegram_file = await update.message.audio.get_file()

    elif update.message.document:
        telegram_file = await update.message.document.get_file()

    else:
        return

    file_path = "audio.ogg"

    await telegram_file.download_to_drive(file_path)

    await update.message.reply_text("🎙 Processing Audio...")

    model = genai.GenerativeModel("gemini-1.5-flash")

    uploaded_file = genai.upload_file(file_path)

    response = model.generate_content([
        uploaded_file,
        """
Analyze this call recording.

Give:
- Summary
- Important Points
- Sentiment
- Action Required
"""
    ])

    await update.message.reply_text(response.text)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(
    MessageHandler(
        filters.VOICE | filters.AUDIO | filters.Document.ALL,
        handle_audio
    )
)

print("Bot Running...")
app.run_polling()