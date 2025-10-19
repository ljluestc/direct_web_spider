"""
Comprehensive unit tests for spider.models.category
"""
import pytest
from datetime import datetime
from mongoengine import connect, disconnect
from spider.models.category import Category


@pytest.mark.unit
@pytest.mark.model
@pytest.mark.unit
class TestCategoryModel:
    """Test cases for Category model"""

    @pytest.fixture(autouse=True)
    def setup_db(self):
        """Setup test database"""
        connect('testdb', host='localhost', mongo_client_class=__import__('mongomock').MongoClient, alias='default')
        Category.drop_collection()
        yield
        Category.drop_collection()
        disconnect(alias='default')

    def test_category_creation(self):
        """Test Category creation"""
        cat = Category(url="http://test.com", name="Test", kind="dangdang")
        assert cat is not None
        assert cat.url == "http://test.com"
        assert cat.name == "Test"
        assert cat.kind == "dangdang"

    def test_category_save(self):
        """Test Category save"""
        cat = Category(url="http://test.com", name="Test", kind="dangdang")
        cat.save()
        assert cat.id is not None
        assert cat.created_at is not None
        assert cat.updated_at is not None

    def test_category_required_fields(self):
        """Test Category required fields"""
        cat = Category()
        with pytest.raises(Exception):  # ValidationError
            cat.save()

    def test_category_unique_url(self):
        """Test Category unique URL constraint"""
        Category(url="http://test.com", name="Test1", kind="dangdang").save()
        cat2 = Category(url="http://test.com", name="Test2", kind="jingdong")
        with pytest.raises(Exception):  # NotUniqueError
            cat2.save()

    def test_category_default_values(self):
        """Test Category default values"""
        cat = Category(url="http://test.com")
        assert cat.completed is False
        assert cat.retry_time == 0

    def test_category_html_property(self):
        """Test Category html property"""
        cat = Category(url="http://test.com")
        assert cat.html is None
        cat.html = "<html>test</html>"
        assert cat.html == "<html>test</html>"

    def test_category_parent_property(self):
        """Test Category parent property"""
        parent = Category(url="http://parent.com", name="Parent", kind="dangdang")
        parent.save()

        child = Category(url="http://child.com", name="Child", kind="dangdang")
        child.parent_id = parent.id
        child.save()

        assert child.parent is not None
        assert child.parent.id == parent.id
        assert child.parent.name == "Parent"

    def test_category_parent_setter(self):
        """Test Category parent setter"""
        parent = Category(url="http://parent.com", name="Parent", kind="dangdang")
        parent.save()

        child = Category(url="http://child.com", name="Child", kind="dangdang")
        child.parent = parent
        child.save()

        assert child.parent_id == parent.id

    def test_category_children_property(self):
        """Test Category children property"""
        parent = Category(url="http://parent.com", name="Parent", kind="dangdang")
        parent.save()

        child1 = Category(url="http://child1.com", name="Child1", kind="dangdang", parent_id=parent.id)
        child1.save()

        child2 = Category(url="http://child2.com", name="Child2", kind="dangdang", parent_id=parent.id)
        child2.save()

        children = list(parent.children)
        assert len(children) == 2

    def test_category_is_leaf_property(self):
        """Test Category is_leaf property"""
        parent = Category(url="http://parent.com", name="Parent", kind="dangdang")
        parent.save()

        child = Category(url="http://child.com", name="Child", kind="dangdang", parent_id=parent.id)
        child.save()

        assert child.is_leaf is True
        assert parent.is_leaf is False

    def test_category_from_kind_classmethod(self):
        """Test Category from_kind classmethod"""
        Category(url="http://dd1.com", name="DD1", kind="dangdang").save()
        Category(url="http://dd2.com", name="DD2", kind="dangdang").save()
        Category(url="http://jd1.com", name="JD1", kind="jingdong").save()

        dd_cats = list(Category.from_kind("dangdang"))
        assert len(dd_cats) == 2

        jd_cats = list(Category.from_kind("jingdong"))
        assert len(jd_cats) == 1

    def test_category_leaves_classmethod(self):
        """Test Category leaves classmethod"""
        parent = Category(url="http://parent.com", name="Parent", kind="dangdang")
        parent.save()

        child1 = Category(url="http://child1.com", name="Child1", kind="dangdang", parent_id=parent.id)
        child1.save()

        child2 = Category(url="http://child2.com", name="Child2", kind="dangdang", parent_id=parent.id)
        child2.save()

        leaves = list(Category.leaves())
        assert len(leaves) == 2  # Only child1 and child2 are leaves

    def test_category_move_children_to_parent(self):
        """Test Category move_children_to_parent method"""
        grandparent = Category(url="http://gp.com", name="GP", kind="dangdang")
        grandparent.save()

        parent = Category(url="http://parent.com", name="Parent", kind="dangdang", parent_id=grandparent.id)
        parent.save()

        child = Category(url="http://child.com", name="Child", kind="dangdang", parent_id=parent.id)
        child.save()

        parent.move_children_to_parent()

        # Reload child
        child = Category.objects(id=child.id).first()
        assert child.parent_id == grandparent.id

    def test_category_move_children_to_parent_no_parent(self):
        """Test move_children_to_parent when category has no parent"""
        parent = Category(url="http://parent.com", name="Parent", kind="dangdang")
        parent.save()

        child = Category(url="http://child.com", name="Child", kind="dangdang", parent_id=parent.id)
        child.save()

        parent.move_children_to_parent()

        # Reload child
        child = Category.objects(id=child.id).first()
        assert child.parent_id is None

    def test_category_delete_moves_children(self):
        """Test Category delete moves children to parent"""
        grandparent = Category(url="http://gp.com", name="GP", kind="dangdang")
        grandparent.save()

        parent = Category(url="http://parent.com", name="Parent", kind="dangdang", parent_id=grandparent.id)
        parent.save()

        child = Category(url="http://child.com", name="Child", kind="dangdang", parent_id=parent.id)
        child.save()

        parent.delete()

        # Reload child
        child = Category.objects(id=child.id).first()
        assert child is not None
        assert child.parent_id == grandparent.id

    def test_category_save_updates_timestamp(self):
        """Test Category save updates updated_at timestamp"""
        cat = Category(url="http://test.com", name="Test", kind="dangdang")
        cat.save()

        original_updated = cat.updated_at
        import time
        time.sleep(0.01)

        cat.name = "Updated"
        cat.save()

        assert cat.updated_at >= original_updated

    def test_category_parent_none(self):
        """Test Category with no parent"""
        cat = Category(url="http://test.com", name="Test", kind="dangdang")
        cat.save()

        assert cat.parent is None
        assert cat.parent_id is None
