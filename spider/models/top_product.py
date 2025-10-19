# encoding: utf-8
from mongoengine import Document, StringField, IntField, DateTimeField
from datetime import datetime


class TopProduct(Document):
    """
    Top Product model (highest level in product hierarchy)
    """
    name = StringField(unique=True)
    order_num = IntField(default=0)

    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'top_products',
        'strict': False
    }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(TopProduct, self).save(*args, **kwargs)
