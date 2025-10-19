# encoding: utf-8
from mongoengine import Document, StringField, DateTimeField, ReferenceField
from datetime import datetime


class MiddleProduct(Document):
    """
    Middle Product model (mid-level in product hierarchy)
    """
    name = StringField(unique=True)

    # Relationships
    top_product = ReferenceField('TopProduct')

    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'middle_products',
        'strict': False
    }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(MiddleProduct, self).save(*args, **kwargs)
