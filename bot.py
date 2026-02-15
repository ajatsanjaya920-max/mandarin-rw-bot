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
    # Reading mode
    if "reading_answer" in context.user_data:
        correct = context.user_data["reading_answer"]
        if user_text.lower() == correct.lower():
            cursor.execute("INSERT INTO progress VALUES (?,1)", (user_id,))
            conn.commit()
            await update.message.reply_text("Benar.")
        else:
            await update.message.reply_text(f"Salah. Jawaban benar: {correct}")
        context.user_data.pop("reading_answer")

    # Writing mode
    elif "writing_answer" in context.user_data:
        correct = context.user_data["writing_answer"]
        if user_text == correct:
            cursor.execute("INSERT INTO progress VALUES (?,1)", (user_id,))
            conn.commit()
            await update.message.reply_text("Benar.")
        else:
            await update.message.reply_text(f"Salah. Jawaban benar: {correct}")
        context.user_data.pop("writing_answer")

# ================= MAIN =================
def main():
    if TOKEN is None:
        raise ValueError("BOT_TOKEN belum diset di Environment Variables.")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("📖 Reading"), reading))
    app.add_handler(MessageHandler(filters.Regex("✍ Writing"), writing))
    app.add_handler(MessageHandler(filters.Regex("📊 Progress"), progress))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer))

    app.run_polling()

if __name__ == "__main__":
    main() 
