from pyrogram import Client, types, filters, enums
from pyromod.exceptions import ListenerTimeout
import asyncio

# Import plugins and helpers
from Plugins.helpers import *
from Config import database

HOME_MESSAGE = {
    'GET_CHAT_LINK': 'يرجى إرسال رابط المجموعة العامة أو الخاصة:',
    'WITH_CHECK_LINK': 'جارٍ التحقق من الرابط...',
    'LINK_INVALID': 'الرابط غير صالح، يرجى التأكد من صحة الرابط والمحاولة مرة أخرى.',
    'CHAT_TYPE_INVALID': 'نوع الدردشة غير صالح. يجب أن يكون نوع الدردشة مجموعة أو مجموعة سوبر.',
    'DONE_ADD_CHAT': 'تم إضافة المجموعة بنجاح. المجموعات الحالية: {}',
    'SHOW_CHAT': 'قائمة المجموعات الحالية:',
    'WITH_DELETE_CHAT': 'جارٍ حذف المجموعة...'
}

def BACK():
    return types.InlineKeyboardMarkup(
        [[types.InlineKeyboardButton("رجوع", callback_data="BACK")]]
    )

def IS_SPLIT(data):
    def func(flt, _, query: types.CallbackQuery):
        return query.data.split('|')[0] == flt.data
    
    return filters.create(func, data=data)

@Client.on_callback_query(filters.regex('^ADD_CHAT$'))
async def ON_ADD_CHAT(app: Client, query: types.CallbackQuery):
    await query.edit_message_text(
        text=HOME_MESSAGE['GET_CHAT_LINK'], reply_markup=BACK()
    )

    database.UPDATE_TEMP('onListen', True)

    try:
        data = await app.listen(chat_id=query.message.chat.id, filters=filters.text & filters.private, timeout=60)
    except ListenerTimeout:
        return
    
    if not database.GET_TEMP('onListen'):
        return
    
    chat_link = data.text
    message_data = await app.send_message(chat_id=query.message.chat.id, text=HOME_MESSAGE['WITH_CHECK_LINK'])

    try:
        chat_data = await app.get_chat(chat_link)
    except Exception as e:
        await app.edit_message_text(
            chat_id=query.message.chat.id, message_id=message_data.id, 
            text=HOME_MESSAGE['LINK_INVALID'], reply_markup=BACK()
        )
        return

    if chat_data.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        await app.edit_message_text(
            chat_id=query.message.chat.id, message_id=message_data.id, 
            text=HOME_MESSAGE['CHAT_TYPE_INVALID'], reply_markup=BACK()
        )
        return
    
    datas = database.GET_DATA()
    datas['chats'].update({chat_data.username or chat_data.id: {'first_name': chat_data.first_name, 'id': chat_data.id}}) 
    database.UPDATE_DATA(datas)

    await app.edit_message_text(
        chat_id=query.message.chat.id, message_id=message_data.id, 
        text=HOME_MESSAGE['DONE_ADD_CHAT'].format(len(datas['chats'])), reply_markup=BACK()
    )

@Client.on_callback_query(filters.regex('^SHOW_CHAT$'))
async def ON_SHOW_CHAT(app: Client, query: types.CallbackQuery):
    await query.edit_message_text(
        text=HOME_MESSAGE['SHOW_CHAT'], reply_markup=SHOW_CHAT()
    )

@Client.on_callback_query(IS_SPLIT('delete_chat'))
async def ON_DELETE_CHAT(app: Client, query: types.CallbackQuery):
    chat_identifier = query.data.split('|')[1]
    await query.edit_message_text(
        text=HOME_MESSAGE['WITH_DELETE_CHAT']
    )
    await asyncio.sleep(0.5)
    datas = database.GET_DATA()
    datas['chats'].pop(chat_identifier, None)
    database.UPDATE_DATA(datas)
    await query.answer(text='تم حذف المجموعة')
    await query.edit_message_text(
        text=HOME_MESSAGE['SHOW_CHAT'], reply_markup=SHOW_CHAT()
    )
