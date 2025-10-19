# encoding: utf-8
from mongoengine import Document, StringField, DateTimeField, DateField, ReferenceField
from datetime import datetime


class BrandType(Document):
    """
    Brand Type model
    """
    name = StringField(unique=True)
    desc = StringField()
    onsale_at = DateField()

    # Relationships
    brand = ReferenceField('Brand')

    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'brand_types',
        'strict': False
    }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(BrandType, self).save(*args, **kwargs)
