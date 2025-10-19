"""
Comprehensive unit tests for spider.models.middle_product
"""
import pytest
from datetime import datetime
from mongoengine import connect, disconnect
from spider.models.middle_product import MiddleProduct
from spider.models.top_product import TopProduct


@pytest.mark.unit
@pytest.mark.model
@pytest.mark.unit
class TestMiddleProductModel:
    """Test cases for MiddleProduct model"""

    @pytest.fixture(autouse=True)
    def setup_db(self):
        """Setup test database"""
        connect('testdb', host='localhost', mongo_client_class=__import__('mongomock').MongoClient, alias='default')
        MiddleProduct.drop_collection()
        TopProduct.drop_collection()
        yield
        MiddleProduct.drop_collection()
        TopProduct.drop_collection()
        disconnect(alias='default')

    def test_middle_product_creation(self):
        """Test MiddleProduct creation"""
        middle_product = MiddleProduct(name="Laptops")
        assert middle_product is not None
        assert middle_product.name == "Laptops"

    def test_middle_product_save(self):
        """Test MiddleProduct save"""
        middle_product = MiddleProduct(name="Smartphones")
        middle_product.save()
        assert middle_product.id is not None
        assert middle_product.created_at is not None
        assert middle_product.updated_at is not None

    def test_middle_product_unique_name(self):
        """Test MiddleProduct unique name constraint"""
        MiddleProduct(name="Tablets").save()
        middle_product2 = MiddleProduct(name="Tablets")
        with pytest.raises(Exception):  # NotUniqueError
            middle_product2.save()

    def test_middle_product_with_top_product_relationship(self):
        """Test MiddleProduct with TopProduct relationship"""
        top_product = TopProduct(name="Electronics")
        top_product.save()

        middle_product = MiddleProduct(name="Computers", top_product=top_product)
        middle_product.save()

        assert middle_product.top_product is not None
        assert middle_product.top_product.name == "Electronics"
        assert middle_product.top_product.id == top_product.id

    def test_middle_product_without_top_product(self):
        """Test MiddleProduct without TopProduct relationship"""
        middle_product = MiddleProduct(name="Generic Category")
        middle_product.save()

        assert middle_product.top_product is None

    def test_middle_product_save_updates_timestamp(self):
        """Test MiddleProduct save updates updated_at timestamp"""
        middle_product = MiddleProduct(name="Cameras")
        middle_product.save()

        original_updated = middle_product.updated_at
        import time
        time.sleep(0.01)

        top_product = TopProduct(name="Photography")
        top_product.save()
        middle_product.top_product = top_product
        middle_product.save()

        assert middle_product.updated_at >= original_updated

    def test_middle_product_timestamps_on_creation(self):
        """Test MiddleProduct timestamps are set on creation"""
        before = datetime.utcnow()
        middle_product = MiddleProduct(name="Headphones")
        middle_product.save()
        after = datetime.utcnow()

        assert before <= middle_product.created_at <= after
        assert before <= middle_product.updated_at <= after

    def test_middle_product_query_by_name(self):
        """Test querying MiddleProduct by name"""
        MiddleProduct(name="Monitors").save()
        MiddleProduct(name="Keyboards").save()

        middle_product = MiddleProduct.objects(name="Monitors").first()
        assert middle_product is not None
        assert middle_product.name == "Monitors"

    def test_middle_product_query_by_top_product(self):
        """Test querying MiddleProduct by top_product"""
        top_product = TopProduct(name="Computing")
        top_product.save()

        MiddleProduct(name="Desktops", top_product=top_product).save()
        MiddleProduct(name="Laptops", top_product=top_product).save()

        middle_products = list(MiddleProduct.objects(top_product=top_product))
        assert len(middle_products) == 2

    def test_middle_product_update_top_product(self):
        """Test updating MiddleProduct top_product"""
        middle_product = MiddleProduct(name="TVs")
        middle_product.save()

        top_product = TopProduct(name="Home Entertainment")
        top_product.save()

        middle_product.top_product = top_product
        middle_product.save()

        middle_product_reloaded = MiddleProduct.objects(name="TVs").first()
        assert middle_product_reloaded.top_product.name == "Home Entertainment"

    def test_middle_product_delete(self):
        """Test deleting MiddleProduct"""
        middle_product = MiddleProduct(name="Speakers")
        middle_product.save()
        middle_product_id = middle_product.id

        middle_product.delete()

        middle_product_deleted = MiddleProduct.objects(id=middle_product_id).first()
        assert middle_product_deleted is None

    def test_middle_product_count(self):
        """Test counting MiddleProduct objects"""
        MiddleProduct(name="Cat1").save()
        MiddleProduct(name="Cat2").save()
        MiddleProduct(name="Cat3").save()

        count = MiddleProduct.objects.count()
        assert count == 3

    def test_middle_product_hierarchy(self):
        """Test complete TopProduct -> MiddleProduct hierarchy"""
        top_product = TopProduct(name="Fashion")
        top_product.save()

        middle1 = MiddleProduct(name="Men's Clothing", top_product=top_product)
        middle1.save()

        middle2 = MiddleProduct(name="Women's Clothing", top_product=top_product)
        middle2.save()

        # Query all middle products for this top product
        middle_products = list(MiddleProduct.objects(top_product=top_product))
        assert len(middle_products) == 2
        names = [mp.name for mp in middle_products]
        assert "Men's Clothing" in names
        assert "Women's Clothing" in names
