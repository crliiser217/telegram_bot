from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Создание кнопок для клиента
b1 = KeyboardButton('/Информация')
b2 = KeyboardButton('/Адрес')
b3 = KeyboardButton('/Каталог')
b4 = KeyboardButton('/Оценить')
b5 = KeyboardButton('/Итоги')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1).row(b2, b3).row(b4, b5)
