import os
import time
import multiprocessing
from http.server import HTTPServer, BaseHTTPRequestHandler

# Импортируем функцию запуска бота
from bot.telegram_bot import run_bot

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK - Bot and Server are running')
    
    def log_message(self, format, *args):
        print(f"HTTP Request: {format % args}")

def start_http_server():
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Starting HTTP server on port {port}")
    
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    print("✅ HTTP Server started successfully!")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("HTTP Server stopped")

def start_bot_process():
    """Запускаем бота в отдельном процессе"""
    print("🤖 Starting Telegram bot...")
    try:
        run_bot()
    except Exception as e:
        print(f"❌ Bot crashed: {e}")
        # Можно добавить перезапуск бота здесь

def main():
    # Запускаем HTTP-сервер в главном процессе
    http_process = multiprocessing.Process(target=start_http_server)
    http_process.start()
    
    # Запускаем бота в отдельном процессе
    bot_process = multiprocessing.Process(target=start_bot_process)
    bot_process.start()
    
    print("✅ Both HTTP server and Bot are running!")
    
    # Ждем завершения процессов (хотя они должны работать вечно)
    try:
        http_process.join()
        bot_process.join()
    except KeyboardInterrupt:
        print("🛑 Stopping both processes...")
        http_process.terminate()
        bot_process.terminate()

if __name__ == '__main__':
    main()
