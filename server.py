from aiohttp import web
from telethon import TelegramClient
from config import Clients as VAR
from templates import Templates
from aiohttp.web import Response as render
# from aiohttp.web import Request
from helper import Database, Xrypto


db = Database()
crypto = Xrypto()
# crypto.NewKey(512)
crypto.importKeyFiles('./.rsa_keys/public.pem', './.rsa_keys/private.pem')
temp = Templates()
client = TelegramClient('sess',VAR.API_ID, VAR.API_HASH)
client.start(bot_token=VAR.API_TOKEN_TEST)


requests = web.RouteTableDef()


@requests.get("/")
async def home(request):
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
    




def main():
    print("Getting loop..")
    loop = client.loop

    app = web.Application()
    app.add_routes(requests)

    print("Running..")
    exist = web.AppRunner(app)
    loop.run_until_complete(exist.setup())
    start = web.TCPSite(exist)
    loop.run_until_complete(start.start())
    loop.run_forever()


    

if __name__ == '__main__':
    main()


