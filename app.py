from aiogram.utils import executor
from loader import dp 
from dotenv import load_dotenv

load_dotenv()

executor.start_polling(dp, skip_updates=True)
