import telebot
from telebot import types
import requests


BOT_TOKEN = "8126027623:AAGkpF4wNaJoOOz7MeWNPGY_nxZCVHYAIXw"
bot = telebot.TeleBot(BOT_TOKEN)


API_KEY = "a67580b01d1d479a9c4942383f46a838"

BASE_URL = "https://api.football-data.org/v4/"

# --- Tugmalar menyusi ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("🏆 Turnir tanlash")
    btn2 = types.KeyboardButton("📅 Ertangi o'yinlar")
    btn3 = types.KeyboardButton("⚽ Bugungi o'yinlar")
    btn4 = types.KeyboardButton("🔄 Yangilash")
    btn5 = types.KeyboardButton("❓ Yordam")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup

# --- Boshlanish ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 
        "Salom! ⚽ Futbol tahlili botiga xush kelibsiz.\nQuyidagi tugmalardan birini tanlang:", 
        reply_markup=main_menu())

# --- Xabarlarni qayta ishlash ---
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "⚽ Bugungi o'yinlar":
        send_matches(message.chat.id, "today")
    elif message.text == "📅 Ertangi o'yinlar":
        send_matches(message.chat.id, "tomorrow")
    elif message.text == "🏆 Turnir tanlash":
        send_competitions(message.chat.id)
    elif message.text == "🔄 Yangilash":
        bot.send_message(message.chat.id, "🔄 Ma'lumot yangilanmoqda...")
        send_matches(message.chat.id, "today")
    elif message.text == "❓ Yordam":
        bot.send_message(message.chat.id, 
            "📖 Yordam:\n\n- ⚽ Bugungi o'yinlar: faqat bugungi o'yinlar\n"
            "- 📅 Ertangi o'yinlar: ertangi o'yinlar\n"
            "- 🏆 Turnir tanlash: liga va turnirlarni tanlash\n"
            "- 🔄 Yangilash: ma'lumotlarni qayta yuklash",
            reply_markup=main_menu())
    else:
        bot.send_message(message.chat.id, "Tugmalardan birini tanlang 👇", reply_markup=main_menu())

# --- API orqali ma'lumot olish ---
def send_matches(chat_id, day):
    try:
        headers = {"X-Auth-Token": API_KEY}
        response = requests.get(BASE_URL + f"matches?dateFrom={day}&dateTo={day}", headers=headers)
        data = response.json()

        if "matches" not in data or len(data["matches"]) == 0:
            bot.send_message(chat_id, "❌ Hozircha o'yinlar topilmadi.")
            return

        msg = "📅 O'yinlar:\n\n"
        for match in data["matches"]:
            home = match["homeTeam"]["name"]
            away = match["awayTeam"]["name"]
            status = match["status"]
            msg += f"{home} 🆚 {away} ({status})\n"
        bot.send_message(chat_id, msg)

    except Exception as e:
        bot.send_message(chat_id, f"Xatolik yuz berdi: {e}")

def send_competitions(chat_id):
    try:
        headers = {"X-Auth-Token": API_KEY}
        response = requests.get(BASE_URL + "competitions", headers=headers)
        data = response.json()

        if "competitions" not in data:
            bot.send_message(chat_id, "❌ Turnirlar topilmadi.")
            return

        msg = "🏆 Turnirlar ro'yxati:\n\n"
        for comp in data["competitions"][:10]:  # faqat birinchi 10 tasini ko'rsatamiz
            msg += f"• {comp['name']} ({comp['area']['name']})\n"
        bot.send_message(chat_id, msg)

    except Exception as e:
        bot.send_message(chat_id, f"Xatolik yuz berdi: {e}")

# --- Botni ishga tushirish ---
print("Bot ishlayapti...")
bot.infinity_polling()