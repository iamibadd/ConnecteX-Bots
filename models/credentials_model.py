from pymodm import MongoModel, fields


class Credentials(MongoModel):
    username = fields.CharField(required=True)
    niche = fields.CharField(required=True)
    pack = fields.CharField(required=True)
    facebook = fields.CharField(required=True)
    facebook_password = fields.CharField(required=True)
    instagram = fields.CharField(required=True)
    instagram_password = fields.CharField(required=True)
    linkedin = fields.CharField(required=True)
    linkedin_password = fields.CharField(required=True)
    twitter = fields.CharField(required=True)
    twitter_password = fields.CharField(required=True)

    class Meta:
        final = True
