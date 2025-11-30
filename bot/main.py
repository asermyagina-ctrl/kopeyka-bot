import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
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

async def on_startup(bot: Bot):
    # Получаем домен из переменных окружения App Platform
    domain = os.getenv('APP_DOMAIN', 'localhost')
    webhook_url = f"https://{domain}/webhook"
    await bot.set_webhook(webhook_url)
    logger.info(f"Webhook set to: {webhook_url}")

def main():
    dp.startup.register(on_startup)
    
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path="/webhook")
    setup_application(app, dp, bot=bot)
    
    port = int(os.environ.get("PORT", 8000))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
