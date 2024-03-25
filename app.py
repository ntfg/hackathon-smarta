from aiogram.utils import executor
from bot import dp 
from api import app
import threading
import asyncio
import os

def run_flask():
    app.run(os.getenv("SERVER_IP"), port=os.getenv("SERVER_PORT"))

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(executor.start_polling(dp))
    loop.run_forever()


if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    bot_thread = threading.Thread(target=run_bot)

    flask_thread.start()
    bot_thread.start()

    flask_thread.join()
    bot_thread.join()

