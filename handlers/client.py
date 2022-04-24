from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from data_base import sqlite_db
from data_base import sqliteVoiting_db
from inlinekeyboards import kb_url, inkb
#from aiogram.types import ReplyKeyboardRemove

class FSMclient(StatesGroup):
    like = State()

#@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Добро пожаловать', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/crliiser_bot')


#@dp.message_handler(commands=['Информация'])
async def main_info(message: types.Message):
    await bot.send_message(message.from_user.id, 'Магазин цифровой техники', reply_markup=kb_client)

#@dp.message_handler(commands='Ссылки')
async def url_command(message : types.Message):
    await message.answer('Ссылки', reply_markup=kb_url)

#@dp.message_handler(commands=['Адрес'])
async def addres_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'ул. Ломоносова д.8\nс 9:00 до 21:00',
                           reply_markup=kb_client)

#@dp.message_handler(commands=['Каталог'])
async def catalog_command(message: types.Message):
    await sqlite_db.sql_read(message)

#@dp.message_handler(commands='Оценить', state=None)
async def voiting_command(message : types.Message):
    await FSMclient.like.set()
    await message.answer('Вам нравится это телеграм-бот', reply_markup=inkb)

#@dp.callback_query_handler(Text(startswith='like_'), state=FSMclient.like)
async def voiting_call(callback : types.CallbackQuery, state: FSMContext):
    res = int(callback.data.split('_')[1])
    async with state.proxy() as data:
        data['like'] = res
    await sqliteVoiting_db.sql_add_command(state)
    await state.finish()
    await callback.answer('Вы успешно проголосовали')
    #await callback.answer('Вы уже голосовали раннее', show_alert=True)

#@dp.message_handler(commands='Итоги')
async def show_likes(message: types.Message):
    await sqliteVoiting_db.sql_read(message)

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(main_info, commands='Информация')
    dp.register_message_handler(addres_command, commands='Адрес')
    dp.register_message_handler(catalog_command, commands='Каталог')
    dp.register_message_handler(url_command, commands='Ссылки')
    dp.register_message_handler(voiting_command, commands='Оценить', state=None)
    dp.register_callback_query_handler(voiting_call, Text(startswith='like_'), state=FSMclient.like)
    dp.register_message_handler(show_likes, commands='Итоги')
