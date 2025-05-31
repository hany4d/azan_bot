from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import requests
from datetime import datetime
import jdatetime

# تابع شروع
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_message = f"""سلام {user.first_name} عزیز 🌹  
به ربات اذان‌گوی خودکار به افق تهران خوش آمدید! 🕌  
ربات دقیق و هوشمند برای اعلام اوقات شرعی روزانه ✅  

ویژگی‌ها:  
✅ اعلام خودکار اذان‌ها  
✅ قابلیت فعالیت در کانال و گروه برای اعلام خودکار اذان  
✅ زمان‌بندی دقیق  
✅ نمایش دستی اوقات شرعی  
✅ رایگان و بدون تبلیغات  

برای شروع برای کانال و گروه:  
1. ربات را به گروه یا کانال اضافه کنید  
2. آن را به‌عنوان ادمین تنظیم کنید  
3. به صورت خودکار برای شما اعلام در گروه یا کانال انجام می‌شود.

برای شروع برای اعلام خودکار در بات به شما:  
1. دکمه 🔔 تنظیمات اعلان اذان را بزنید."""

    keyboard = [
        [
            InlineKeyboardButton("❤️ آیدی پشتیبانی", callback_data='support'),
            InlineKeyboardButton("🕒 اوقات شرعی امروز (دستی)", callback_data='times')
        ],
        [
            InlineKeyboardButton("➕ افزودن ربات به گروه دلخواه", callback_data='add_group')
        ],
        [
            InlineKeyboardButton("➕ افزودن ربات به کانال دلخواه", callback_data='add_channel')
        ],
        [
            InlineKeyboardButton("🔔 تنظیمات اعلان اذان (برای من در بات)", callback_data='settings')
        ],
        [
            InlineKeyboardButton("📚 راهنمای ربات", callback_data='guide')
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)


# تابع تبدیل تاریخ
def get_date_info():
    today = datetime.now()
    persian_date = jdatetime.date.fromgregorian(date=today.date())
    hijri = requests.get(f"https://api.aladhan.com/v1/gToH?date={today.strftime('%d-%m-%Y')}").json()
    hijri_date = hijri['data']['hijri']['date']
    hijri_day = hijri['data']['hijri']['weekday']['ar']
    hijri_month = hijri['data']['hijri']['month']['ar']
    hijri_year = hijri['data']['hijri']['year']

    return {
        'gregorian': today.strftime('%d %B %Y'),
        'weekday': persian_date.strftime('%A'),
        'shamsi': f"{persian_date.day} {persian_date.strftime('%B')} {persian_date.year}",
        'hijri': f"{hijri_date} ({hijri_day}، {hijri_month} {hijri_year})"
    }

# تابع پاسخ به دکمه "times"
async def show_today_times(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        response = requests.get("https://api.aladhan.com/v1/timingsByCity?city=Tehran&country=Iran&method=7")
        data = response.json()['data']
        times = data['timings']

        date_info = get_date_info()

        message = f"""🧭 به افق تهران  
⭐️ {date_info['weekday']}  
📆 شمسی: {date_info['shamsi']}  
📅 میلادی: {date_info['gregorian']}  
📆 قمری: {date_info['hijri']}

🕌 اوقات شرعی امروز به افق تهران:

🕓 اذان صبح: {times['Fajr']}  
🌅 طلوع آفتاب: {times['Sunrise']}  
🕛 اذان ظهر: {times['Dhuhr']}  
☀️ اذان عصر: {times['Asr']}  
🌇 غروب آفتاب: {times['Sunset']}  
🕌 اذان مغرب: {times['Maghrib']}  
🌃 اذان عشاء: {times['Isha']}  
🌙 نیمه‌شب شرعی: {times['Midnight']}

📤 این پیام به‌صورت خودکار توسط ربات ارسال شده است. ⏰"""

        await query.message.reply_text(message)

    except Exception as e:
        await query.message.reply_text("❌ خطا در دریافت اطلاعات. لطفاً دوباره تلاش کنید.")


# --- اجرای ربات ---
if __name__ == '__main__':
    application = ApplicationBuilder().token('8108851924:AAEp5LZjdPCMUFp60esD2Z49CYzrQ77Qpp4').build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(show_today_times, pattern='^times$'))

    print("✅ ربات با موفقیت اجرا شد...")
    application.run_polling()
