from os import environ as env

class Clients:
    API_ID: int
    API_HASH: str
    BOT_TOKEN: str

    def __init__(self):
        self.API_ID = 0
        self.BOT_TOKEN = ''
        self.API_HASH = ''

    def initenv(self):
        self.API_ID = int(env.get('API_ID',0))
        self.API_HASH = env.get('API_HASH', '')
        self.BOT_TOKEN = env.get('BOT_TOKEN', '')

    def init(self, API_ID: int, API_HASH: str, BOT_TOKEN: str):
        self.API_ID = API_ID
        self.API_HASH = API_HASH
        self.BOT_TOKEN = BOT_TOKEN



        


