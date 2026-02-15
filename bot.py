import logging
import random
import sqlite3
import os
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ================= TOKEN =================
TOKEN = os.environ.get("7960179021:AAGDySkdWCF2JshRam3aZ2_DDhDk0hBvdWA")

# ================= DATABASE =================
conn = sqlite3.connect("mandarin_rw.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hanzi TEXT,
    pinyin TEXT,
    meaning TEXT,
    week INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS progress (
    user_id INTEGER,
    correct INTEGER
)
""")

conn.commit()

# ================= DATA KARAKTER AWAL (MINGGU 1-2) =================
characters_data = [
    ("我","wo3","saya",1),
    ("你","ni3","kamu",1),
    ("他","ta1","dia",1),
    ("是","shi4","adalah",1),
    ("不","bu4","tidak",1),
    ("有","you3","punya/ada",1),
    ("这","zhe4","ini",1),
    ("那","na4","itu",1),
    ("人","ren2","orang",1),
    ("好","hao3","baik",1),
    ("在","zai4","di",2),
    ("哪","na3","mana",2),
    ("什","shen2","apa (bagian)",2),
    ("么","me","apa (bagian)",2),
    ("叫","jiao4","bernama",2),
    ("名","ming2","nama (bagian)",2),
    ("字","zi4","huruf/karakter",2),
    ("国","guo2","negara",2),
    ("家","jia1","rumah/keluarga",2),
    ("大","da4","besar",2),
]

# Insert hanya kalau tabel masih kosong
cursor.execute("SELECT COUNT(*) FROM characters")
if cursor.fetchone()[0] == 0:
    cursor.executemany(
        "INSERT INTO characters (hanzi,pinyin,meaning,week) VALUES (?,?,?,?)",
        characters_data
    )
    conn.commit()

# ================= LOGGING =================
logging.basicConfig(level=logging.INFO)

# ================= WEEK LOGIC =================
def get_current_week():
    start_date = datetime(2024, 1, 1)  # Ganti sesuai tanggal mulai kamu
    today = datetime.now()
    delta = today - start_date
    return delta.days // 7 + 1

# ================= COMMANDS =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["📖 Reading", "✍ Writing"],
                ["📊 Progress"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Mandarin Reading & Writing Bot Aktif.",
        reply_markup=reply_markup
    )

async def reading(update: Update, context: ContextTypes.DEFAULT_TYPE):
    week = get_current_week()
    cursor.execute("SELECT hanzi, meaning FROM characters WHERE week <= ?", (week,))
    data = cursor.fetchall()

    if not data:
        await update.message.reply_text("Belum ada karakter tersedia.")
        return

    hanzi, meaning = random.choice(data)
    context.user_data["reading_answer"] = meaning
    await update.message.reply_text(f"Apa arti karakter ini?\n\n{hanzi}")

async def writing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    week = get_current_week()
    cursor.execute("SELECT hanzi, pinyin FROM characters WHERE week <= ?", (week,))
    data = cursor.fetchall()

    if not data:
        await update.message.reply_text("Belum ada karakter tersedia.")
        return

    hanzi, pinyin = random.choice(data)
    context.user_data["writing_answer"] = hanzi
    await update.message.reply_text(f"Tulis karakter untuk pinyin:\n\n{pinyin}")

async def progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    cursor.execute("SELECT COUNT(*) FROM progress WHERE user_id=? AND correct=1", (user_id,))
    count = cursor.fetchone()[0]
    await update.message.reply_text(f"Total jawaban benar: {count}")

async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = update.message.from_user.id

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
