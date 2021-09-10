from pymodm import connect
from datetime import datetime
import sys

# if importing from another folders use append else insert
sys.path.append('../utils')
sys.path.append('../models')
from config import MONGODB_URL
from linkedin_model import Linkdelns, Linkedinposts

connect(MONGODB_URL, tls=True, tlsAllowInvalidCertificates=True)


def record_linkedin(email, package, connections, requests):
    try:
        user = dict(Linkdelns.objects.values().get({'email': email}))
        if connections == 'None' and requests == 'None':
            return Linkdelns.objects.raw({'email': email}).update(
                {'$set': {'posts': user.get('posts') + 1, 'updatedAt': datetime.now()}})
        elif connections == 'None' and requests == 'Requesting':
            return Linkdelns.objects.raw({'email': email}).update(
                {'$set': {'requests': user.get('requests') + 1, 'updatedAt': datetime.now()}})
        else:
            return Linkdelns.objects.raw({'email': email}).update(
                {'$set': {'connections': connections,
                          'gained': user.get('gained') + (connections - user.get('connections')),
                          'updatedAt': datetime.now()}})
    except:
        return Linkdelns(email=email, package=package, posts=1, requests=0, connections=0, gained=0,
                         createdAt=datetime.now(), updatedAt=datetime.now()).save()


def record_linkedin_posts(user, email, post, package):
    return Linkedinposts(user=user, email=email, package=package, post_details=post,
                         createdAt=datetime.now(), updatedAt=datetime.now()).save()
