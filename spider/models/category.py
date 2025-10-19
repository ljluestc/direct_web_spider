# encoding: utf-8
from mongoengine import Document, StringField, BooleanField, IntField, DateTimeField, ObjectIdField, QuerySet
from datetime import datetime


class Category(Document):
    """
    Category model with tree structure support.
    Mimics Ruby's Mongoid::Tree functionality.
    """
    url = StringField(required=True, unique=True)
    completed = BooleanField(default=False)
    name = StringField()
    kind = StringField()
    retry_time = IntField(default=0)

    # Tree structure fields
    parent_id = ObjectIdField()

    # Virtual attribute (not stored in database)
    _html = None

    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'categories',
        'strict': False,
        'indexes': [
            'url',
            'kind',
            'parent_id'
        ]
    }

    @property
    def html(self):
        return self._html

    @html.setter
    def html(self, value):
        self._html = value

    @property
    def parent(self):
        """Get parent category"""
        if self.parent_id:
            return Category.objects(id=self.parent_id).first()
        return None

    @parent.setter
    def parent(self, parent_category):
        """Set parent category"""
        if parent_category:
            self.parent_id = parent_category.id

    @property
    def children(self):
        """Get all child categories"""
        return Category.objects(parent_id=self.id)

    @property
    def is_leaf(self):
        """Check if this is a leaf node (no children)"""
        return Category.objects(parent_id=self.id).count() == 0

    @classmethod
    def from_kind(cls, kind):
        """Filter categories by kind"""
        return cls.objects(kind=kind)

    @classmethod
    def leaves(cls):
        """Get all leaf categories (no children)"""
        # Get all category IDs
        all_ids = set(str(cat.id) for cat in cls.objects.only('id'))
        # Get all parent IDs
        parent_ids = set(str(cat.parent_id) for cat in cls.objects(parent_id__ne=None).only('parent_id'))
        # Leaf IDs are those that are not parents
        leaf_ids = all_ids - parent_ids
        return cls.objects(id__in=leaf_ids)

    def move_children_to_parent(self):
        """Move all children to parent before deletion"""
        if self.parent_id:
            # Move children up one level
            for child in self.children:
                child.parent_id = self.parent_id
                child.save()
        else:
            # Remove parent from children (make them root nodes)
            for child in self.children:
                child.parent_id = None
                child.save()

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(Category, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.move_children_to_parent()
        return super(Category, self).delete(*args, **kwargs)
