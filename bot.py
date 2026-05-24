import os
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import google.generativeai as genai

TOKEN = os.getenv("
8968685727:AAEs9ViZlOpknZOGpMpZO-wiWfaieRubDFw")
GEMINI_API = os.getenv("AIzaSyDTx796TfXOuOyFspuZcLh8o3i6_j9S0II")

genai.configure(api_key=GEMINI_API)

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):

    file = None

    if update.message.voice:
        file = await update.message.voice.get_file()
    elif update.message.audio:
        file = await update.message.audio.get_file()
    elif update.message.document:
        file = await update.message.document.get_file()
    else:
        return

    path = "audio.ogg"
    await file.download_to_drive(path)

    await update.message.reply_text("🎙 Processing...")

    model = genai.GenerativeModel("gemini-1.5-flash")

    uploaded = genai.upload_file(path)
    time.sleep(2)

    response = model.generate_content([
        uploaded,
        "Give summary, key points, sentiment, action items"
    ])

    await update.message.reply_text(response.text)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(
    filters.VOICE | filters.AUDIO | filters.Document.ALL,
    handle_audio
))

print("Bot Running...")
app.run_polling()