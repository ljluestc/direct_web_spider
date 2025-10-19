# encoding: utf-8
from mongoengine import Document, StringField, BooleanField, IntField, DateTimeField, ObjectIdField, ReferenceField
from datetime import datetime


class ProductUrl(Document):
    """
    ProductUrl model - represents a URL to a product page
    """
    url = StringField(required=True, unique=True)
    completed = BooleanField(default=False)
    kind = StringField()
    retry_time = IntField(default=0)
    page_id = ObjectIdField()

    # Virtual attribute (not stored in database)
    _html = None

    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'product_urls',
        'strict': False,
        'indexes': [
            'url',
            'kind',
            'completed',
            'page_id'
        ]
    }

    @property
    def html(self):
        return self._html

    @html.setter
    def html(self, value):
        self._html = value

    @property
    def page(self):
        """Get associated page"""
        if self.page_id:
            from spider.models.page import Page
            return Page.objects(id=self.page_id).first()
        return None

    @classmethod
    def from_kind(cls, kind):
        """Filter product URLs by kind"""
        return cls.objects(kind=kind)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(ProductUrl, self).save(*args, **kwargs)
