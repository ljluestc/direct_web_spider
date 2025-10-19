"""
Comprehensive unit tests for spider.models.product
"""
import pytest
from datetime import datetime
from decimal import Decimal
from mongoengine import connect, disconnect
from spider.models.product import Product
from spider.models.product_url import ProductUrl
from spider.models.comment import Comment
from spider.models.merchant import Merchant
from spider.models.brand import Brand
from spider.models.brand_type import BrandType
from spider.models.end_product import EndProduct


@pytest.mark.unit
@pytest.mark.model
@pytest.mark.unit
class TestProductModel:
    """Test cases for Product model"""

    @pytest.fixture(autouse=True)
    def setup_db(self):
        """Setup test database"""
        connect('testdb', host='localhost', mongo_client_class=__import__('mongomock').MongoClient, alias='default')
        Product.drop_collection()
        ProductUrl.drop_collection()
        Merchant.drop_collection()
        Brand.drop_collection()
        BrandType.drop_collection()
        EndProduct.drop_collection()
        yield
        Product.drop_collection()
        ProductUrl.drop_collection()
        Merchant.drop_collection()
        Brand.drop_collection()
        BrandType.drop_collection()
        EndProduct.drop_collection()
        disconnect(alias='default')

    def test_product_creation(self):
        """Test Product creation"""
        product = Product(title="Test Product", kind="dangdang")
        assert product is not None
        assert product.title == "Test Product"
        assert product.kind == "dangdang"

    def test_product_save(self):
        """Test Product save"""
        product = Product(title="Test Product", kind="dangdang")
        product.save()
        assert product.id is not None
        assert product.created_at is not None
        assert product.updated_at is not None

    def test_product_with_price(self):
        """Test Product with price field"""
        product = Product(title="Test Product", price=Decimal("99.99"), kind="dangdang")
        product.save()

        assert product.price == Decimal("99.99")

        product_reloaded = Product.objects(id=product.id).first()
        assert product_reloaded.price == Decimal("99.99")

    def test_product_with_all_basic_fields(self):
        """Test Product with all basic fields"""
        product = Product(
            title="Test Product",
            price=Decimal("149.99"),
            price_url="http://price.com",
            stock=100,
            kind="dangdang",
            image_url="http://image.com/img.jpg",
            desc="Product description",
            score=5,
            standard="国标",
            product_code="ABC123"
        )
        product.save()

        assert product.title == "Test Product"
        assert product.price == Decimal("149.99")
        assert product.price_url == "http://price.com"
        assert product.stock == 100
        assert product.kind == "dangdang"
        assert product.image_url == "http://image.com/img.jpg"
        assert product.desc == "Product description"
        assert product.score == 5
        assert product.standard == "国标"
        assert product.product_code == "ABC123"

    def test_product_with_image_info_list(self):
        """Test Product with image_info list field"""
        product = Product(
            title="Test Product",
            kind="dangdang",
            image_info=["http://img1.com", "http://img2.com", "http://img3.com"]
        )
        product.save()

        assert len(product.image_info) == 3
        assert "http://img1.com" in product.image_info
        assert "http://img2.com" in product.image_info

    def test_product_with_merchant_relationship(self):
        """Test Product with Merchant relationship"""
        merchant = Merchant(name="Test Merchant")
        merchant.save()

        product = Product(title="Test Product", kind="dangdang", merchant=merchant)
        product.save()

        assert product.merchant is not None
        assert product.merchant.name == "Test Merchant"
        assert product.merchant.id == merchant.id

    def test_product_with_brand_relationship(self):
        """Test Product with Brand relationship"""
        brand = Brand(name="Test Brand")
        brand.save()

        product = Product(title="Test Product", kind="dangdang", brand=brand)
        product.save()

        assert product.brand is not None
        assert product.brand.name == "Test Brand"
        assert product.brand.id == brand.id

    def test_product_with_brand_type_relationship(self):
        """Test Product with BrandType relationship"""
        brand = Brand(name="Samsung")
        brand.save()

        brand_type = BrandType(name="Galaxy S23", brand=brand)
        brand_type.save()

        product = Product(title="Test Product", kind="dangdang", brand_type=brand_type)
        product.save()

        assert product.brand_type is not None
        assert product.brand_type.name == "Galaxy S23"
        assert product.brand_type.id == brand_type.id

    def test_product_with_end_product_relationship(self):
        """Test Product with EndProduct relationship"""
        end_product = EndProduct(name="Smartphone")
        end_product.save()

        product = Product(title="Test Product", kind="dangdang", end_product=end_product)
        product.save()

        assert product.end_product is not None
        assert product.end_product.name == "Smartphone"
        assert product.end_product.id == end_product.id

    def test_product_with_all_relationships(self):
        """Test Product with all relationships"""
        merchant = Merchant(name="Test Merchant")
        merchant.save()

        brand = Brand(name="Test Brand")
        brand.save()

        brand_type = BrandType(name="Type A", brand=brand)
        brand_type.save()

        end_product = EndProduct(name="Category X")
        end_product.save()

        product = Product(
            title="Test Product",
            kind="dangdang",
            merchant=merchant,
            brand=brand,
            brand_type=brand_type,
            end_product=end_product
        )
        product.save()

        assert product.merchant.name == "Test Merchant"
        assert product.brand.name == "Test Brand"
        assert product.brand_type.name == "Type A"
        assert product.end_product.name == "Category X"

    def test_product_with_embedded_comments(self):
        """Test Product with embedded comments"""
        comment1 = Comment(
            title="Great product",
            content="Very satisfied",
            author_name="John",
            star=5
        )
        comment2 = Comment(
            title="Good",
            content="Nice",
            author_name="Jane",
            star=4
        )

        product = Product(
            title="Test Product",
            kind="dangdang",
            comments=[comment1, comment2]
        )
        product.save()

        assert len(product.comments) == 2
        assert product.comments[0].title == "Great product"
        assert product.comments[0].author_name == "John"
        assert product.comments[0].star == 5
        assert product.comments[1].title == "Good"
        assert product.comments[1].star == 4

    def test_product_add_comment_after_save(self):
        """Test adding comments to Product after save"""
        product = Product(title="Test Product", kind="dangdang")
        product.save()

        comment = Comment(title="New comment", content="Test", author_name="Bob", star=5)
        product.comments.append(comment)
        product.save()

        product_reloaded = Product.objects(id=product.id).first()
        assert len(product_reloaded.comments) == 1
        assert product_reloaded.comments[0].author_name == "Bob"

    def test_product_url_property_with_product_url(self):
        """Test Product product_url property"""
        product_url = ProductUrl(url="http://test.com/p/123", kind="dangdang")
        product_url.save()

        product = Product(title="Test Product", kind="dangdang", product_url_id=product_url.id)
        product.save()

        assert product.product_url is not None
        assert product.product_url.id == product_url.id
        assert product.product_url.url == "http://test.com/p/123"

    def test_product_url_property_without_product_url(self):
        """Test Product product_url property when product_url_id is None"""
        product = Product(title="Test Product", kind="dangdang")
        product.save()

        assert product.product_url is None

    def test_product_url_property_invalid_id(self):
        """Test Product product_url property with non-existent product_url_id"""
        from bson import ObjectId
        product = Product(title="Test Product", kind="dangdang", product_url_id=ObjectId())
        product.save()

        assert product.product_url is None

    def test_product_from_kind_classmethod(self):
        """Test Product from_kind classmethod"""
        Product(title="Product 1", kind="dangdang").save()
        Product(title="Product 2", kind="dangdang").save()
        Product(title="Product 3", kind="jingdong").save()

        dd_products = list(Product.from_kind("dangdang"))
        assert len(dd_products) == 2

        jd_products = list(Product.from_kind("jingdong"))
        assert len(jd_products) == 1

    def test_product_from_kind_empty_result(self):
        """Test Product from_kind with no matching results"""
        Product(title="Product 1", kind="dangdang").save()

        results = list(Product.from_kind("nonexistent"))
        assert len(results) == 0

    def test_product_save_updates_timestamp(self):
        """Test Product save updates updated_at timestamp"""
        product = Product(title="Test Product", kind="dangdang")
        product.save()

        original_updated = product.updated_at
        import time
        time.sleep(0.01)

        product.title = "Updated Product"
        product.save()

        assert product.updated_at >= original_updated

    def test_product_timestamps_on_creation(self):
        """Test Product timestamps are set on creation"""
        before = datetime.utcnow()
        product = Product(title="Test Product", kind="dangdang")
        product.save()
        after = datetime.utcnow()

        assert before <= product.created_at <= after
        assert before <= product.updated_at <= after

    def test_product_stock_field(self):
        """Test Product stock field"""
        product = Product(title="Test Product", kind="dangdang", stock=50)
        product.save()

        assert product.stock == 50

        product.stock = 25
        product.save()

        product_reloaded = Product.objects(id=product.id).first()
        assert product_reloaded.stock == 25

    def test_product_score_field(self):
        """Test Product score field"""
        product = Product(title="Test Product", kind="dangdang", score=4)
        product.save()

        assert product.score == 4

    def test_product_complete_scenario(self):
        """Test Product with complete real-world scenario"""
        # Create all related objects
        merchant = Merchant(name="Amazon")
        merchant.save()

        brand = Brand(name="Sony")
        brand.save()

        brand_type = BrandType(name="PlayStation 5", brand=brand)
        brand_type.save()

        end_product = EndProduct(name="Gaming Console")
        end_product.save()

        product_url = ProductUrl(url="http://test.com/ps5", kind="dangdang")
        product_url.save()

        comment1 = Comment(title="Excellent!", content="Best console ever", author_name="Gamer1", star=5)
        comment2 = Comment(title="Good", content="Worth it", author_name="Gamer2", star=4)

        # Create product with everything
        product = Product(
            title="PlayStation 5 Console",
            price=Decimal("499.99"),
            price_url="http://test.com/price",
            stock=20,
            kind="dangdang",
            image_url="http://test.com/ps5.jpg",
            desc="Next-gen gaming console",
            image_info=["http://img1.com", "http://img2.com"],
            score=5,
            standard="Global",
            product_code="PS5-001",
            product_url_id=product_url.id,
            merchant=merchant,
            brand=brand,
            brand_type=brand_type,
            end_product=end_product,
            comments=[comment1, comment2]
        )
        product.save()

        # Verify everything
        product_reloaded = Product.objects(id=product.id).first()
        assert product_reloaded.title == "PlayStation 5 Console"
        assert product_reloaded.price == Decimal("499.99")
        assert product_reloaded.stock == 20
        assert product_reloaded.merchant.name == "Amazon"
        assert product_reloaded.brand.name == "Sony"
        assert product_reloaded.brand_type.name == "PlayStation 5"
        assert product_reloaded.end_product.name == "Gaming Console"
        assert product_reloaded.product_url.url == "http://test.com/ps5"
        assert len(product_reloaded.comments) == 2
        assert product_reloaded.comments[0].author_name == "Gamer1"
