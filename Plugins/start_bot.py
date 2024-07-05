# Requier Mdoules 
from pyrogram import Client, types, filters
import asyncio 

# Requier Bot Helpers
from Plugins.helpers import HOME_MESSAGE, HONE_KEYBOARD
from Config import database, config

# On ?start Bot
@Client.on_message(filters.private & filters.user(config.SUDO) & filters.regex('^/start$'))
async def ON_START_BOT(app: Client, message: types.Message):
    await app.send_message(
        chat_id=message.chat.id, 
        text=HOME_MESSAGE['HOME'], reply_markup=HONE_KEYBOARD()
    )

# On Back Home 
@Client.on_callback_query(filters.regex('^back$'))
async def BACK_HOME(app: Client, query: types.CallbackQuery):
    database.UPDATE_TEMP('onListen', False)
    await query.edit_message_text(
        text=HOME_MESSAGE['HOME'], reply_markup=HONE_KEYBOARD()
    )
    