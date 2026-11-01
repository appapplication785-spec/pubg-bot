from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import random
import string

# 🔴 እዚህ ጋር የእርስዎን ቶከን ያስገቡ
TOKEN = "9157089778:AAG7LkrTZAWIi35_gS2V7Lc6p44ISiDyZIM"

# ስሞች የሚቀያየሩበት ዝርዝር
FIRST_NAMES = ["Saron", "Abebe", "Kebede", "Marta", "Dawit", "Hanna", "Yonas", "Tigist", "Samuel", "Bethel"]
LAST_NAMES = ["Bizuayehu", "Tesfaye", "Alemu", "Girma", "Kassa", "Bekele", "Mulugeta", "Haile", "Desta", "Tadesse"]

# ራሱን የቻለ ኢሜል እና ፓስወርድ የሚፈጥር ፋንክሽን
def generate_account():
    # ስሞችን በዘፈቀደ መምረጥ
    f_name = random.choice(FIRST_NAMES)
    l_name = random.choice(LAST_NAMES)
    
    # የዘፈቀደ 8 ፊደላት ማመንጨት ለኢሜል
    random_letters = ''.join(random.choices(string.ascii_lowercase, k=8))
    email = f"{random_letters}@gmail.com"
    
    # የዘፈቀደ የይለፍ ቃል ማመንጨት
    password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$", k=12))
    
    return f_name, l_name, email, password

# የ /start ትዕዛዝ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Register an Account", callback_data='register')],
        [InlineKeyboardButton("My Accounts", callback_data='accounts')],
        [InlineKeyboardButton("Balance", callback_data='balance')],
        [InlineKeyboardButton("Referrals", callback_data='referrals')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Choose an option from the menu below:",
        reply_markup=reply_markup
    )

# የቁልፍ ሰሌዳው ሲነካ የሚሰራ
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'register':
        # አዲስ አካውንት መፍጠር (ስሞች በዘፈቀደ ይቀያየራሉ)
        f_name, l_name, email, password = generate_account()
        
        text = (
            "🎉 **New Account Generated!**\n\n"
            f"First name: {f_name}\n"
            f"Last name: {l_name}\n"
            "Year of birth: 1987\n\n"
            f"📧 **Email:** `{email}`\n"
            f"🔑 **Password:** `{password}`\n\n"
            "⚠️ Be sure to use the specified data, otherwise the account will not be paid."
        )
        await query.edit_message_text(text=text, parse_mode='Markdown')
        
    elif query.data == 'balance':
        await query.edit_message_text(text="💰 Your current balance is: $0.00")
        
    elif query.data == 'accounts':
        await query.edit_message_text(text="📁 You have no registered accounts yet. Click 'Register an Account' to get one.")
        
    elif query.data == 'referrals':
        await query.edit_message_text(text="🔗 Your referral link: https://t.me/YourBot?start=ref123")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
