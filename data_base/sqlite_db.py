import os
from create_bot import bot
import psycopg2 as ps


# Работа с базой данных
# Таблица для каталога
# Подключение к базе данных


def sqk_start():
    global base, cur
    base = ps.connect(os.environ.get('DATABASE_URL'), sslmode='require')
    cur = base.cursor()
    if base:
        print('Data base connected OK')
        cur.execute('''CREATE TABLE IF NOT EXISTS catalog(img TEXT, name TEXT PRIMARY KEY, description TEXT, 
        price TEXT); CREATE TABLE IF NOT EXISTS ans(like TEXT);''')
        base.commit()
    else:
        print('Database error')


# Добавление значений в таблицу
async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO catalog VALUES (%s, %s, %s, %s)', tuple(data.values()))
        base.commit()


# Чтение данных из таблицы
async def sql_read(message):
    cur.execute('SELECT * FROM catalog')
    for ret in cur.fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена: {ret[-1]}')


# Чтение данных для выбора удаляемой строки в таблице
async def sql_read_for_del():
    cur.execute('SELECT * FROM catalog')
    return cur.fetchall()


# Удаление строки
async def sql_delete_elem(data):
    cur.execute('DELETE FROM catalog WHERE name = %s', (data,))
    base.commit()


# Отключение базы данных
async def ps_off():
    cur.close()
    base.close()
