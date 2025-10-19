# encoding: utf-8
from mongoengine import Document, StringField, BooleanField, IntField, DateTimeField, ObjectIdField, ReferenceField
from datetime import datetime


class Page(Document):
    """
    Page model - represents a listing page with multiple products
    """
    url = StringField(required=True, unique=True)
    completed = BooleanField(default=False)
    kind = StringField()
    retry_time = IntField(default=0)
    category_id = ObjectIdField()

    # Virtual attribute (not stored in database)
    _html = None

    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'pages',
        'strict': False,
        'indexes': [
            'url',
            'kind',
            'completed',
            'category_id'
        ]
    }

    @property
    def html(self):
        return self._html

    @html.setter
    def html(self, value):
        self._html = value

    @property
    def category(self):
        """Get associated category"""
        if self.category_id:
            from spider.models.category import Category
            return Category.objects(id=self.category_id).first()
        return None

    @classmethod
    def from_kind(cls, kind):
        """Filter pages by kind"""
        return cls.objects(kind=kind)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(Page, self).save(*args, **kwargs)
