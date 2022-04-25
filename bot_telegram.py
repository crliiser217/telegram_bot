import os

from aiogram.utils import executor

from create_bot import dp, bot
from data_base import sqlite_db
from data_base import sqliteVoiting_db

async def on_startup(dp):
    sqlite_db.sqk_start()
    sqliteVoiting_db.sqk_start()
    await bot.set_webhook(os.environ.get('URL_APP'))

async def on_shutdown(dp):
    await sqlite_db.ps_off()
    await bot.delete_webhook()


    #sqlite_db.sqk_start()
    #sqliteVoiting_db.sqk_start()

from handlers import client, admin, other

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)


executor.start_webhook(
    dispatcher=dp,
    webhook_path='',
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    skip_updates=True,
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 5000))
)
