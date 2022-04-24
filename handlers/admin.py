from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ID = None

class FSMadmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()

#@dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_command(message : types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Режим администратора', reply_markup = admin_kb.button_case_admin)
    await message.delete()



#@dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message : types.Message):
    if message.from_user.id == ID:
        await FSMadmin.photo.set()
        await message.reply('Загрузи фото')

#@dp.message_handler(state="*", commands='отмена')
#@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message : types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')


#@dp.message_handler(content_types=['photo'], state=FSMadmin.photo)
async def load_photo(message : types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMadmin.next()
        await message.reply('Теперь введи название')


#@dp.message_handler(state=FSMadmin.name)
async def load_name(message : types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMadmin.next()
        await message.reply('Введи описание')


#@dp.message_handler(state=FSMadmin.description)
async def load_description(message : types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMadmin.next()
        await message.reply('Введи цену')



#@dp.message_handler(state=FSMadmin.price)
async def load_price(message : types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)
        await sqlite_db.sql_add_command(state)
        await state.finish()


#@dp.message_handler(command='Удалить')
async def delete_elem(message : types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read_for_del()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена: {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^^^^', reply_markup=InlineKeyboardMarkup().\
                        add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))


#@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def dell_callback(callback_query : types.CallbackQuery):
    await sqlite_db.sql_delete_elem(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")}\nтовар удален', show_alert=True)


def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands='Загрузить', state=None)
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMadmin.photo)
    dp.register_message_handler(load_name, state=FSMadmin.name)
    dp.register_message_handler(load_description, state=FSMadmin.description)
    dp.register_message_handler(load_price, state=FSMadmin.price)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(delete_elem, commands='Удалить')
    dp.register_callback_query_handler(dell_callback, lambda x: x.data and x.data.startswith('del '))
