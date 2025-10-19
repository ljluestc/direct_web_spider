"""
Comprehensive unit tests for spider.models.brand
"""
import pytest
from datetime import datetime
from mongoengine import connect, disconnect
from spider.models.brand import Brand


@pytest.mark.unit
@pytest.mark.model
@pytest.mark.unit
class TestBrandModel:
    """Test cases for Brand model"""

    @pytest.fixture(autouse=True)
    def setup_db(self):
        """Setup test database"""
        connect('testdb', host='localhost', mongo_client_class=__import__('mongomock').MongoClient, alias='default')
        Brand.drop_collection()
        yield
        Brand.drop_collection()
        disconnect(alias='default')

    def test_brand_creation(self):
        """Test Brand creation"""
        brand = Brand(name="Nike")
        assert brand is not None
        assert brand.name == "Nike"

    def test_brand_save(self):
        """Test Brand save"""
        brand = Brand(name="Adidas")
        brand.save()
        assert brand.id is not None
        assert brand.created_at is not None
        assert brand.updated_at is not None

    def test_brand_unique_name(self):
        """Test Brand unique name constraint"""
        Brand(name="Sony").save()
        brand2 = Brand(name="Sony")
        with pytest.raises(Exception):  # NotUniqueError
            brand2.save()

    def test_brand_with_all_fields(self):
        """Test Brand with all fields populated"""
        brand = Brand(
            name="Samsung",
            desc="Electronics manufacturer",
            service="Excellent customer service",
            brandurl="http://samsung.com",
            taobrandurl="http://taobao.com/samsung"
        )
        brand.save()

        assert brand.name == "Samsung"
        assert brand.desc == "Electronics manufacturer"
        assert brand.service == "Excellent customer service"
        assert brand.brandurl == "http://samsung.com"
        assert brand.taobrandurl == "http://taobao.com/samsung"

    def test_brand_save_updates_timestamp(self):
        """Test Brand save updates updated_at timestamp"""
        brand = Brand(name="Apple")
        brand.save()

        original_updated = brand.updated_at
        import time
        time.sleep(0.01)

        brand.desc = "Updated description"
        brand.save()

        assert brand.updated_at >= original_updated

    def test_brand_timestamps_on_creation(self):
        """Test Brand timestamps are set on creation"""
        before = datetime.utcnow()
        brand = Brand(name="LG")
        brand.save()
        after = datetime.utcnow()

        assert before <= brand.created_at <= after
        assert before <= brand.updated_at <= after

    def test_brand_query_by_name(self):
        """Test querying Brand by name"""
        Brand(name="Huawei").save()
        Brand(name="Xiaomi").save()

        brand = Brand.objects(name="Huawei").first()
        assert brand is not None
        assert brand.name == "Huawei"

    def test_brand_update_fields(self):
        """Test updating Brand fields"""
        brand = Brand(name="Oppo")
        brand.save()

        brand.desc = "Smartphone manufacturer"
        brand.brandurl = "http://oppo.com"
        brand.save()

        brand_reloaded = Brand.objects(name="Oppo").first()
        assert brand_reloaded.desc == "Smartphone manufacturer"
        assert brand_reloaded.brandurl == "http://oppo.com"

    def test_brand_delete(self):
        """Test deleting Brand"""
        brand = Brand(name="Vivo")
        brand.save()
        brand_id = brand.id

        brand.delete()

        brand_deleted = Brand.objects(id=brand_id).first()
        assert brand_deleted is None

    def test_brand_count(self):
        """Test counting Brand objects"""
        Brand(name="Brand1").save()
        Brand(name="Brand2").save()
        Brand(name="Brand3").save()

        count = Brand.objects.count()
        assert count == 3

    def test_brand_optional_fields(self):
        """Test Brand with only required fields"""
        brand = Brand(name="MinimalBrand")
        brand.save()

        assert brand.name == "MinimalBrand"
        assert brand.desc is None
        assert brand.service is None
        assert brand.brandurl is None
        assert brand.taobrandurl is None
