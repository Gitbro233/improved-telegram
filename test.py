import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import executor
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")  # Загружаем токен из переменных окружения
ADMIN_ID = os.getenv("ADMIN_ID")  # ID админа (куда будут приходить вопросы)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

# Главное меню
main_keyboard = InlineKeyboardMarkup(row_width=2)
btn_start = InlineKeyboardButton("🚀 С чего начать?", callback_data="start_info")
btn_kpd = InlineKeyboardButton("📊 КПД и качество трафика", callback_data="kpd_info")
btn_ask = InlineKeyboardButton("❓ Задать вопрос", callback_data="ask_question")
main_keyboard.add(btn_start, btn_kpd, btn_ask)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Привет! Здесь ты найдёшь информацию по арбитражу трафика.", reply_markup=main_keyboard)

@dp.callback_query_handler(lambda c: c.data == 'start_info')
async def start_info(callback_query: types.CallbackQuery):
    text = "🔹 **С чего начать в арбитраже трафика?**\n\n1️⃣ Определи нишу (например, крипта, гемблинг)\n2️⃣ Найди клиента (через Tgstat, Telemetr)\n3️⃣ Настрой перелив трафика\n4️⃣ Масштабируй и улучшай КПД"
    await bot.send_message(callback_query.from_user.id, text)

@dp.callback_query_handler(lambda c: c.data == 'kpd_info')
async def kpd_info(callback_query: types.CallbackQuery):
    text = "📊 **Что такое КПД?**\nКПД – это показатель эффективности трафика.\n\nПример:\n- Привёл 1000 человек, заработал 500$\n- Эти люди принесли клиенту 1500$\n✅ Отличный КПД → ставка увеличивается!"
    await bot.send_message(callback_query.from_user.id, text)

@dp.callback_query_handler(lambda c: c.data == 'ask_question')
async def ask_question(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "✉️ Напиши свой вопрос, и я передам его админу!")

@dp.message_handler()
async def forward_to_admin(message: types.Message):
    if str(message.from_user.id) != ADMIN_ID:  # Проверяем, чтобы админ сам себе не пересылал
        await bot.send_message(ADMIN_ID, f"📩 Вопрос от @{message.from_user.username}:\n\n{message.text}")
        await message.reply("✅ Вопрос отправлен админу! Ожидайте ответ.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
