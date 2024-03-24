import asyncio
from pyrogram import Client
from datetime import datetime
import pymorphy2
import nltk 
from nltk.tokenize import word_tokenize 
from typing import List
import os

from data import Database

db = Database()

morph_analyzer = pymorphy2.MorphAnalyzer()


def _word_analyzer(keywords: List[str], text: str) -> bool:
    # Все слова ставятся в начальную форму
    keywords = [morph_analyzer.parse(word)[0].normal_form for word in keywords]
    text = [morph_analyzer.parse(word)[0].normal_form for word in word_tokenize(text)]
    
    return any(keyword in text for keyword in keywords)


def _strip_ascii(text: str):
    return ''.join(c for c in text if c.isascii())


async def parse_dialogs(keywords: List[str]):
    async with Client("my_account", api_id=os.getenv("API_ID"), api_hash=os.getenv("API_HASH")) as app:
        async for chat in app.get_dialogs():
            if chat.chat.type.value in ["group", "channel"]:
                async for message in app.get_chat_history(str(chat.chat.id), limit=100):
                    if message.text:
                        text = _strip_ascii(message.text)
                        if _word_analyzer(keywords, text):
                        
                        # Если это свойство не None, то это группа. Иначе канал
                            if message.from_user:
                                db.add(message.chat.title, message.from_user.username, message.from_user.id, text, message.date)
                            else:
                                db.add(title=message.chat.title, text=text, time=message.date)
                        

                    
                



