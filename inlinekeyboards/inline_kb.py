from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ССылки
kb_url = InlineKeyboardMarkup(row_width=1)
urlButton = InlineKeyboardButton(text='Youtube', url='https://youtube.com/')
urlButton2 = InlineKeyboardButton(text='Yandex', url='https://yandex.ru/')

kb_url.add(urlButton, urlButton2)


inkb = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Like', callback_data='like_1'),\
                                             InlineKeyboardButton(text='Dislike', callback_data='like_-1'))









