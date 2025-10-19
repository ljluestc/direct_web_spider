"""
Comprehensive unit tests for spider.models.comment
"""
import pytest
from datetime import datetime
from mongoengine import connect, disconnect
from spider.models.comment import Comment
from spider.models.product import Product


@pytest.mark.unit
@pytest.mark.model
@pytest.mark.unit
class TestCommentModel:
    """Test cases for Comment embedded document"""

    @pytest.fixture(autouse=True)
    def setup_db(self):
        """Setup test database"""
        connect('testdb', host='localhost', mongo_client_class=__import__('mongomock').MongoClient, alias='default')
        Product.drop_collection()
        yield
        Product.drop_collection()
        disconnect(alias='default')

    def test_comment_creation(self):
        """Test Comment creation"""
        comment = Comment(title="Great product", content="Very satisfied")
        assert comment is not None
        assert comment.title == "Great product"
        assert comment.content == "Very satisfied"

    def test_comment_with_all_fields(self):
        """Test Comment with all fields"""
        publish_date = datetime(2024, 1, 15, 10, 30)
        comment = Comment(
            title="Excellent!",
            content="Best purchase ever",
            author_name="John Doe",
            star=5,
            publish_at=publish_date
        )

        assert comment.title == "Excellent!"
        assert comment.content == "Best purchase ever"
        assert comment.author_name == "John Doe"
        assert comment.star == 5
        assert comment.publish_at == publish_date

    def test_comment_embedded_in_product(self):
        """Test Comment embedded in Product"""
        comment1 = Comment(title="Good", content="Satisfied", author_name="Alice", star=4)
        comment2 = Comment(title="Excellent", content="Love it", author_name="Bob", star=5)

        product = Product(
            title="Test Product",
            kind="dangdang",
            comments=[comment1, comment2]
        )
        product.save()

        # Reload and verify
        product_reloaded = Product.objects(title="Test Product").first()
        assert len(product_reloaded.comments) == 2
        assert product_reloaded.comments[0].title == "Good"
        assert product_reloaded.comments[0].author_name == "Alice"
        assert product_reloaded.comments[1].title == "Excellent"
        assert product_reloaded.comments[1].star == 5

    def test_comment_star_rating(self):
        """Test Comment star rating field"""
        comment = Comment(title="Test", content="Test content", star=3)
        assert comment.star == 3

    def test_comment_with_datetime(self):
        """Test Comment with publish_at datetime"""
        publish_date = datetime(2024, 3, 20, 14, 30, 0)
        comment = Comment(
            title="Recent review",
            content="Just bought this",
            publish_at=publish_date
        )

        assert comment.publish_at == publish_date

    def test_comment_optional_fields(self):
        """Test Comment with only some fields"""
        comment = Comment(title="Minimal comment")
        assert comment.title == "Minimal comment"
        assert comment.content is None
        assert comment.author_name is None
        assert comment.star is None
        assert comment.publish_at is None

    def test_comment_in_product_multiple_comments(self):
        """Test Product with multiple comments"""
        comments = [
            Comment(title=f"Review {i}", content=f"Content {i}", author_name=f"User{i}", star=i)
            for i in range(1, 6)
        ]

        product = Product(title="Popular Product", kind="dangdang", comments=comments)
        product.save()

        product_reloaded = Product.objects(title="Popular Product").first()
        assert len(product_reloaded.comments) == 5
        assert product_reloaded.comments[0].star == 1
        assert product_reloaded.comments[4].star == 5

    def test_comment_update_in_product(self):
        """Test updating comments in Product"""
        comment = Comment(title="Initial", content="First comment")
        product = Product(title="Product", kind="dangdang", comments=[comment])
        product.save()

        # Add another comment
        product.comments.append(Comment(title="Second", content="Another comment"))
        product.save()

        product_reloaded = Product.objects(title="Product").first()
        assert len(product_reloaded.comments) == 2
        assert product_reloaded.comments[1].title == "Second"

    def test_comment_with_long_content(self):
        """Test Comment with long content"""
        long_content = "This is a very detailed review. " * 50
        comment = Comment(
            title="Detailed Review",
            content=long_content,
            author_name="Reviewer",
            star=4
        )

        product = Product(title="Product", kind="dangdang", comments=[comment])
        product.save()

        product_reloaded = Product.objects(title="Product").first()
        assert product_reloaded.comments[0].content == long_content

    def test_comment_empty_product_comments(self):
        """Test Product with no comments"""
        product = Product(title="No Comments Product", kind="dangdang")
        product.save()

        product_reloaded = Product.objects(title="No Comments Product").first()
        assert len(product_reloaded.comments) == 0
