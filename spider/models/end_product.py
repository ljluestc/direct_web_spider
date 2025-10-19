# encoding: utf-8
from mongoengine import Document, StringField, DateTimeField, ReferenceField
from datetime import datetime


class EndProduct(Document):
    """
    End Product model (lowest level in product hierarchy)
    """
    name = StringField(unique=True)

    # Relationships
    middle_product = ReferenceField('MiddleProduct')

    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'end_products',
        'strict': False
    }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(EndProduct, self).save(*args, **kwargs)
