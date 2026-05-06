from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import google.generativeai as genai

# 🔑 Yahan apni keys daalo (IMPORTANT: quotes lagana)
TELEGRAM_TOKEN = "8203672663:AAFjk_ovoZFcTPp-8M_8seUoK_a1S68XaMw"
GEMINI_API_KEY = "AIzaSyCKxA-s6meMq-2j9Bi_vqkCDY1Y6y7JcfA"

# Gemini setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Login details
USERNAME = "Anmol"
PASSWORD = "Hacker0000"

logged_in_users = {}

# 🤖 AI function
def get_ai_reply(msg):
    try:
        response = model.generate_content(msg)
        return response.text
    except Exception as e:
        return "Error: " + str(e)

# 🔐 Login command
async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("Use: /login id password")
        return

    username, password = context.args

    if username == USERNAME and password == PASSWORD:
        logged_in_users[update.effective_user.id] = True
        await update.message.reply_text("✅ Login successful!")
    else:
        await update.message.reply_text("❌ Wrong ID/Password")

# 💬 Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not logged_in_users.get(user_id):
        await update.message.reply_text("🔐 Please login first: /login id password")
        return

    msg = update.message.text
    reply = get_ai_reply(msg)

    await update.message.reply_text(reply)

# 📸 File/Image handler
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not logged_in_users.get(user_id):
        await update.message.reply_text("🔐 Login first")
        return

    await update.message.reply_text("📁 File/Image received!")

# ▶️ Start bot
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("login", login))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, handle_file))

print("🤖 Bot running...")
app.run_polling()