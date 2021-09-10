from pymodm import connect
from datetime import datetime
import sys

# if importing from another folders use append else insert
sys.path.append('../utils')
sys.path.append('../models')
from config import MONGODB_URL
from credentials_model import Credentials

connect(MONGODB_URL, tls=True, tlsAllowInvalidCertificates=True)


def get_user(username):
    return dict(Credentials.objects.values().get({'username': username}))

# password = 'twitter_password'
# hashed = (get_user('username')['twitter_password']).encode('utf-8')
# print(bcrypt.hashpw(hashed, bcrypt.gensalt()))
# if bcrypt.hashpw(password.encode('utf-8'), hashed) == hashed:
#     print("It Matches!")
# else:
#     print("It Does not Match :(")
