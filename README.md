## simpleaiohttpandtelethon_server
Web server with aiohttp and telethon

**Available**
```text
GET / -> text
GET /login chat=chat_id(encrypted) mess_id=message_id(unencrypted) -> login.html
GET /verified chat=chat_id(encrypted) mess_id=message_id(unencrypted) -> verified.html
POST /database token=decrypted token --> full database as json
GET /sw.js -> sw.js
GET /generate -> encrypted token
GET /send chat=chat text=text -> text
```


