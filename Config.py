# Bot Config File 
# Requier Bot Modules 
from pyrogram import Client , enums
import os 
# Requier Database Modules Class 
from Utils.database import Database


# Bot Config
class config:
    API_KEY : str = "5204315005:AAFTcY_4CtLVdbN1d-NtQN752dRIdLUKIIA" # The API key or Bot Token
    API_HASH: str = "bf3e98d2c351e4ad06946b4897374a1e" # UsrBot Api Hash
    API_ID  : int = 8934899 # User Bot Api Id
    SUDO    : int = 6597393738 # Sudo Id
 


# Check Bot DIrctory
if not os.path.exists('./.session'): # Sesisons FIle 
    os.mkdir('./.session')


if not os.path.exists('./database'): #  Databesas FIle 
    os.mkdir('./database')


# Get Database 
database = Database()

# Temp status 
temp = {'broadcast':False}

# Start Pyrogram Client
app = Client(
    name="./.session/rad", 
    bot_token=config.API_KEY, 
    api_hash=config.API_HASH,
    api_id=config.API_ID, 
    plugins=dict(root="Plugins"), 
    parse_mode=enums.ParseMode.DEFAULT
)

