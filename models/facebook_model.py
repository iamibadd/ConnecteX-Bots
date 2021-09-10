from pymodm import MongoModel, fields


class Facebooks(MongoModel):
    email = fields.CharField(required=True)
    user = fields.CharField(required=True)
    package = fields.CharField(required=True)
    status = fields.CharField(required=True, default='Live')
    posts = fields.IntegerField(required=True)
    friends = fields.CharField(required=True)
    createdAt = fields.DateTimeField(required=True)
    updatedAt = fields.DateTimeField(required=True)

    class Meta:
        final = True


class Facebookposts(MongoModel):
    email = fields.CharField(required=True)
    user = fields.CharField(required=True)
    package = fields.CharField(required=True)
    post_details = fields.CharField(default='')
    createdAt = fields.DateTimeField(required=True)
    updatedAt = fields.DateTimeField(required=True)

    class Meta:
        final = True