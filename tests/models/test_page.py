"""
Comprehensive unit tests for spider.models.page
"""
import pytest
from datetime import datetime
from mongoengine import connect, disconnect
from spider.models.page import Page
from spider.models.category import Category


@pytest.mark.unit
@pytest.mark.model
@pytest.mark.unit
class TestPageModel:
    """Test cases for Page model"""

    @pytest.fixture(autouse=True)
    def setup_db(self):
        """Setup test database"""
        connect('testdb', host='localhost', mongo_client_class=__import__('mongomock').MongoClient, alias='default')
        Page.drop_collection()
        Category.drop_collection()
        yield
        Page.drop_collection()
        Category.drop_collection()
        disconnect(alias='default')

    def test_page_creation(self):
        """Test Page creation"""
        page = Page(url="http://test.com/page", kind="dangdang")
        assert page is not None
        assert page.url == "http://test.com/page"
        assert page.kind == "dangdang"

    def test_page_save(self):
        """Test Page save"""
        page = Page(url="http://test.com/page", kind="dangdang")
        page.save()
        assert page.id is not None
        assert page.created_at is not None
        assert page.updated_at is not None

    def test_page_required_fields(self):
        """Test Page required fields"""
        page = Page()
        with pytest.raises(Exception):  # ValidationError
            page.save()

    def test_page_unique_url(self):
        """Test Page unique URL constraint"""
        Page(url="http://test.com/page", kind="dangdang").save()
        page2 = Page(url="http://test.com/page", kind="jingdong")
        with pytest.raises(Exception):  # NotUniqueError
            page2.save()

    def test_page_default_values(self):
        """Test Page default values"""
        page = Page(url="http://test.com/page")
        assert page.completed is False
        assert page.retry_time == 0

    def test_page_html_property_getter(self):
        """Test Page html property getter"""
        page = Page(url="http://test.com/page")
        assert page.html is None

    def test_page_html_property_setter(self):
        """Test Page html property setter"""
        page = Page(url="http://test.com/page")
        page.html = "<html><body>Test</body></html>"
        assert page.html == "<html><body>Test</body></html>"

    def test_page_html_not_persisted(self):
        """Test Page html is not persisted to database"""
        page = Page(url="http://test.com/page", kind="dangdang")
        page.html = "<html>test</html>"
        page.save()

        # Reload from database
        page_reloaded = Page.objects(url="http://test.com/page").first()
        assert page_reloaded.html is None

    def test_page_category_property_with_category(self):
        """Test Page category property when category exists"""
        cat = Category(url="http://cat.com", name="Electronics", kind="dangdang")
        cat.save()

        page = Page(url="http://test.com/page", kind="dangdang", category_id=cat.id)
        page.save()

        assert page.category is not None
        assert page.category.id == cat.id
        assert page.category.name == "Electronics"

    def test_page_category_property_without_category(self):
        """Test Page category property when category_id is None"""
        page = Page(url="http://test.com/page", kind="dangdang")
        page.save()

        assert page.category is None

    def test_page_category_property_invalid_id(self):
        """Test Page category property with non-existent category_id"""
        from bson import ObjectId
        page = Page(url="http://test.com/page", kind="dangdang", category_id=ObjectId())
        page.save()

        assert page.category is None

    def test_page_from_kind_classmethod(self):
        """Test Page from_kind classmethod"""
        Page(url="http://dd1.com", kind="dangdang").save()
        Page(url="http://dd2.com", kind="dangdang").save()
        Page(url="http://jd1.com", kind="jingdong").save()

        dd_pages = list(Page.from_kind("dangdang"))
        assert len(dd_pages) == 2

        jd_pages = list(Page.from_kind("jingdong"))
        assert len(jd_pages) == 1

    def test_page_from_kind_empty_result(self):
        """Test Page from_kind with no matching results"""
        Page(url="http://test.com", kind="dangdang").save()

        results = list(Page.from_kind("nonexistent"))
        assert len(results) == 0

    def test_page_save_updates_timestamp(self):
        """Test Page save updates updated_at timestamp"""
        page = Page(url="http://test.com/page", kind="dangdang")
        page.save()

        original_updated = page.updated_at
        import time
        time.sleep(0.01)

        page.completed = True
        page.save()

        assert page.updated_at >= original_updated

    def test_page_completed_flag(self):
        """Test Page completed flag"""
        page = Page(url="http://test.com/page", kind="dangdang")
        assert page.completed is False

        page.completed = True
        page.save()

        page_reloaded = Page.objects(url="http://test.com/page").first()
        assert page_reloaded.completed is True

    def test_page_retry_time(self):
        """Test Page retry_time field"""
        page = Page(url="http://test.com/page", kind="dangdang")
        assert page.retry_time == 0

        page.retry_time = 3
        page.save()

        page_reloaded = Page.objects(url="http://test.com/page").first()
        assert page_reloaded.retry_time == 3

    def test_page_multiple_pages_same_kind(self):
        """Test multiple pages with same kind"""
        Page(url="http://test1.com", kind="dangdang").save()
        Page(url="http://test2.com", kind="dangdang").save()
        Page(url="http://test3.com", kind="dangdang").save()

        pages = list(Page.from_kind("dangdang"))
        assert len(pages) == 3
        urls = [p.url for p in pages]
        assert "http://test1.com" in urls
        assert "http://test2.com" in urls
        assert "http://test3.com" in urls

    def test_page_with_all_fields(self):
        """Test Page with all fields populated"""
        cat = Category(url="http://cat.com", name="Books", kind="dangdang")
        cat.save()

        page = Page(
            url="http://test.com/page",
            kind="dangdang",
            completed=True,
            retry_time=2,
            category_id=cat.id
        )
        page.save()

        assert page.id is not None
        assert page.url == "http://test.com/page"
        assert page.kind == "dangdang"
        assert page.completed is True
        assert page.retry_time == 2
        assert page.category_id == cat.id
        assert page.category.name == "Books"

    def test_page_timestamps_on_creation(self):
        """Test Page timestamps are set on creation"""
        before = datetime.utcnow()
        page = Page(url="http://test.com/page", kind="dangdang")
        page.save()
        after = datetime.utcnow()

        assert before <= page.created_at <= after
        assert before <= page.updated_at <= after
