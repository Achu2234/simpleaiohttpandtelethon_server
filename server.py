from asyncio import events
from aiohttp import web
from telethon import TelegramClient
from config import Clients as VAR
from templates import Templates
from aiohttp.web import Response as render
from aiohttp.web import json_response as jsonr
# from aiohttp.web import Request
from helper import Database, Xrypto
import os

db = Database()
crypto = Xrypto()

# crypto.NewKey(1024) //uncomment for first time
crypto.importKeyFiles('./.rsa_keys/public.pem', './.rsa_keys/private.pem') 
temp = Templates()
client = TelegramClient('sess',VAR.API_ID, VAR.API_HASH)
client.start(bot_token=VAR.BOT_TOKEN)
loop = client.loop

requests = web.RouteTableDef()


@requests.get("/")
async def home(_):
    me = await client.get_me()
    print(me.username)
    return temp.home

@requests.get("/login")
async def login(request):

    try:
        chat =   request.rel_url.query['chat']
        mess_id = request.rel_url.query['mess_id']
        mess_id_ = crypto.decrypt(mess_id)
        mess_id_ = int(mess_id_)
        chat_ = crypto.decrypt(chat)
        chat_ = chat_ if not chat_.isdigit() else int(chat_)


        await client.edit_message(chat_, mess_id_, "Verification in process")

        if not db.ultra('users', chat_):

            return temp.login(chat=chat,mess_id=mess_id)
        else:
            return temp.already
    except Exception as e:
        return render(text=str(e), status=400)



@requests.get("/verified")
async def verified(request):

    try:
        chat =   request.rel_url.query['chat']
        mess_id = request.rel_url.query['mess_id']
        mess_id_ = crypto.decrypt(mess_id)
        mess_id_ = int(mess_id_)
        chat_ = crypto.decrypt(chat)
        chat_ = chat_ if not chat_.isdigit() else int(chat_)
        await client.edit_message(chat_, mess_id_, "Now you are verified")
        return temp.verified({'name_id': chat})
    except Exception as e:
        return render(text=str(e), status=400)
    

@requests.get("/sw.ja")
async def sw_js(_):
    return temp.swjs

@requests.post("/database")
async def get_data(data):
    data = await data.post()
    print(data)
    if 'token' in data:
        if db.is_token(data['token']):
            return jsonr(db.database) 
    return jsonr({"status": False}, status=400)

@requests.get("/generate")
async def generate(_):
    return render(text=crypto.encrypt(db.new_token))

@requests.get("/send")
async def send_message(req):
    try:
        chat  = req.rel_url.query['chat']
        chat = chat if not chat.isdigit() else int(chat)

        mess = req.rel_url.query['text']

        await client.send_message(chat,mess)
        return render(text="Message sent")
    except Exception as e:
        return render(text=str(e), status=400)


if __name__ == '__main__':
    print("Getting loop..")


    app = web.Application()
    app.add_routes(requests)

    print("Running..")
    exist = web.AppRunner(app)
    PORT = os.environ.get('PORT', 5000)
    loop.run_until_complete(exist.setup())
    start = web.TCPSite(exist, host='0.0.0.0', port=int(PORT))
    loop.run_until_complete(start.start())
    loop.run_forever()


    



