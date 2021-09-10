from pymodm import connect
from datetime import datetime
import sys

# if importing from another folders use append else insert
sys.path.append('../utils')
sys.path.append('../models')
from config import MONGODB_URL
from facebook_model import Facebooks, Facebookposts

connect(MONGODB_URL, tls=True, tlsAllowInvalidCertificates=True)


def record_facebook(email, friends, package):
    try:
        user = dict(Facebooks.objects.values().get({'email': email}))
        if friends is None:
            posts = user.get('posts') + 1
            return Facebooks.objects.raw({'email': email}).update(
                {'$set': {'posts': posts, 'updatedAt': datetime.now()}})
        else:
            return Facebooks.objects.raw({'email': email}).update(
                {'$set': {'friends': friends, 'updatedAt': datetime.now()}})
    except:
        return Facebooks(email=email, package=package, posts=1, friends=0,
                         createdAt=datetime.now(), updatedAt=datetime.now()).save()


def record_facebook_posts(user, email, post, package):
    return Facebookposts(user=user, email=email, package=package, post_details=post,
                         createdAt=datetime.now(), updatedAt=datetime.now()).save()
