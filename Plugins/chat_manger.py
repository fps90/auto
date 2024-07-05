# Requier Modules 
from pyrogram import Client, types, filters, enums
from pyromod.exceptions import ListenerTimeout
import asyncio 

# Requier Bot Plugins and Helper
from Plugins.helpers import *
from Config import database


# Pyrorgam filters 
def IS_SPLIT(data):
    def func(flt, _, query: types.CallbackQuery):
        return query.data.split('|')[0] == flt.data
    
    return filters.create(func , data=data)



# ON Add New Chat
@Client.on_callback_query(filters.regex('^ADD_CHAT$'))
async def ON_ADD_CHAT(app :Client, query: types.CallbackQuery):
    await query.edit_message_text(
        text=HOME_MESSAGE['GET_CHAT_USERNAME'] ,reply_markup=BACK()
    )

    database.UPDATE_TEMP('onListen', True)

    try:
        data = await app.listen(chat_id=query.message.chat.id, filters=filters.text & filters.private, timeout=60)
    except ListenerTimeout as e:
        return
    
    if database.GET_TEMP('onListen') == False:
        return
    
    ChatUsernmae = data.text
    # With Check Message
    message_data = await app.send_message(chat_id=query.message.chat.id ,text=HOME_MESSAGE['WITH_CHECK_USERNAME'])


    # Chekc USernmae 
    try:
        chatData = await app.get_chat(chat_id=ChatUsernmae)
    except Exception as e:
        await app.edit_message_text(
            chat_id=query.message.chat.id , message_id=message_data.id, 
            text=HOME_MESSAGE['USERNAME_INVELD'], reply_markup=BACK()
        )
        return
    # Bot Devs Radfx2 @R_AFX CH : @radfx2
    
    # Check Chat Types
    if not chatData.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        await app.edit_message_text(
            chat_id=query.message.chat.id , message_id=message_data.id, 
            text=HOME_MESSAGE['CHAT_TYPE_INVELD'], reply_markup=BACK()
        )
        return
    
    datas = database.GET_DATA()
    datas['chats'].update({chatData.username:{'first_name':chatData.first_name, 'id':chatData.id}}) 
    database.UPDATE_DATA(datas)

    await app.edit_message_text(
            chat_id=query.message.chat.id , message_id=message_data.id, 
            text=HOME_MESSAGE['DONE_ADD_CHAT'].format(len(datas['chats'])), reply_markup=BACK()
        )


# ON Show Chats 
@Client.on_callback_query(filters.regex('^SHOW_CHAT$'))
async def ON_SHOW_CHAT(app: Client, query: types.CallbackQuery):
    await query.edit_message_text(
        text=HOME_MESSAGE['SHOW_CHAT'], reply_markup=SHOW_CHAT()
    )



# On Delet Chats
@Client.on_callback_query(IS_SPLIT('delet_chat'))
async def ON_DELETE_CHAT(app: Client, query: types.CallbackQuery):
    chatUsername = query.data.split('|')[1]
    await query.edit_message_text(
        text=HOME_MESSAGE['WITH_DELETE_CHAT']
    )
    await asyncio.sleep(0.5)
    datas = database.GET_DATA()
    datas['chats'].pop(chatUsername)
    database.UPDATE_DATA(datas)
    await query.answer(text='تم حذف المجموعة')
    await query.edit_message_text(
        text=HOME_MESSAGE['SHOW_CHAT'], reply_markup=SHOW_CHAT()
    )  

