import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Я ваш финансовый помощник Копейка!\n"
        "Начните с ввода операции:\n"
        "• Перекрёсток 1430\n"
        "• 20.11.2025 Кафе 500\n"
        "• Или отправьте фото чека"
    )

@dp.message()
async def handle_message(message: types.Message):
    await message.answer(f"📝 Получил: {message.text}\n\nСейчас настраиваю систему!")

if __name__ == '__main__':
    from aiogram import executor
    logger.info("Бот запущен в режиме Long Polling")
    executor.start_polling(dp, skip_updates=True)
