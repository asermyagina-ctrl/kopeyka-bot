from aiohttp import web
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def health_check(request):
    logger.info("Health check called")
    return web.Response(text="OK - Server is running")

app = web.Application()
app.router.add_get('/health', health_check)
app.router.add_get('/', health_check)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting HTTP server on port {port}")
    web.run_app(app, host='0.0.0.0', port=port, print=None)
