from pymodm import connect
from datetime import datetime
import sys

# if importing from another folders use append else insert
sys.path.append('../utils')
sys.path.append('../models')
from config import MONGODB_URL
from twitter_model import Twitters, Twitterposts

connect(MONGODB_URL, tls=True, tlsAllowInvalidCertificates=True)


def record_twitter(username, followers, follow_requests, package, post):
    try:
        user = dict(Twitters.objects.values().get({'username': username}))
        if followers is None and post is None:
            follow_requests = follow_requests + user.get('follow_requests')
            return Twitters.objects.raw({'username': username}).update(
                {'$set': {'follow_requests': follow_requests, 'updatedAt': datetime.now()}})
        elif follow_requests is None and post is None:

            followers_gained = followers - user.get('followers')
            if followers == followers_gained:
                followers_gained = 0
            return Twitters.objects.raw({'username': username}).update(
                {'$set': {'followers': followers, 'followers_gained': followers_gained, 'updatedAt': datetime.now()}})
        elif follow_requests is None and followers is None:
            posts = user.get('posts') + 1
            return Twitters.objects.raw({'username': username}).update(
                {'$set': {'posts': posts, 'updatedAt': datetime.now()}})
    except Exception as e:
        print(e)
        return Twitters(username=username, package=package, posts=1, followers=0, createdAt=datetime.now(),
                        updatedAt=datetime.now()).save()


def record_twitter_posts(user, username, post, package):
    return Twitterposts(user=user, username=username, package=package, post_details=post, createdAt=datetime.now(),
                        updatedAt=datetime.now()).save()
