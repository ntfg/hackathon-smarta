from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, Bot 
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
import os
import jwt
import datetime

from .text_parser import parse_dialogs
from .keyboards import keyboard, edit_keyboard
from .states import WordStates

load_dotenv()
    
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot,
                storage=MemoryStorage())

keywords = ["нашёл", "потерял"]

allowed_user = int(os.getenv("ALLOWED_USER"))

@dp.message_handler(lambda message: message.chat.id == allowed_user, commands=["start"])
async def start(message):
    await bot.send_message(message.chat.id, 
                           "Привет",
                           reply_markup=keyboard)

@dp.message_handler(lambda message: message.chat.id == allowed_user, Text("Редактировать список слов🔄"))
async def edit_words(message):
    await bot.send_message(message.chat.id,
                           "Пришлите новый список слов, каждое с новой строки",
                           reply_markup=edit_keyboard)
    await WordStates.word.set()


@dp.message_handler(lambda message: message.chat.id == allowed_user, Text(equals="Пропустить➡"), state=WordStates.word)
async def skip_words(message, state: FSMContext):
    await bot.send_message(message.chat.id,
                     "Как пожелаете",
                     reply_markup=keyboard)
    await state.finish()


@dp.message_handler(lambda message: message.chat.id == allowed_user, state=WordStates.word)
async def list_of_words(message, state: FSMContext):
    words = message.text.split("\n")
    if all(map(lambda x: len(x.split())==1, words)):
        await bot.send_message(message.chat.id,
                               "Список успешно изменён✅",
                               reply_markup=keyboard)
        keywords = words
        print(keywords)
        await state.finish()
    else:
        await bot.send_message(message.chat.id,
                               "Кажется, вы ввели больше одного слова в строке")
        

@dp.message_handler(lambda message: message.chat.id == allowed_user, Text(equals="Спарсить чаты🦾"))
async def parse_chats(message):
    await parse_dialogs(keywords)
    await bot.send_message(message.chat.id,
                           "Список чатов успешно спаршен✅")
    

@dp.message_handler(lambda message: message.chat.id == allowed_user, Text(equals="Получить токен"))
async def get_token(message):
    jwt_payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(weeks=1)
    }
    message_text = f'Этот токен будет действовать ровно неделю\n\n{jwt.encode(jwt_payload, os.getenv("JWT_KEY"), algorithm="HS256")}'
    await bot.send_message(message.chat.id,
                           message_text)

    