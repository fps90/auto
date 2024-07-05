# Requier Methods And Modules
import json, os 


class Database:

    def __init__(self):
        # Data
        self.__PAT = './database/data.json'
        if not os.path.exists(self.__PAT):
            obj = {'temp':{}, 'status':{'account':False, 'message':False, 'time':False}, 'data':{'account':None, 'message':None, 'time':None}, 'chats':{}}
            json.dump(obj, open(self.__PAT, 'w'), indent=3)

    
    def GET_DATA(self):
        return json.load(open(self.__PAT, 'r'))
    
    def UPDATE_DATA(self, NEW_DATA: dict):
        return json.dump(NEW_DATA, open(self.__PAT, 'w'), indent=3)
    
    def GET_TEMP(self, key: str):
        data = self.GET_DATA()
        return data['temp'][key]
    
    def UPDATE_TEMP(self, key: str, values):
        data = self.GET_DATA()
        data['temp'].update({key: values})
        self.UPDATE_DATA(data)        