import logging as log
from typing import Union
import rsa
from base64 import  b64decode, b64encode
from os import path
from os import mkdir
from secrets import token_urlsafe
class InvalidKeyError(Exception):
    pass


class Database:
    database: dict
    def __init__(self) -> None:
        self.database = dict()

    def append(self, key, value):
        if key in self.database:
            log.debug(f"Append: {key} <-- {value}")
            self.database[key].append(value)
            return True
        else:
            log.debug(f"Init: {key} <- {value}")
            self.database[key] = [value]
            return True
    
            
    def getbykey(self, key) -> Union[list,bool]:
        if key in self.database:
            return self.database[key]
        else:
            return False

    def getlastbykey(self, key):
        if key in self.database:
            return self.database[key][-1]
        return False
    def ultra(self,key,value):
        if key in self.database:
            if value in self.database[key]:
                return True
            else:
                self.append(key, value)
                return False
        else:
            return False
    def is_token(self, token):
        if 'token' in self.database:
            if self.database['token'] == token:
                return True
            return False
        return False
    @property
    def new_token(self):
        token = token_urlsafe(64)
        self.database['token'] = token
        return token

    def find_bool(self, key, value):
        if key in self.database:
            if value in self.database[key]:
                return True
            return False
        return False

    def __repr__(self) -> str:
        return "{}".format(str(self.database))

class Xrypto:

     
    def __init__(self, PubKey=None, PrivateKey=None) -> None:
        self._PubKey = PubKey
        self._PrivateKey = PrivateKey

    def Hash(self):
        pass
        

    def importKey(self, privatekey, publickey):
        self._PubKey = publickey
        self._PrivateKey = privatekey

    def importKeyFiles(self, public: str, private: str):
        with open(public, 'rb') as f:
            pub = f.read()
            self._PubKey = rsa.PublicKey.load_pkcs1(pub)
        with open(private, 'rb') as f:
            piv = f.read()
            self._PrivateKey = rsa.PrivateKey.load_pkcs1(piv)
    def importKeyBytes(self, public: bytes, private: bytes):
        self._PrivateKey = rsa.PrivateKey.load_pkcs1(private)
        self._PubKey = rsa.PublicKey.load_pkcs1(public)

    
    def NewKey(self, key_length):
        assert key_length in [1024,2048,3072,4096]
        self._PubKey, self._PrivateKey = rsa.newkeys(key_length)

        if not path.exists('.rsa_keys'):
            mkdir('.rsa_keys')

        with open('.rsa_keys/private.pem', 'wb') as f:
            f.write(self._PrivateKey.save_pkcs1())

        with open('.rsa_keys/public.pem', 'wb') as f:
            f.write(self._PubKey.save_pkcs1())
        return self._PubKey, self._PrivateKey

    def encrypt(self, string: str):
        
        assert (self._PubKey is not None)
        _ = rsa.encrypt(string.encode(), self._PubKey)
        return b64encode(_).decode()

    def decrypt(self, string: str):

        assert (self._PrivateKey is not None)
        _ = b64decode(string)
        return rsa.decrypt(_, self._PrivateKey).decode()


if __name__ == '__main__':
    crypto = Xrypto()
    crypto.NewKey(int(input("1024,2048,3072,4096: ")))
    enc = crypto.encrypt("lrlhAaC9jEbywKTF5G8K28-DED2TW6ebhfxVuLKSmfsuXHu1bb3jQ_kGrAllGyD6LgiCTI7biG485HXY4eq8ug")
    print(enc)
    dec = crypto.decrypt(enc)
    print(dec)


        


        
        



# if __name__ == '__main__':
#     log.basicConfig(level=log.DEBUG)
#     db = Database()
#     db.append("key","valur")
#     print(db)
#     cp = Xrypto()
#     cp.NewKey(1024)
    

        
