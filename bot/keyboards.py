from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("Редактировать список слов🔄"))
keyboard.add(KeyboardButton("Спарсить чаты🦾"))

edit_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
edit_keyboard.add(KeyboardButton("Пропустить➡"))