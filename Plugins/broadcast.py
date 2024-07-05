# Requier Modules 
from pyrogram import Client, filters, types
from threading import Timer
import asyncio 

# Requier Bot Plugins 
from Config import config, database,temp ,app as apps
from Plugins.helpers import *

async def SEND_MESSAGE(session: str, chat_id: str, msg: str):
    # Start Pyro Client
    clinets=  Client(':memory:', api_hash=config.API_HASH, api_id=config.API_ID, session_string=session, workers=2, no_updates=True)
    try:
        await clinets.connect()
    except Exception as e:
        return (False, 'CONNECT_ERROR')
    try:
        await clinets.join_chat(chat_id=chat_id)
    except Exception  as e:
        pass
    try:
        await clinets.send_message(chat_id=chat_id, text=msg)
    except Exception as e:
        #print(e)
        return (False, 'SEND_MESSAGE')
    return (True, None)

# Boradcats Finctions 
def BROAD_CAST():
    datas = database.GET_DATA()
    if not  temp['broadcast']:
        return
    
    if not datas['chats']:
        temp['broadcast'] = False
        try:
            asyncio.run(apps.send_message(
                chat_id=config.SUDO, text="↫ : تم ايقاف النشر بي سبب عدم توفر مجموعات"
            ))
        except:pass
        return

    if not datas['data']['account']['status']:
        temp['broadcast'] = False
        try:
            asyncio.run(apps.send_message(
                chat_id=config.SUDO, text="↫ : تم ايقاف النشر بي سبب عدم عمل الحساب يرجا التحقق من الحساب و اعادة المحاولا"
            ))
        except:pass
        return
    for i in datas['chats']:
        try:
            status = asyncio.run(SEND_MESSAGE(
                session=datas['data']['account']['session'], chat_id=i, msg=datas['data']['message']
            ))
            if status[0] == False:
                datas['data']['account']['status'] = False
                database.UPDATE_DATA(datas)

        except Exception as e:
            return
        
    Timer(database.GET_DATA()['data']['time'], BROAD_CAST).start()




# On Boradcats
@Client.on_callback_query(filters.regex('ON_broadcast'))
async def ON_broadcast(app: Client, query: types.CallbackQuery):
    status = database.GET_DATA()['status']
    if not status['account'] or not status['message'] or not status['time']:
        await query.edit_message_text(
            text=HOME_MESSAGE['ERROR_NO_DATA'], reply_markup=BACK()
        )
        return
    temp['broadcast'] = True if  temp['broadcast'] == False else False
    if temp['broadcast'] == True:
        await query.answer('تم تفعيل النشر ')
        Timer(2, BROAD_CAST).start()
         
    else:
        await query.answer('تم اايقاف النشر') 
    await query.edit_message_text(
        text=HOME_MESSAGE['HOME'], reply_markup=HONE_KEYBOARD()

    )

