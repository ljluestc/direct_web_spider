# encoding: utf-8
from mongoengine import (Document, StringField, IntField, DecimalField, ListField,
                         DateTimeField, ObjectIdField, ReferenceField, EmbeddedDocumentListField)
from datetime import datetime
from spider.models.comment import Comment


class Product(Document):
    """
    Product model - represents a parsed product with all details
    """
    price = DecimalField(precision=2)
    price_url = StringField()
    title = StringField()
    stock = IntField()
    kind = StringField()
    image_url = StringField()
    desc = StringField()
    image_info = ListField()
    score = IntField()
    standard = StringField()
    product_code = StringField()
    product_url_id = ObjectIdField()

    # Relationships
    merchant = ReferenceField('Merchant')
    brand = ReferenceField('Brand')
    end_product = ReferenceField('EndProduct')
    brand_type = ReferenceField('BrandType')

    # Embedded documents
    comments = EmbeddedDocumentListField(Comment)

    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'products',
        'strict': False,
        'indexes': [
            'kind',
            'product_url_id',
            'brand',
            'merchant'
        ]
    }

    @property
    def product_url(self):
        """Get associated product URL"""
        if self.product_url_id:
            from spider.models.product_url import ProductUrl
            return ProductUrl.objects(id=self.product_url_id).first()
        return None

    @classmethod
    def from_kind(cls, kind):
        """Filter products by kind"""
        return cls.objects(kind=kind)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(Product, self).save(*args, **kwargs)
