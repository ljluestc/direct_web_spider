"""
Comprehensive unit tests for spider.models.top_product
"""
import pytest
from datetime import datetime
from mongoengine import connect, disconnect
from spider.models.top_product import TopProduct


@pytest.mark.unit
@pytest.mark.model
@pytest.mark.unit
class TestTopProductModel:
    """Test cases for TopProduct model"""

    @pytest.fixture(autouse=True)
    def setup_db(self):
        """Setup test database"""
        connect('testdb', host='localhost', mongo_client_class=__import__('mongomock').MongoClient, alias='default')
        TopProduct.drop_collection()
        yield
        TopProduct.drop_collection()
        disconnect(alias='default')

    def test_top_product_creation(self):
        """Test TopProduct creation"""
        top_product = TopProduct(name="Electronics")
        assert top_product is not None
        assert top_product.name == "Electronics"

    def test_top_product_save(self):
        """Test TopProduct save"""
        top_product = TopProduct(name="Books")
        top_product.save()
        assert top_product.id is not None
        assert top_product.created_at is not None
        assert top_product.updated_at is not None

    def test_top_product_unique_name(self):
        """Test TopProduct unique name constraint"""
        TopProduct(name="Clothing").save()
        top_product2 = TopProduct(name="Clothing")
        with pytest.raises(Exception):  # NotUniqueError
            top_product2.save()

    def test_top_product_with_order_num(self):
        """Test TopProduct with order_num field"""
        top_product = TopProduct(name="Sports", order_num=5)
        top_product.save()

        assert top_product.order_num == 5

        top_product_reloaded = TopProduct.objects(name="Sports").first()
        assert top_product_reloaded.order_num == 5

    def test_top_product_default_order_num(self):
        """Test TopProduct default order_num"""
        top_product = TopProduct(name="Home")
        assert top_product.order_num == 0

        top_product.save()
        top_product_reloaded = TopProduct.objects(name="Home").first()
        assert top_product_reloaded.order_num == 0

    def test_top_product_save_updates_timestamp(self):
        """Test TopProduct save updates updated_at timestamp"""
        top_product = TopProduct(name="Toys")
        top_product.save()

        original_updated = top_product.updated_at
        import time
        time.sleep(0.01)

        top_product.order_num = 10
        top_product.save()

        assert top_product.updated_at >= original_updated

    def test_top_product_timestamps_on_creation(self):
        """Test TopProduct timestamps are set on creation"""
        before = datetime.utcnow()
        top_product = TopProduct(name="Garden")
        top_product.save()
        after = datetime.utcnow()

        assert before <= top_product.created_at <= after
        assert before <= top_product.updated_at <= after

    def test_top_product_query_by_name(self):
        """Test querying TopProduct by name"""
        TopProduct(name="Furniture").save()
        TopProduct(name="Appliances").save()

        top_product = TopProduct.objects(name="Furniture").first()
        assert top_product is not None
        assert top_product.name == "Furniture"

    def test_top_product_update_order_num(self):
        """Test updating TopProduct order_num"""
        top_product = TopProduct(name="Beauty", order_num=1)
        top_product.save()

        top_product.order_num = 5
        top_product.save()

        top_product_reloaded = TopProduct.objects(name="Beauty").first()
        assert top_product_reloaded.order_num == 5

    def test_top_product_delete(self):
        """Test deleting TopProduct"""
        top_product = TopProduct(name="Automotive")
        top_product.save()
        top_product_id = top_product.id

        top_product.delete()

        top_product_deleted = TopProduct.objects(id=top_product_id).first()
        assert top_product_deleted is None

    def test_top_product_count(self):
        """Test counting TopProduct objects"""
        TopProduct(name="Cat1").save()
        TopProduct(name="Cat2").save()
        TopProduct(name="Cat3").save()

        count = TopProduct.objects.count()
        assert count == 3

    def test_top_product_order_num_sorting(self):
        """Test sorting TopProduct by order_num"""
        TopProduct(name="Third", order_num=3).save()
        TopProduct(name="First", order_num=1).save()
        TopProduct(name="Second", order_num=2).save()

        top_products = list(TopProduct.objects.order_by('order_num'))
        assert top_products[0].name == "First"
        assert top_products[1].name == "Second"
        assert top_products[2].name == "Third"
