# Bot Helpers 
from pyrogram import types
# Requier Bot COnfig 
from Config import database, temp
# ↫ : ❲ ❳

# Inline Keyboard 
def HONE_KEYBOARD():
    status =  database.GET_DATA()['status']
    data =  database.GET_DATA()['data']
    return types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton(text="❲ {} ❳".format('مفعل' if temp['broadcast'] else 'غير مفعل'), callback_data="ON_broadcast"),
            types.InlineKeyboardButton(text="❲ النشر ❳", callback_data="NONE")
        ],
        [
            types.InlineKeyboardButton(text="↫ : الحساب ❲ {} ❳".format(None if not status['account'] else data['account']['first_name']), url='t.me/None' if status['account'] == False else 't.me/{}'.format(data['account']['username']))
        ],
        [
            types.InlineKeyboardButton(text="↫ الرسالة: ❲ {} ❳".format(None if not status['message'] else data['message'][0:6] + '..'), callback_data="SHOWMESSAGE"),
            types.InlineKeyboardButton(text="↫ الوقت : ❲ {} ❳".format(0 if not status['time'] else data['time']), callback_data="NONETIME")
        ], 
        [
            types.InlineKeyboardButton(text="↫ : ❲ تعين حساب ❳" if status['account'] == False else '↫ : ❲ تغير حساب ❳', callback_data="ACCOUNT_MANGE"), 
            types.InlineKeyboardButton(text="↫ : ❲ تعين رسالة ❳" if status['message'] == False else "↫ : ❲ تغير رسالة ❳", callback_data="MESSAGE_MANGER")
        ], 
        [
            types.InlineKeyboardButton(text="↫ : ❲ تعين وقت ❳" if status['time'] == False else "↫ : ❲ تغير وقت ❳", callback_data="TIME_MANGER"), 
        ], 
        [
            types.InlineKeyboardButton(text="↫ : ❲  عرض المجموعات ❳", callback_data="SHOW_CHAT"), 
            types.InlineKeyboardButton(text="↫ : ❲ اضافة مجموعة ❳", callback_data="ADD_CHAT")
        ],[
            types.InlineKeyboardButton(text="❲ D E V ❳", url='t.me/r_afx')
        ]

    ])

# cheng Acount keybaord
def CHANGE_ACCOUNT():
    return types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton(text="❲ Back ❳", callback_data='back'), 
            types.InlineKeyboardButton(text="↫ : ❲ تغير ❳", callback_data="ON_CHANGE_ACCOUNT")
        ]
    ])

# ❲ Back ❳ keybaord 
def BACK():
    return types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton(text="❲ Back ❳", callback_data='back')
        ]
    ])

def VER_EDIT_MESSAGE():
    return types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton(text="❲ Back ❳", callback_data='back'), 
            types.InlineKeyboardButton(text="↫ : ❲ تغير ❳", callback_data="ON_CHANGE_MESSAGE")
        ]
    ])
    return

def VER_EDIT_TIME():
    return types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton(text="❲ Back ❳", callback_data='back'), 
            types.InlineKeyboardButton(text="↫ : ❲ تغير ❳", callback_data="ON_CHANGE_TIME")
        ]
    ])

# Show Chat Keyboard
def SHOW_CHAT():
    keybaord = []
    datas = database.GET_DATA()
    for i in datas['chats']:
        chat = datas['chats'][i]
        keybaord.append([
            types.InlineKeyboardButton(text=chat['first_name'], url=f't.me/{i}'), 
            types.InlineKeyboardButton(text=chat['id'], callback_data='NONE'), 
            types.InlineKeyboardButton(text="❲ حذف ❳", callback_data=f'delet_chat|{i}'), 
        ])

    if not keybaord:
        keybaord.append(
            [types.InlineKeyboardButton(text="❲ لا يوجد مجموعات ❳", callback_data='NONE'), ]
        )
    
    keybaord.append([
            types.InlineKeyboardButton(text="❲ Back ❳", callback_data='back'),
    ])
    return types.InlineKeyboardMarkup(keybaord)

# Bot Devs Radfx2 @R_AFX CH : @radfx2


# Messgae 
HOME_MESSAGE = {
    'HOME':
            u"↫ : اهلاً بك في بوت النشر التلقأي  "
            u""
            u"", 
    'GET_ACCOUNT':
            u"↫ : قم بي ارسال الجلسة"
            u"", 
    'WITH_CHEAK_ACCOUNT':
            u"↫ : انتضر جاري التحقق من الحساب"
            u"", 
    'ACCOUNT_ERROR':
            u"↫ : عذرن الجلسة غير صالحة "
            u"", 
    'DONE_ADD_ACCOUNT':
            u"↫ : تم تعين الحساب بي نجاح \n"
            u"↫ :"
            u"", 
    'VER_CHANEG_ACCOUNT':
            u"↫ : هل انتا متأكد من انك تريد تعين حساب جديد",
    'GET_MESSAGE':
            u"↫ : قم بي ارسال النص "
            u"", 
    'DONE_ADD_MESSAGE_TEXT':
            u"↫ : تم تعين رسالا جديدة  بي نجاح"
            u""
            u"",
    'VER_EDIT_MESSAGE':
            u"↫ : هل انتا متأكد من انك تريد تعين رسالا جديدة\n"
            u"↫ : الرسالا الحالية :  (`{}`)", 
    'GET_TIME':
            u"↫ : قم بي ارسال الوقت على شكل ارقام"
            u"",
    'ERROR_GET_TIME':
            u"↫ : قم بي اراسال الوقت بي شكل صحيح"
            u"", 

    'VER_EDIT_TIME':
            u"↫ : هل انتا متأكد من انك تريد تعدي وقت النشر"
            u"", 
    'DONE_EDIT_TIME':
            u"↫ : تم تعين وقت جديد بي نجاح"
            u"", 
    'GET_CHAT_USERNAME':
            u"↫ : قم بي ارسال معرف المجموعة \n\n↫ : Ex : @username" 
            u"",
    'WITH_CHECK_USERNAME':
            u"↫ : انتضر جاري التحقق من المعرف"
            u"", 
    'USERNAME_INVELD':
            u"↫ : معرف المجموعة غير صالح "
            u"",
    'CHAT_TYPE_INVELD':
            u"↫ : يمكنك اضافة مجموعات فقط " 
            u"",  

    'DONE_ADD_CHAT':
            u"↫ : تم اضافة مجموعة جديدة , عدد مجموعاتك الان : ❲ {} ❳"
            u"", 
    'SHOW_CHAT':
            u"↫ : اهلاً بك في قسم عرض المجموعات"
            u""
            u"",
    'WITH_DELETE_CHAT':
            u"↫ : انتضر جاري حذف المجموعة" 
            u"",  
    'ERROR_NO_DATA':
            u"↫ : عذرن لم تقم بي تعين البيانات الازمة"
            u"", 


}