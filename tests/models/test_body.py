"""
Comprehensive unit tests for spider.models.body
"""
import pytest
from datetime import datetime
from decimal import Decimal
from mongoengine import connect, disconnect
from spider.models.body import Body
from spider.models.product import Product
from spider.models.comment import Comment


@pytest.mark.unit
@pytest.mark.model
@pytest.mark.unit
class TestBodyModel:
    """Test cases for Body model"""

    @pytest.fixture(autouse=True)
    def setup_db(self):
        """Setup test database"""
        # Disconnect any existing connections first
        try:
            disconnect(alias='default')
        except:
            pass
        
        connect('testdb', host='localhost', mongo_client_class=__import__('mongomock').MongoClient, alias='default')
        Body.drop_collection()
        Product.drop_collection()
        yield
        Body.drop_collection()
        Product.drop_collection()
        try:
            disconnect(alias='default')
        except:
            pass

    def test_body_creation(self):
        """Test Body creation"""
        body = Body(title="Test Body", kind="dangdang")
        assert body is not None
        assert body.title == "Test Body"
        assert body.kind == "dangdang"

    def test_body_save(self):
        """Test Body save"""
        body = Body(title="Test Body", kind="dangdang")
        body.save()
        assert body.id is not None
        assert body.created_at is not None
        assert body.updated_at is not None

    def test_body_with_price(self):
        """Test Body with price field"""
        body = Body(title="Product Body", price=Decimal("199.99"), kind="jingdong")
        body.save()

        assert body.price == Decimal("199.99")

        body_reloaded = Body.objects(id=body.id).first()
        assert body_reloaded.price == Decimal("199.99")

    def test_body_with_all_basic_fields(self):
        """Test Body with all basic fields"""
        body = Body(
            title="Complete Body",
            price=Decimal("299.50"),
            price_url="http://price.com",
            stock=75,
            kind="tmall",
            image_url="http://img.com/body.jpg",
            text_info="Product details",
            score=4.5,
            standard="Premium",
            product_id=None
        )
        body.save()

        assert body.title == "Complete Body"
        assert body.price == Decimal("299.50")
        assert body.price_url == "http://price.com"
        assert body.stock == 75
        assert body.kind == "tmall"
        assert body.image_url == "http://img.com/body.jpg"
        assert body.text_info == "Product details"
        assert body.score == 4.5
        assert body.standard == "Premium"

    def test_body_with_image_info_list(self):
        """Test Body with image_info list field"""
        body = Body(
            title="Multi Image Body",
            kind="newegg",
            image_info=["http://img1.jpg", "http://img2.jpg", "http://img3.jpg"]
        )
        body.save()

        assert len(body.image_info) == 3
        assert "http://img1.jpg" in body.image_info

    def test_body_with_product_relationship(self):
        """Test Body with Product relationship"""
        product = Product(title="Reference Product", kind="dangdang")
        product.save()

        body = Body(title="Body with Product", kind="dangdang", product=product)
        body.save()

        assert body.product is not None
        assert body.product.title == "Reference Product"
        assert body.product.id == product.id

    def test_body_with_embedded_comments(self):
        """Test Body with embedded comments"""
        comment1 = Comment(title="Great!", content="Amazing product", author_name="User1", star=5)
        comment2 = Comment(title="Good", content="Satisfied", author_name="User2", star=4)

        body = Body(
            title="Body with Comments",
            kind="suning",
            comments=[comment1, comment2]
        )
        body.save()

        assert len(body.comments) == 2
        assert body.comments[0].title == "Great!"
        assert body.comments[0].star == 5
        assert body.comments[1].author_name == "User2"

    def test_body_from_kind_classmethod(self):
        """Test Body from_kind classmethod"""
        Body(title="Body 1", kind="dangdang").save()
        Body(title="Body 2", kind="dangdang").save()
        Body(title="Body 3", kind="jingdong").save()

        dd_bodies = list(Body.from_kind("dangdang"))
        assert len(dd_bodies) == 2

        jd_bodies = list(Body.from_kind("jingdong"))
        assert len(jd_bodies) == 1

    def test_body_from_kind_empty_result(self):
        """Test Body from_kind with no matching results"""
        Body(title="Body", kind="dangdang").save()

        results = list(Body.from_kind("nonexistent"))
        assert len(results) == 0

    def test_body_save_updates_timestamp(self):
        """Test Body save updates updated_at timestamp"""
        body = Body(title="Update Test", kind="gome")
        body.save()

        original_updated = body.updated_at
        import time
        time.sleep(0.01)

        body.title = "Updated Title"
        body.save()

        assert body.updated_at >= original_updated

    def test_body_timestamps_on_creation(self):
        """Test Body timestamps are set on creation"""
        before = datetime.utcnow()
        body = Body(title="Timestamp Test", kind="dangdang")
        body.save()
        after = datetime.utcnow()

        assert before <= body.created_at <= after
        assert before <= body.updated_at <= after

    def test_body_stock_field(self):
        """Test Body stock field"""
        body = Body(title="Stock Test", kind="dangdang", stock=100)
        body.save()

        body.stock = 50
        body.save()

        body_reloaded = Body.objects(id=body.id).first()
        assert body_reloaded.stock == 50

    def test_body_score_field(self):
        """Test Body score field (float)"""
        body = Body(title="Score Test", kind="dangdang", score=4.7)
        body.save()

        body_reloaded = Body.objects(id=body.id).first()
        assert body_reloaded.score == 4.7

    def test_body_with_product_id(self):
        """Test Body with product_id ObjectId field"""
        product = Product(title="Test Product", kind="dangdang")
        product.save()

        body = Body(title="Body", kind="dangdang", product_id=product.id)
        body.save()

        body_reloaded = Body.objects(id=body.id).first()
        assert body_reloaded.product_id == product.id

    def test_body_add_comments_after_save(self):
        """Test adding comments to Body after save"""
        body = Body(title="Comment Test", kind="dangdang")
        body.save()

        comment = Comment(title="New", content="New comment", author_name="Test", star=5)
        body.comments.append(comment)
        body.save()

        body_reloaded = Body.objects(id=body.id).first()
        assert len(body_reloaded.comments) == 1
        assert body_reloaded.comments[0].title == "New"

    def test_body_complete_scenario(self):
        """Test Body with complete real-world scenario"""
        product = Product(title="Main Product", kind="dangdang")
        product.save()

        comment1 = Comment(title="Excellent", content="Best ever", author_name="Buyer1", star=5)
        comment2 = Comment(title="Good", content="Nice", author_name="Buyer2", star=4)

        body = Body(
            title="Complete Product Details",
            price=Decimal("599.99"),
            price_url="http://test.com/price",
            stock=30,
            kind="dangdang",
            image_url="http://test.com/img.jpg",
            text_info="Detailed product information",
            image_info=["http://img1.jpg", "http://img2.jpg"],
            score=4.8,
            standard="High Quality",
            product_id=product.id,
            product=product,
            comments=[comment1, comment2]
        )
        body.save()

        # Verify everything
        body_reloaded = Body.objects(id=body.id).first()
        assert body_reloaded.title == "Complete Product Details"
        assert body_reloaded.price == Decimal("599.99")
        assert body_reloaded.stock == 30
        assert body_reloaded.score == 4.8
        assert body_reloaded.product.title == "Main Product"
        assert len(body_reloaded.comments) == 2
        assert body_reloaded.comments[0].star == 5

    def test_body_multiple_kinds(self):
        """Test Bodies with different kinds"""
        Body(title="DD Body", kind="dangdang").save()
        Body(title="JD Body", kind="jingdong").save()
        Body(title="TM Body", kind="tmall").save()

        dd_bodies = list(Body.from_kind("dangdang"))
        jd_bodies = list(Body.from_kind("jingdong"))
        tm_bodies = list(Body.from_kind("tmall"))

        assert len(dd_bodies) == 1
        assert len(jd_bodies) == 1
        assert len(tm_bodies) == 1
