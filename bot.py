from datetime import datetime
import gspread
import json
import os
import telebot
from telebot import types
from keep_alive import keep_alive

# ==========================================
# تحميل بيانات Google credentials من الـ Secrets
# ==========================================
creds_json = os.getenv("GOOGLE_CREDENTIALS")
SHEET_ID = os.getenv("SHEET_ID")
OWNER_ID = int(os.getenv("OWNER_ID"))  # لازم يكون int
TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

creds_dict = json.loads(creds_json)
gc = gspread.service_account_from_dict(creds_dict)
sh = gc.open_by_key(SHEET_ID)
worksheet = sh.sheet1

# ==========================================
# أوامر البوت
# ==========================================
@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    username = message.from_user.username or "N/A"
    first_name = message.from_user.first_name or "N/A"
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # تسجيل في Google Sheet
    worksheet.append_row([user_id, username, first_name, date])

    # إرسال إشعار ليك
    bot.send_message(
        OWNER_ID,
        f"👤 مستخدم جديد\n🆔 ID: {user_id}\n👤 Username: @{username}\n📛 الاسم: {first_name}\n📅 التاريخ: {date}"
    )

    # رسالة للمستخدم
    bot.send_message(message.chat.id, "✅ تم تسجيلك بنجاح!")

# ==========================================
# تشغيل البوت
# ==========================================
if __name__ == "__main__":
    keep_alive()
    print("✅ Bot is running...")
    bot.infinity_polling(skip_pending=True)
