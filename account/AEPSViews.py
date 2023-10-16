import calendar
from django.shortcuts import render, redirect
from .models import Account, UserProfile, Role, Scheme, Company, APIManager, Provider, Commission, CommissionType, Reports
from django.contrib import auth
from lib.settings import password_check
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import uuid, requests
import time
import datetime
import random
import jwt
from py3rijndael import Rijndael
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
# from Crypto.Cipher import AES
class Token:
    def __init__(self):
        self.bs = AES.block_size
        self.prtnerid = "PS001536"
        self.jwt_key = "UFMwMDE1MzYwYzdiNTVkZTUyNjUxOTE4NDVmMmYzZjFjMzUwMTZiZA=="
        self.aesek = b"355ba8f41f2c7419"
        self.aesei = b"d024f4a22366238a"
        

    def JsonWebTokenGenerator(self):
        presentDate = datetime.datetime.now()
        unix_timestamp = datetime.datetime.timestamp(presentDate)*1000
        req_id = random.randint(00000000, 99999999)
        data = { 
        'timestamp': int(unix_timestamp), 
        'partnerId': self.prtnerid, 
        'reqid': req_id 
        }
        print(data)
        encoded = jwt.encode(data, self.jwt_key.encode('utf-8'), algorithm='HS256')
        return encoded
    def JsonWebTokenGeneratorForPayload(self, data):
        presentDate = datetime.datetime.now()
        unix_timestamp = datetime.datetime.timestamp(presentDate)*1000
        req_id = random.randint(00000000, 99999999)
        
        print(data)
        encoded = jwt.encode(data, 'secret', algorithm='HS256')
        return encoded

    def EncryptStringToBytes(self, data):
        raw = self._pad(data)
        key = self.aesek
        iv = self.aesei
        # data= pad(data.encode(),16)
        # cipher = AES.new(key.encode('utf-8'),AES.MODE_CBC,iv.encode("utf-8"))
        # return base64.b64encode(cipher.encrypt(data))
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return b64encode(cipher.encrypt(raw.encode()))
    
    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
    

    






