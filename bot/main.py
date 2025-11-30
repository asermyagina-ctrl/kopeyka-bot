import os
import logging
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Проверяем токен
TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TOKEN:
    logger.error("❌ TELEGRAM_TOKEN не установлен!")
    exit(1)

logger.info("✅ Токен найден, запускаем бота...")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("✅ Бот работает! Тест успешен!")

@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Эхо: {message.text}")

# Простой HTTP-сервер для health check
async def health_check(request):
    return web.Response(text="OK")

async def start_bot():
    """Запускаем бота в фоновом режиме"""
    from aiogram import executor
    logger.info("🚀 Запускаем бота...")
    
    # Запускаем бота в отдельной задаче
    asyncio.create_task(executor.start_polling(dp, skip_updates=True))
    logger.info("✅ Бот запущен в фоновом режиме")

async def on_startup(app):
    """Запускаем при старте HTTP-сервера"""
    await start_bot()

def main():
    # Создаем HTTP-приложение
    app = web.Application()
    app.router.add_get('/health', health_check)
    app.router.add_get('/', health_check)
    
    # Запускаем бот при старте
    app.on_startup.append(on_startup)
    
    # Запускаем HTTP-сервер
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"🌐 HTTP-сервер запущен на порту {port}")
    web.run_app(app, host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()
    "Fix: Add HTTP server for health check"
