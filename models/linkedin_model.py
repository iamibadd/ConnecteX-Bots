from pymodm import MongoModel, fields


class Linkdelns(MongoModel):
    email = fields.CharField(required=True)
    user = fields.CharField(required=True)
    package = fields.CharField(required=True)
    posts = fields.IntegerField(required=True)
    connections = fields.IntegerField(required=True)
    requests = fields.IntegerField(required=True)
    gained = fields.IntegerField(required=True)
    createdAt = fields.DateTimeField(required=True)
    updatedAt = fields.DateTimeField(required=True)

    class Meta:
        final = True


class Linkedinposts(MongoModel):
    email = fields.CharField(required=True)
    user = fields.CharField(required=True)
    package = fields.CharField(required=True)
    post_details = fields.CharField(default='')
    createdAt = fields.DateTimeField(required=True)
    updatedAt = fields.DateTimeField(required=True)

    class Meta:
        final = True
