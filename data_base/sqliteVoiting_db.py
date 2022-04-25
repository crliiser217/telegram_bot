import psycopg2 as ps
from create_bot import bot
import os

def sqk_start():
    global base2, cur2
    base2 = ps.connect(os.environ.get('DATABASE_URL'), sslmode='require')
    cur2 = base2.cursor()
    if base2:
        print('Data base for voiting connected OK')



async def sql_add_command(state):
    async with state.proxy() as data:
        cur2.execute('INSERT INTO ans VALUES (%s)', tuple(data.values()))
        base2.commit()


async def sql_read(message):
    likes = 0
    dislikes = 0
    cur2.execute('SELECT * FROM ans')
    for ret in cur2.fetchall():
        if ret[0] == '1':
            likes += 1
        else:
            dislikes += 1
    await bot.send_message(message.from_user.id, f'Лайки\n{likes}\nДизлайки\n{dislikes}')