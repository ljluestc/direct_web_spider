"""
Comprehensive unit tests for spider.models.brand_type
"""
import pytest
from datetime import datetime, date
from mongoengine import connect, disconnect
from spider.models.brand_type import BrandType
from spider.models.brand import Brand


@pytest.mark.unit
@pytest.mark.model
@pytest.mark.unit
class TestBrandTypeModel:
    """Test cases for BrandType model"""

    @pytest.fixture(autouse=True)
    def setup_db(self):
        """Setup test database"""
        connect('testdb', host='localhost', mongo_client_class=__import__('mongomock').MongoClient, alias='default')
        BrandType.drop_collection()
        Brand.drop_collection()
        yield
        BrandType.drop_collection()
        Brand.drop_collection()
        disconnect(alias='default')

    def test_brand_type_creation(self):
        """Test BrandType creation"""
        brand_type = BrandType(name="iPhone 14")
        assert brand_type is not None
        assert brand_type.name == "iPhone 14"

    def test_brand_type_save(self):
        """Test BrandType save"""
        brand_type = BrandType(name="Galaxy S23")
        brand_type.save()
        assert brand_type.id is not None
        assert brand_type.created_at is not None
        assert brand_type.updated_at is not None

    def test_brand_type_unique_name(self):
        """Test BrandType unique name constraint"""
        BrandType(name="MacBook Pro").save()
        brand_type2 = BrandType(name="MacBook Pro")
        with pytest.raises(Exception):  # NotUniqueError
            brand_type2.save()

    def test_brand_type_with_brand_relationship(self):
        """Test BrandType with Brand relationship"""
        brand = Brand(name="Apple")
        brand.save()

        brand_type = BrandType(name="iPhone 15", brand=brand)
        brand_type.save()

        assert brand_type.brand is not None
        assert brand_type.brand.name == "Apple"
        assert brand_type.brand.id == brand.id

    def test_brand_type_with_all_fields(self):
        """Test BrandType with all fields populated"""
        brand = Brand(name="Samsung")
        brand.save()

        brand_type = BrandType(
            name="Galaxy S24",
            desc="Flagship smartphone",
            onsale_at=date(2024, 1, 15),
            brand=brand
        )
        brand_type.save()

        assert brand_type.name == "Galaxy S24"
        assert brand_type.desc == "Flagship smartphone"
        assert brand_type.onsale_at == date(2024, 1, 15)
        assert brand_type.brand.name == "Samsung"

    def test_brand_type_without_brand(self):
        """Test BrandType without Brand relationship"""
        brand_type = BrandType(name="Generic Type")
        brand_type.save()

        assert brand_type.brand is None

    def test_brand_type_save_updates_timestamp(self):
        """Test BrandType save updates updated_at timestamp"""
        brand_type = BrandType(name="Pixel 8")
        brand_type.save()

        original_updated = brand_type.updated_at
        import time
        time.sleep(0.01)

        brand_type.desc = "Updated description"
        brand_type.save()

        assert brand_type.updated_at >= original_updated

    def test_brand_type_timestamps_on_creation(self):
        """Test BrandType timestamps are set on creation"""
        before = datetime.utcnow()
        brand_type = BrandType(name="OnePlus 12")
        brand_type.save()
        after = datetime.utcnow()

        assert before <= brand_type.created_at <= after
        assert before <= brand_type.updated_at <= after

    def test_brand_type_query_by_name(self):
        """Test querying BrandType by name"""
        BrandType(name="Type1").save()
        BrandType(name="Type2").save()

        brand_type = BrandType.objects(name="Type1").first()
        assert brand_type is not None
        assert brand_type.name == "Type1"

    def test_brand_type_query_by_brand(self):
        """Test querying BrandType by brand"""
        brand = Brand(name="Huawei")
        brand.save()

        BrandType(name="Mate 60", brand=brand).save()
        BrandType(name="P60", brand=brand).save()

        brand_types = list(BrandType.objects(brand=brand))
        assert len(brand_types) == 2

    def test_brand_type_update_fields(self):
        """Test updating BrandType fields"""
        brand_type = BrandType(name="Xiaomi 14")
        brand_type.save()

        brand_type.desc = "High-end smartphone"
        brand_type.onsale_at = date(2024, 2, 1)
        brand_type.save()

        brand_type_reloaded = BrandType.objects(name="Xiaomi 14").first()
        assert brand_type_reloaded.desc == "High-end smartphone"
        assert brand_type_reloaded.onsale_at == date(2024, 2, 1)

    def test_brand_type_delete(self):
        """Test deleting BrandType"""
        brand_type = BrandType(name="Vivo X100")
        brand_type.save()
        brand_type_id = brand_type.id

        brand_type.delete()

        brand_type_deleted = BrandType.objects(id=brand_type_id).first()
        assert brand_type_deleted is None

    def test_brand_type_count(self):
        """Test counting BrandType objects"""
        BrandType(name="Type1").save()
        BrandType(name="Type2").save()
        BrandType(name="Type3").save()

        count = BrandType.objects.count()
        assert count == 3

    def test_brand_type_with_onsale_date(self):
        """Test BrandType with onsale_at date field"""
        release_date = date(2024, 3, 15)
        brand_type = BrandType(name="Oppo Find X7", onsale_at=release_date)
        brand_type.save()

        brand_type_reloaded = BrandType.objects(name="Oppo Find X7").first()
        assert brand_type_reloaded.onsale_at == release_date

    def test_brand_type_optional_fields(self):
        """Test BrandType with only required fields"""
        brand_type = BrandType(name="MinimalType")
        brand_type.save()

        assert brand_type.name == "MinimalType"
        assert brand_type.desc is None
        assert brand_type.onsale_at is None
        assert brand_type.brand is None
