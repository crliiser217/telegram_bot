import sqlite3 as sq
from create_bot import bot

def sqk_start():
    global base, cur
    base = sq.connect('my_baza.db')
    cur = base.cursor()
    if base:
        print('Data base for voiting connected OK')
    base.execute('CREATE TABLE IF NOT EXISTS answ(like TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO answ VALUES (?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    likes = 0
    dislikes = 0
    for ret in cur.execute('SELECT * FROM answ').fetchall():
        if ret[0] == '1':
            likes += 1
        else:
            dislikes += 1
    await bot.send_message(message.from_user.id, f'Лайки\n{likes}\nДизлайки\n{dislikes}')