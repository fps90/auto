# Requier Module
from pyrogram import Client, filters, types
from pyromod.exceptions import ListenerTimeout
import asyncio 

# Requier helpers 
from Config import database, config
from Plugins.helpers import *


# ON Account Manger 
@Client.on_callback_query(filters.regex("^ACCOUNT_MANGE$"))
async def ON_ACCOUNT_MENGER(app: Client, query: types.CallbackQuery):
    datas = database.GET_DATA()
    if datas['status']['account'] == True:
        await query.edit_message_text(
            text=HOME_MESSAGE['VER_CHANEG_ACCOUNT'], reply_markup=CHANGE_ACCOUNT()
        )
        return 
    

    await query.edit_message_text(
        text=HOME_MESSAGE['GET_ACCOUNT'], reply_markup=BACK()
    )

    # On Listen Get Account 
    try:
        data = await app.listen(chat_id=query.message.chat.id, filters=filters.text & filters.private, timeout=60)
    except ListenerTimeout as e:
        return
    database.UPDATE_TEMP('onListen', True)
            
    if database.GET_TEMP('onListen') == False:
        return
    message_data = await app.send_message(
        chat_id=query.message.chat.id, text=HOME_MESSAGE['WITH_CHEAK_ACCOUNT']
    )

    SessionString  = data.text
    # check session 
    sessionClient = Client(':memory:', api_hash=config.API_HASH, api_id=config.API_ID,session_string=SessionString ,in_memory=True)
    try :
        await sessionClient.connect()
        Clientdata = await sessionClient.get_me()
    except Exception as e:
        await query.edit_message_text(
        chat_id=query.message.chat.id,message_id=message_data.id,  
            text=HOME_MESSAGE['ACCOUNT_ERROR'], 
            reply_markup=BACK()
        )
        await sessionClient.disconnect()
        return
    
    datas['status']['account'] = True
    datas['data']['account'] = {'session':SessionString, 'first_name':Clientdata.first_name, 'username':Clientdata.username, 'id':Clientdata.id, 'status':True}
    database.UPDATE_DATA(datas)

    await sessionClient.disconnect()
    await app.edit_message_text(
        chat_id=query.message.chat.id,message_id=message_data.id,  
        text=HOME_MESSAGE['DONE_ADD_ACCOUNT'], reply_markup=BACK()
    )
    

# ON ON_CHANGE_ACCOUNT
@Client.on_callback_query(filters.regex('^ON_CHANGE_ACCOUNT$'))
async def ON_CHANGE_ACCOUNT(app: Client, query: types.CallbackQuery):
    datas = database.GET_DATA()

    await query.edit_message_text(
        text=HOME_MESSAGE['GET_ACCOUNT'], reply_markup=BACK()
    )
    database.UPDATE_TEMP('onListen', True)
    # On Listen Get Account 
    try:
        data = await app.listen(chat_id=query.message.chat.id, filters=filters.text & filters.private, timeout=60)
    except ListenerTimeout as e:
        return
        
    if database.GET_TEMP('onListen') == False:
        return

    message_data = await app.send_message(
        chat_id=query.message.chat.id, text=HOME_MESSAGE['WITH_CHEAK_ACCOUNT']
    )

    SessionString  = data.text
    # check session 
    sessionClient = Client(':memory:', api_hash=config.API_HASH, api_id=config.API_ID,session_string=SessionString ,in_memory=True)
    try :
        await sessionClient.connect()
        Clientdata = await sessionClient.get_me()
    except Exception as e:
        await query.edit_message_text(
        chat_id=query.message.chat.id,message_id=message_data.id,  
            text=HOME_MESSAGE['ACCOUNT_ERROR'], 
            reply_markup=BACK()
        )
        await sessionClient.disconnect()
        return
    
    datas['data']['account'] = {'session':SessionString, 'first_name':Clientdata.first_name, 'username':Clientdata.username, 'id':Clientdata.id}
    database.UPDATE_DATA(datas)

    await sessionClient.disconnect()
    await app.edit_message_text(
        chat_id=query.message.chat.id,message_id=message_data.id,  
        text=HOME_MESSAGE['DONE_ADD_ACCOUNT'], reply_markup=BACK()
    )
    


# Messag Sitteng
@Client.on_callback_query(filters.regex('^MESSAGE_MANGER$'))
async def ON_MESSAGE_MANGER(app: Client, query: types.CallbackQuery):
    datas = database.GET_DATA()
    if datas['status']['message'] == True:
        await query.edit_message_text(
            text=HOME_MESSAGE['VER_EDIT_MESSAGE'].format(datas['data']['message']), reply_markup=VER_EDIT_MESSAGE()
        )
        return
    
    await query.edit_message_text(
        text=HOME_MESSAGE['GET_MESSAGE'], reply_markup=BACK()
    )
    database.UPDATE_TEMP('onListen', True)

    try:
        data = await app.listen(chat_id=query.message.chat.id, filters=filters.text & filters.private, timeout=60)
    except ListenerTimeout as e:
        return
    
    if database.GET_TEMP('onListen') == False:
        return

    datas['status']['message'] = True
    datas['data']['message'] = data.text
    database.UPDATE_DATA(datas)

    # Done Edit 
    await app.send_message(
        chat_id=query.message.chat.id , text=HOME_MESSAGE['DONE_ADD_MESSAGE_TEXT'], 
        reply_markup=BACK()
    )

# ON Change MEssage 
@Client.on_callback_query(filters.regex('^ON_CHANGE_MESSAGE$'))
async def ON_CHANGE_MESSAGE(app: Client, query: types.CallbackQuery):
    datas = database.GET_DATA()
    await query.edit_message_text(
        text=HOME_MESSAGE['GET_MESSAGE'], reply_markup=BACK()
    )
    database.UPDATE_TEMP('onListen', True)

    try:
        data = await app.listen(chat_id=query.message.chat.id, filters=filters.text & filters.private, timeout=60)
    except ListenerTimeout as e:
        return
    
    if database.GET_TEMP('onListen') == False:
        return

    datas['data']['message'] = data.text
    database.UPDATE_DATA(datas)
    # Done Edit 
    await app.send_message(
        chat_id=query.message.chat.id , text=HOME_MESSAGE['DONE_ADD_MESSAGE_TEXT'], 
        reply_markup=BACK()
    )


# Time Manger 
@Client.on_callback_query(filters.regex('^TIME_MANGER$'))
async def ON_MANGER_TIME_(app :Client, query: types.CallbackQuery):
    datas = database.GET_DATA()
    if datas['status']['time'] == True:
        await query.edit_message_text(
            text=HOME_MESSAGE['VER_EDIT_TIME'], reply_markup=VER_EDIT_TIME()
        )
        return
    await query.edit_message_text(
        text=HOME_MESSAGE['GET_TIME'], reply_markup=BACK()
    )


    database.UPDATE_TEMP('onListen', True)

    try:
        data = await app.listen(chat_id=query.message.chat.id, filters=filters.text & filters.private, timeout=60)
    except ListenerTimeout as e:
        return
    
    if database.GET_TEMP('onListen') == False:
        return
    
    if not data.text.isdigit:
        await app.send_message(
            chat_id=query.message.chat.id, text=HOME_MESSAGE['ERROR_GET_TIME'], reply_markup=BACK())
        return
    
    # Add Time  On 
    datas['status']['time'] = True
    datas['data']['time'] = int(data.text)
    database.UPDATE_DATA(datas)

    await app.send_message(
        chat_id=query.message.chat.id,text=HOME_MESSAGE['DONE_EDIT_TIME'], reply_markup=BACK()
    )

@Client.on_callback_query(filters.regex('^ON_CHANGE_TIME$'))
async def ON_CHANGE_TIME(app :Client, query: types.CallbackQuery):
    datas = database.GET_DATA()
       
    await query.edit_message_text(
        text=HOME_MESSAGE['GET_TIME'], reply_markup=BACK()
    )


    database.UPDATE_TEMP('onListen', True)

    try:
        data = await app.listen(chat_id=query.message.chat.id, filters=filters.text & filters.private, timeout=60)
    except ListenerTimeout as e:
        return
    
    if database.GET_TEMP('onListen') == False:
        return
    
    if not data.text.isdigit:
        await app.send_message(
            chat_id=query.message.chat.id, text=HOME_MESSAGE['ERROR_GET_TIME'], reply_markup=BACK())
        return
    
    # Add Time  On 
    datas['data']['time'] = int(data.text)
    database.UPDATE_DATA(datas)

    await app.send_message(
        chat_id=query.message.chat.id,text=HOME_MESSAGE['DONE_EDIT_TIME'], reply_markup=BACK()
    )


@Client.on_callback_query(filters.regex('^SHOWMESSAGE$'))
async def ON_SHOWMESSAGE(app :Client, query: types.CallbackQuery):
    datas = database.GET_DATA()
    await query.answer(text='↫ : الرسالة : {}'.format(datas['data']['message']), show_alert=True)