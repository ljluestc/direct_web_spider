# encoding: utf-8
from mongoengine import (Document, StringField, IntField, DecimalField, FloatField,
                         ListField, DateTimeField, ObjectIdField, ReferenceField,
                         EmbeddedDocumentListField)
from datetime import datetime
from spider.models.comment import Comment


class Body(Document):
    """
    Body model - alternative product storage model
    """
    price = DecimalField(precision=2)
    price_url = StringField()
    title = StringField()
    stock = IntField()
    kind = StringField()
    image_url = StringField()
    text_info = StringField()
    image_info = ListField()
    score = FloatField()
    standard = StringField()
    product_id = ObjectIdField()

    # Relationships
    product = ReferenceField('Product')

    # Embedded documents
    comments = EmbeddedDocumentListField(Comment)

    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'bodies',
        'strict': False,
        'indexes': [
            'kind',
            'product_id'
        ]
    }

    @classmethod
    def from_kind(cls, kind):
        """Filter bodies by kind"""
        return cls.objects(kind=kind)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(Body, self).save(*args, **kwargs)
