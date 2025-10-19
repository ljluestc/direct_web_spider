# encoding: utf-8
from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField
from datetime import datetime


class Brand(Document):
    """
    Brand model
    """
    name = StringField(unique=True)
    desc = StringField()
    service = StringField()
    brandurl = StringField()
    taobrandurl = StringField()

    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'brands',
        'strict': False
    }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(Brand, self).save(*args, **kwargs)
