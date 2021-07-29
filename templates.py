import os
from string import Template
from aiohttp.web import Response
class Templates:

    HOME: str = "{'status': true}"
    LOGIN: str
    ALREADY: str
    VERIFIED : str
    SW_JS : str

    def __init__(self) -> None:
        os.chdir('./indexes')
        self.ALREADY = open("already.html", "r" ).read()
        self.LOGIN = open("login.html", "r").read()
        self.VERIFIED = open('verified.html', 'r').read()
        self.SW_JS = open("sw.js",'r').read()

    def login(self, **kargs):
        return Response(text=Template(self.LOGIN).safe_substitute(**kargs), content_type='text/html')

    def verified(self, name):
        return Response(text=Template(self.VERIFIED).safe_substitute(name), content_type='text/html')
    
    @property
    def home(self):
        return Response(text=self.HOME, content_type="text/html")

    @property
    def already(self):
        return Response(text=self.ALREADY, content_type='text/html')
    
    
     
    @property
    def swjs(self):
        return Response(text=self.SW_JS, content_type='text/javascript')

    
        
    
    


if __name__ == '__main__':
    temp = Templates()
    # print(temp.HOME % {'status': True})
    print(temp.login(1234))
    print(temp.verified("hello"))

    
    
