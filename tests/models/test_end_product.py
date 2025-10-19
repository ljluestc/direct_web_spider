"""
Comprehensive unit tests for spider.models.end_product
"""
import pytest
from datetime import datetime
from mongoengine import connect, disconnect
from spider.models.end_product import EndProduct
from spider.models.middle_product import MiddleProduct
from spider.models.top_product import TopProduct


@pytest.mark.unit
@pytest.mark.model
@pytest.mark.unit
class TestEndProductModel:
    """Test cases for EndProduct model"""

    @pytest.fixture(autouse=True)
    def setup_db(self):
        """Setup test database"""
        connect('testdb', host='localhost', mongo_client_class=__import__('mongomock').MongoClient, alias='default')
        EndProduct.drop_collection()
        MiddleProduct.drop_collection()
        TopProduct.drop_collection()
        yield
        EndProduct.drop_collection()
        MiddleProduct.drop_collection()
        TopProduct.drop_collection()
        disconnect(alias='default')

    def test_end_product_creation(self):
        """Test EndProduct creation"""
        end_product = EndProduct(name="iPhone 15 Pro")
        assert end_product is not None
        assert end_product.name == "iPhone 15 Pro"

    def test_end_product_save(self):
        """Test EndProduct save"""
        end_product = EndProduct(name="Galaxy S24 Ultra")
        end_product.save()
        assert end_product.id is not None
        assert end_product.created_at is not None
        assert end_product.updated_at is not None

    def test_end_product_unique_name(self):
        """Test EndProduct unique name constraint"""
        EndProduct(name="MacBook Pro 16").save()
        end_product2 = EndProduct(name="MacBook Pro 16")
        with pytest.raises(Exception):  # NotUniqueError
            end_product2.save()

    def test_end_product_with_middle_product_relationship(self):
        """Test EndProduct with MiddleProduct relationship"""
        middle_product = MiddleProduct(name="Smartphones")
        middle_product.save()

        end_product = EndProduct(name="Pixel 8 Pro", middle_product=middle_product)
        end_product.save()

        assert end_product.middle_product is not None
        assert end_product.middle_product.name == "Smartphones"
        assert end_product.middle_product.id == middle_product.id

    def test_end_product_without_middle_product(self):
        """Test EndProduct without MiddleProduct relationship"""
        end_product = EndProduct(name="Generic Product")
        end_product.save()

        assert end_product.middle_product is None

    def test_end_product_save_updates_timestamp(self):
        """Test EndProduct save updates updated_at timestamp"""
        end_product = EndProduct(name="iPad Pro")
        end_product.save()

        original_updated = end_product.updated_at
        import time
        time.sleep(0.01)

        middle_product = MiddleProduct(name="Tablets")
        middle_product.save()
        end_product.middle_product = middle_product
        end_product.save()

        assert end_product.updated_at >= original_updated

    def test_end_product_timestamps_on_creation(self):
        """Test EndProduct timestamps are set on creation"""
        before = datetime.utcnow()
        end_product = EndProduct(name="AirPods Pro")
        end_product.save()
        after = datetime.utcnow()

        assert before <= end_product.created_at <= after
        assert before <= end_product.updated_at <= after

    def test_end_product_query_by_name(self):
        """Test querying EndProduct by name"""
        EndProduct(name="Product1").save()
        EndProduct(name="Product2").save()

        end_product = EndProduct.objects(name="Product1").first()
        assert end_product is not None
        assert end_product.name == "Product1"

    def test_end_product_query_by_middle_product(self):
        """Test querying EndProduct by middle_product"""
        middle_product = MiddleProduct(name="Laptops")
        middle_product.save()

        EndProduct(name="ThinkPad X1", middle_product=middle_product).save()
        EndProduct(name="Dell XPS 15", middle_product=middle_product).save()

        end_products = list(EndProduct.objects(middle_product=middle_product))
        assert len(end_products) == 2

    def test_end_product_update_middle_product(self):
        """Test updating EndProduct middle_product"""
        end_product = EndProduct(name="Surface Pro")
        end_product.save()

        middle_product = MiddleProduct(name="2-in-1 Devices")
        middle_product.save()

        end_product.middle_product = middle_product
        end_product.save()

        end_product_reloaded = EndProduct.objects(name="Surface Pro").first()
        assert end_product_reloaded.middle_product.name == "2-in-1 Devices"

    def test_end_product_delete(self):
        """Test deleting EndProduct"""
        end_product = EndProduct(name="OnePlus 12")
        end_product.save()
        end_product_id = end_product.id

        end_product.delete()

        end_product_deleted = EndProduct.objects(id=end_product_id).first()
        assert end_product_deleted is None

    def test_end_product_count(self):
        """Test counting EndProduct objects"""
        EndProduct(name="Product1").save()
        EndProduct(name="Product2").save()
        EndProduct(name="Product3").save()

        count = EndProduct.objects.count()
        assert count == 3

    def test_end_product_complete_hierarchy(self):
        """Test complete TopProduct -> MiddleProduct -> EndProduct hierarchy"""
        # Create top level
        top_product = TopProduct(name="Electronics")
        top_product.save()

        # Create middle level
        middle_product = MiddleProduct(name="Smartphones", top_product=top_product)
        middle_product.save()

        # Create end products
        end1 = EndProduct(name="iPhone 15", middle_product=middle_product)
        end1.save()

        end2 = EndProduct(name="Galaxy S24", middle_product=middle_product)
        end2.save()

        # Verify hierarchy
        assert end1.middle_product.name == "Smartphones"
        assert end1.middle_product.top_product.name == "Electronics"

        # Query all end products for this middle product
        end_products = list(EndProduct.objects(middle_product=middle_product))
        assert len(end_products) == 2
        names = [ep.name for ep in end_products]
        assert "iPhone 15" in names
        assert "Galaxy S24" in names

    def test_end_product_multiple_middle_products(self):
        """Test EndProducts across multiple MiddleProducts"""
        middle1 = MiddleProduct(name="Phones")
        middle1.save()

        middle2 = MiddleProduct(name="Computers")
        middle2.save()

        EndProduct(name="iPhone", middle_product=middle1).save()
        EndProduct(name="Android Phone", middle_product=middle1).save()
        EndProduct(name="MacBook", middle_product=middle2).save()

        phones = list(EndProduct.objects(middle_product=middle1))
        computers = list(EndProduct.objects(middle_product=middle2))

        assert len(phones) == 2
        assert len(computers) == 1
