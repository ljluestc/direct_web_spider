# encoding: utf-8
from mongoengine import EmbeddedDocument, StringField, IntField, DateTimeField


class Comment(EmbeddedDocument):
    """
    Comment embedded document (embedded in Product)
    """
    title = StringField()
    content = StringField()
    author_name = StringField()
    star = IntField()
    publish_at = DateTimeField()

    meta = {
        'strict': False
    }
