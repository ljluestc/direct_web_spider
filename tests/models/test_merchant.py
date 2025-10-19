"""
Comprehensive unit tests for spider.models.merchant
"""
import pytest
from datetime import datetime
from mongoengine import connect, disconnect
from spider.models.merchant import Merchant


@pytest.mark.unit
@pytest.mark.model
@pytest.mark.unit
class TestMerchantModel:
    """Test cases for Merchant model"""

    @pytest.fixture(autouse=True)
    def setup_db(self):
        """Setup test database"""
        connect('testdb', host='localhost', mongo_client_class=__import__('mongomock').MongoClient, alias='default')
        Merchant.drop_collection()
        yield
        Merchant.drop_collection()
        disconnect(alias='default')

    def test_merchant_creation(self):
        """Test Merchant creation"""
        merchant = Merchant(name="Amazon")
        assert merchant is not None
        assert merchant.name == "Amazon"

    def test_merchant_save(self):
        """Test Merchant save"""
        merchant = Merchant(name="eBay")
        merchant.save()
        assert merchant.id is not None
        assert merchant.created_at is not None
        assert merchant.updated_at is not None

    def test_merchant_unique_name(self):
        """Test Merchant unique name constraint"""
        Merchant(name="Alibaba").save()
        merchant2 = Merchant(name="Alibaba")
        with pytest.raises(Exception):  # NotUniqueError
            merchant2.save()

    def test_merchant_with_all_fields(self):
        """Test Merchant with all fields populated"""
        merchant = Merchant(
            name="JD.com",
            desc="Large online retailer",
            service="Fast delivery",
            merchanturl="http://jd.com"
        )
        merchant.save()

        assert merchant.name == "JD.com"
        assert merchant.desc == "Large online retailer"
        assert merchant.service == "Fast delivery"
        assert merchant.merchanturl == "http://jd.com"

    def test_merchant_save_updates_timestamp(self):
        """Test Merchant save updates updated_at timestamp"""
        merchant = Merchant(name="Walmart")
        merchant.save()

        original_updated = merchant.updated_at
        import time
        time.sleep(0.01)

        merchant.desc = "Updated description"
        merchant.save()

        assert merchant.updated_at >= original_updated

    def test_merchant_timestamps_on_creation(self):
        """Test Merchant timestamps are set on creation"""
        before = datetime.utcnow()
        merchant = Merchant(name="Target")
        merchant.save()
        after = datetime.utcnow()

        assert before <= merchant.created_at <= after
        assert before <= merchant.updated_at <= after

    def test_merchant_query_by_name(self):
        """Test querying Merchant by name"""
        Merchant(name="BestBuy").save()
        Merchant(name="Newegg").save()

        merchant = Merchant.objects(name="BestBuy").first()
        assert merchant is not None
        assert merchant.name == "BestBuy"

    def test_merchant_update_fields(self):
        """Test updating Merchant fields"""
        merchant = Merchant(name="Costco")
        merchant.save()

        merchant.desc = "Wholesale retailer"
        merchant.merchanturl = "http://costco.com"
        merchant.save()

        merchant_reloaded = Merchant.objects(name="Costco").first()
        assert merchant_reloaded.desc == "Wholesale retailer"
        assert merchant_reloaded.merchanturl == "http://costco.com"

    def test_merchant_delete(self):
        """Test deleting Merchant"""
        merchant = Merchant(name="Sears")
        merchant.save()
        merchant_id = merchant.id

        merchant.delete()

        merchant_deleted = Merchant.objects(id=merchant_id).first()
        assert merchant_deleted is None

    def test_merchant_count(self):
        """Test counting Merchant objects"""
        Merchant(name="Merchant1").save()
        Merchant(name="Merchant2").save()
        Merchant(name="Merchant3").save()

        count = Merchant.objects.count()
        assert count == 3

    def test_merchant_optional_fields(self):
        """Test Merchant with only required fields"""
        merchant = Merchant(name="MinimalMerchant")
        merchant.save()

        assert merchant.name == "MinimalMerchant"
        assert merchant.desc is None
        assert merchant.service is None
        assert merchant.merchanturl is None
