"""
Comprehensive unit tests for spider.models.product_url
"""
import pytest
from datetime import datetime
from mongoengine import connect, disconnect
from spider.models.product_url import ProductUrl
from spider.models.page import Page


@pytest.mark.unit
@pytest.mark.model
@pytest.mark.unit
class TestProductUrlModel:
    """Test cases for ProductUrl model"""

    @pytest.fixture(autouse=True)
    def setup_db(self):
        """Setup test database"""
        connect('testdb', host='localhost', mongo_client_class=__import__('mongomock').MongoClient, alias='default')
        ProductUrl.drop_collection()
        Page.drop_collection()
        yield
        ProductUrl.drop_collection()
        Page.drop_collection()
        disconnect(alias='default')

    def test_product_url_creation(self):
        """Test ProductUrl creation"""
        product_url = ProductUrl(url="http://test.com/product/123", kind="dangdang")
        assert product_url is not None
        assert product_url.url == "http://test.com/product/123"
        assert product_url.kind == "dangdang"

    def test_product_url_save(self):
        """Test ProductUrl save"""
        product_url = ProductUrl(url="http://test.com/product/123", kind="dangdang")
        product_url.save()
        assert product_url.id is not None
        assert product_url.created_at is not None
        assert product_url.updated_at is not None

    def test_product_url_required_fields(self):
        """Test ProductUrl required fields"""
        product_url = ProductUrl()
        with pytest.raises(Exception):  # ValidationError
            product_url.save()

    def test_product_url_unique_url(self):
        """Test ProductUrl unique URL constraint"""
        ProductUrl(url="http://test.com/product/123", kind="dangdang").save()
        product_url2 = ProductUrl(url="http://test.com/product/123", kind="jingdong")
        with pytest.raises(Exception):  # NotUniqueError
            product_url2.save()

    def test_product_url_default_values(self):
        """Test ProductUrl default values"""
        product_url = ProductUrl(url="http://test.com/product/123")
        assert product_url.completed is False
        assert product_url.retry_time == 0

    def test_product_url_html_property_getter(self):
        """Test ProductUrl html property getter"""
        product_url = ProductUrl(url="http://test.com/product/123")
        assert product_url.html is None

    def test_product_url_html_property_setter(self):
        """Test ProductUrl html property setter"""
        product_url = ProductUrl(url="http://test.com/product/123")
        product_url.html = "<html><body>Product Page</body></html>"
        assert product_url.html == "<html><body>Product Page</body></html>"

    def test_product_url_html_not_persisted(self):
        """Test ProductUrl html is not persisted to database"""
        product_url = ProductUrl(url="http://test.com/product/123", kind="dangdang")
        product_url.html = "<html>product</html>"
        product_url.save()

        # Reload from database
        product_url_reloaded = ProductUrl.objects(url="http://test.com/product/123").first()
        assert product_url_reloaded.html is None

    def test_product_url_page_property_with_page(self):
        """Test ProductUrl page property when page exists"""
        page = Page(url="http://page.com", kind="dangdang")
        page.save()

        product_url = ProductUrl(url="http://test.com/product/123", kind="dangdang", page_id=page.id)
        product_url.save()

        assert product_url.page is not None
        assert product_url.page.id == page.id
        assert product_url.page.url == "http://page.com"

    def test_product_url_page_property_without_page(self):
        """Test ProductUrl page property when page_id is None"""
        product_url = ProductUrl(url="http://test.com/product/123", kind="dangdang")
        product_url.save()

        assert product_url.page is None

    def test_product_url_page_property_invalid_id(self):
        """Test ProductUrl page property with non-existent page_id"""
        from bson import ObjectId
        product_url = ProductUrl(url="http://test.com/product/123", kind="dangdang", page_id=ObjectId())
        product_url.save()

        assert product_url.page is None

    def test_product_url_from_kind_classmethod(self):
        """Test ProductUrl from_kind classmethod"""
        ProductUrl(url="http://dd1.com/p/1", kind="dangdang").save()
        ProductUrl(url="http://dd2.com/p/2", kind="dangdang").save()
        ProductUrl(url="http://jd1.com/p/1", kind="jingdong").save()

        dd_product_urls = list(ProductUrl.from_kind("dangdang"))
        assert len(dd_product_urls) == 2

        jd_product_urls = list(ProductUrl.from_kind("jingdong"))
        assert len(jd_product_urls) == 1

    def test_product_url_from_kind_empty_result(self):
        """Test ProductUrl from_kind with no matching results"""
        ProductUrl(url="http://test.com/p/1", kind="dangdang").save()

        results = list(ProductUrl.from_kind("nonexistent"))
        assert len(results) == 0

    def test_product_url_save_updates_timestamp(self):
        """Test ProductUrl save updates updated_at timestamp"""
        product_url = ProductUrl(url="http://test.com/product/123", kind="dangdang")
        product_url.save()

        original_updated = product_url.updated_at
        import time
        time.sleep(0.01)

        product_url.completed = True
        product_url.save()

        assert product_url.updated_at >= original_updated

    def test_product_url_completed_flag(self):
        """Test ProductUrl completed flag"""
        product_url = ProductUrl(url="http://test.com/product/123", kind="dangdang")
        assert product_url.completed is False

        product_url.completed = True
        product_url.save()

        product_url_reloaded = ProductUrl.objects(url="http://test.com/product/123").first()
        assert product_url_reloaded.completed is True

    def test_product_url_retry_time(self):
        """Test ProductUrl retry_time field"""
        product_url = ProductUrl(url="http://test.com/product/123", kind="dangdang")
        assert product_url.retry_time == 0

        product_url.retry_time = 5
        product_url.save()

        product_url_reloaded = ProductUrl.objects(url="http://test.com/product/123").first()
        assert product_url_reloaded.retry_time == 5

    def test_product_url_multiple_urls_same_kind(self):
        """Test multiple product URLs with same kind"""
        ProductUrl(url="http://test1.com/p/1", kind="dangdang").save()
        ProductUrl(url="http://test2.com/p/2", kind="dangdang").save()
        ProductUrl(url="http://test3.com/p/3", kind="dangdang").save()

        product_urls = list(ProductUrl.from_kind("dangdang"))
        assert len(product_urls) == 3
        urls = [pu.url for pu in product_urls]
        assert "http://test1.com/p/1" in urls
        assert "http://test2.com/p/2" in urls
        assert "http://test3.com/p/3" in urls

    def test_product_url_with_all_fields(self):
        """Test ProductUrl with all fields populated"""
        page = Page(url="http://page.com", kind="dangdang")
        page.save()

        product_url = ProductUrl(
            url="http://test.com/product/123",
            kind="dangdang",
            completed=True,
            retry_time=3,
            page_id=page.id
        )
        product_url.save()

        assert product_url.id is not None
        assert product_url.url == "http://test.com/product/123"
        assert product_url.kind == "dangdang"
        assert product_url.completed is True
        assert product_url.retry_time == 3
        assert product_url.page_id == page.id
        assert product_url.page.url == "http://page.com"

    def test_product_url_timestamps_on_creation(self):
        """Test ProductUrl timestamps are set on creation"""
        before = datetime.utcnow()
        product_url = ProductUrl(url="http://test.com/product/123", kind="dangdang")
        product_url.save()
        after = datetime.utcnow()

        assert before <= product_url.created_at <= after
        assert before <= product_url.updated_at <= after
