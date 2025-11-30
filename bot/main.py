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
    # Не выходим, чтобы HTTP-сервер работал для диагностики
    bot = None
    dp = None
else:
    logger.info("✅ Токен найден, настраиваем бота...")
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
    status = "Bot is running" if TOKEN else "Bot token not set"
    return web.Response(text=f"OK - {status}")

async def start_bot():
    """Запускаем бота в фоновом режиме"""
    if bot and dp:
        logger.info("🚀 Запускаем бота...")
        from aiogram import executor
        await executor.start_polling(dp, skip_updates=True)
    else:
        logger.warning("🤖 Бот не запущен - нет токена")

async def start_http_server():
    """Запускаем HTTP-сервер"""
    app = web.Application()
    app.router.add_get('/health', health_check)
    app.router.add_get('/', health_check)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    port = int(os.environ.get("PORT", 8000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"🌐 HTTP-сервер запущен на порту {port}")

async def main():
    """Запускаем и бота, и HTTP-сервер"""
    # Запускаем HTTP-сервер
    await start_http_server()
    
    # Запускаем бота в фоне, если есть токен
    if TOKEN:
        await start_bot()
    else:
        logger.error("❌ TELEGRAM_TOKEN не установлен! Бот не запущен.")
        logger.info("💡 Добавьте TELEGRAM_TOKEN в настройки App Platform")

if __name__ == '__main__':
    asyncio.run(main())
