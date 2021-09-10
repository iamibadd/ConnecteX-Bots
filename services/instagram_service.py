from pymodm import connect
from datetime import datetime
import sys

# if importing from another folders use append else insert
sys.path.append('../utils')
sys.path.append('../models')
from config import MONGODB_URL
from instagram_model import Instagrams

connect(MONGODB_URL, tls=True, tlsAllowInvalidCertificates=True)


def record_instagram(username, package, followers, follow_requests):
    try:
        user = dict(Instagrams.objects.values().get({'username': username}))
        if followers is None:
            follow_requests = follow_requests + user.get('follow_requests')
            return Instagrams.objects.raw({'username': username}).update(
                {'$set': {'follow_requests': follow_requests, 'updatedAt': datetime.now()}})
        elif follow_requests is None:
            followers_gained = followers - user.get('followers')
            if followers == followers_gained:
                followers_gained = 0
            return Instagrams.objects.raw({'username': username}).update(
                {'$set': {'followers': followers, 'followers_gained': followers_gained, 'updatedAt': datetime.now()}})
    except:
        return Instagrams(username=username, package=package, followers=followers, follow_requests=0,
                          followers_gained=0, createdAt=datetime.now(), updatedAt=datetime.now()).save()
