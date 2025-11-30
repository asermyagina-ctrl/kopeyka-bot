import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_bot():
    TOKEN = os.getenv('TELEGRAM_TOKEN')
    if not TOKEN:
        logger.error("❌ TELEGRAM_TOKEN не установлен!")
        return

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        await message.answer("✅ Бот работает! Тест успешен!")

    @dp.message()
    async def echo(message: types.Message):
        await message.answer(f"Эхо: {message.text}")

    logger.info("🚀 Запускаем бота...")
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    run_bot()
