import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Ambil token dari environment variable
BOT_TOKEN = os.getenv("7960179021:AAEOwRM8btLhbY_2fTf1c9Emz6YzMPKAlTA")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN belum diset di Environment Variables.")

# Command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot aktif. Kirim teks untuk saya simpan.")

# Simpan teks sederhana ke file
async def save_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    with open("notes.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")

    await update.message.reply_text("Teks disimpan.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_text))

    print("Bot berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
