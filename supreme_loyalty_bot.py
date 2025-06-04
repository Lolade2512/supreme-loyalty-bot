
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = '7422859486:AAGy17m3cn0d12uDOs2NER_EISt7XAExmL0'

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory user data and used codes
user_data = {}
used_codes = set()

# Load valid codes from file
def load_valid_codes():
    try:
        with open("valid_codes.txt", "r") as file:
            return set(code.strip() for code in file.readlines())
    except FileNotFoundError:
        return set()

valid_codes = load_valid_codes()

# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.chat.id
    await update.message.reply_text(
        "👑 Welcome to Supreme Loyalty Bot!\n"
        "Each time you buy, you’ll get a secret code. Enter it here to earn punches.\n"
        "📱 You are tracked by your phone number.\n"
        "Type /mypoints to check your progress.\n"
        "Type /redeem to enter a code."
    )

async def mypoints(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.chat.id
    count = user_data.get(phone, 0)
    squares = "⬜" * count + "◻️" * (25 - count)
    await update.message.reply_text(f"📱 Your Progress: {count}/25\n{squares}")

async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.chat.id
    args = context.args

    if not args:
        await update.message.reply_text("🔐 Send the code you received after your purchase.")
        return

    code = args[0].strip()

    if code in used_codes:
        await update.message.reply_text("❌ This code has already been used.")
        return

    if code in valid_codes:
        used_codes.add(code)
        user_data[phone] = user_data.get(phone, 0) + 1
        await update.message.reply_text("✅ Code accepted! You earned a punch. Use /mypoints to see your progress.")
    else:
        await update.message.reply_text("❌ Invalid code. Please try again.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mypoints", mypoints))
    app.add_handler(CommandHandler("redeem", redeem))

    print("✅ Bot is running and ready.")
    app.run_polling()

if __name__ == "__main__":
    main()
