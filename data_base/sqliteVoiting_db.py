import psycopg2 as ps
from create_bot import bot
import os

def sqk_start():
    global base, cur
    base = ps.connect(os.environ.get('DATABASE_URL'), sslmode='require')
    cur = base.cursor()
    if base:
        print('Data base for voiting connected OK')
    


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO answ VALUES (%s)', (data,))
        base.commit()


async def sql_read(message):
    likes = 0
    dislikes = 0
    cur.execute('SELECT * FROM answ')
    for ret in cur.fetchall():
        if ret[0] == '1':
            likes += 1
        else:
            dislikes += 1
    await bot.send_message(message.from_user.id, f'Лайки\n{likes}\nДизлайки\n{dislikes}')