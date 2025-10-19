# encoding: utf-8
from mongoengine import Document, StringField, DateTimeField
from datetime import datetime


class Merchant(Document):
    """
    Merchant model
    """
    name = StringField(unique=True)
    desc = StringField()
    service = StringField()
    merchanturl = StringField()

    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'merchants',
        'strict': False
    }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(Merchant, self).save(*args, **kwargs)
