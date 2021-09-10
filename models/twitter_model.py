from pymodm import MongoModel, fields


class Twitters(MongoModel):
    username = fields.CharField(required=True)
    user = fields.CharField(required=True)
    package = fields.CharField(required=True)
    status = fields.CharField(required=True, default='Live')
    posts = fields.IntegerField(required=True)
    followers = fields.IntegerField(required=True)
    followers_gained = fields.IntegerField(required=True)
    follow_requests = fields.IntegerField(required=True)
    createdAt = fields.DateTimeField(required=True)
    updatedAt = fields.DateTimeField(required=True)

    class Meta:
        final = True


class Twitterposts(MongoModel):
    username = fields.CharField(required=True)
    user = fields.CharField(required=True)
    package = fields.CharField(required=True)
    post_details = fields.CharField(default='')
    createdAt = fields.DateTimeField(required=True)
    updatedAt = fields.DateTimeField(required=True)

    class Meta:
        final = True
