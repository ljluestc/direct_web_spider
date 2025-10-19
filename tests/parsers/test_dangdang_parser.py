"""
Comprehensive unit tests for spider.parser.dangdang_parser
"""
import pytest
from unittest.mock import Mock
from datetime import datetime
from spider.parser.dangdang_parser import DangdangParser
from spider.parser import Parser


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestDangdangParserBase:
    """Test cases for DangdangParser base functionality"""

    def test_dangdang_parser_exists(self):
        """Test DangdangParser exists"""
        assert DangdangParser is not None

    def test_dangdang_parser_is_class(self):
        """Test DangdangParser is a class"""
        assert isinstance(DangdangParser, type)

    def test_dangdang_parser_inherits_parser(self):
        """Test DangdangParser inherits from Parser"""
        assert issubclass(DangdangParser, Parser)

    def test_dangdang_parser_initialization(self):
        """Test DangdangParser initialization"""
        product = Mock(html="<html><body>Test</body></html>", kind="dangdang", id="123")
        parser = DangdangParser(product)
        assert parser is not None
        assert parser.product == product
        assert parser.doc is not None

    def test_dangdang_parser_has_all_required_methods(self):
        """Test DangdangParser implements all required methods"""
        product = Mock(html="<html></html>", kind="dangdang", id="123")
        parser = DangdangParser(product)

        methods = [
            'title', 'price', 'price_url', 'stock', 'image_url',
            'desc', 'score', 'standard', 'product_code', 'comments',
            'end_product', 'merchant', 'brand', 'brand_type',
            'belongs_to_categories', 'attributes'
        ]
        for method_name in methods:
            assert hasattr(parser, method_name)
            assert callable(getattr(parser, method_name))


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestDangdangParserTitle:
    """Test cases for title() method"""

    def test_title_extraction_success(self):
        """Test title extraction with valid HTML"""
        html = """
        <html>
            <div class="dp_wrap">
                <h1>iPhone 15 Pro Max</h1>
            </div>
        </html>
        """
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        title = parser.title()
        assert title == "iPhone 15 Pro Max"

    def test_title_extraction_with_whitespace(self):
        """Test title extraction strips whitespace"""
        html = """
        <html>
            <div class="dp_wrap">
                <h1>  Samsung Galaxy S24  </h1>
            </div>
        </html>
        """
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        title = parser.title()
        assert title == "Samsung Galaxy S24"

    def test_title_extraction_missing_element(self):
        """Test title extraction with missing element"""
        html = "<html><body>No title here</body></html>"
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        title = parser.title()
        assert title is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestDangdangParserPrice:
    """Test cases for price() method"""

    def test_price_extraction_success(self):
        """Test price extraction with valid HTML"""
        html = """
        <html>
            <span id="salePriceTag">￥999</span>
        </html>
        """
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        price = parser.price()
        assert price == 999

    def test_price_extraction_with_decimal(self):
        """Test price extraction with decimal value"""
        html = """
        <html>
            <span id="salePriceTag">￥1299.99</span>
        </html>
        """
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        price = parser.price()
        assert price == 1299

    def test_price_extraction_without_currency_symbol(self):
        """Test price extraction without currency symbol"""
        html = """
        <html>
            <span id="salePriceTag">599</span>
        </html>
        """
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        price = parser.price()
        assert price == 599

    def test_price_extraction_missing_element(self):
        """Test price extraction with missing element"""
        html = "<html><body>No price here</body></html>"
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        price = parser.price()
        assert price is None

    def test_price_extraction_invalid_value(self):
        """Test price extraction with invalid value"""
        html = """
        <html>
            <span id="salePriceTag">￥Not a number</span>
        </html>
        """
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        price = parser.price()
        assert price is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestDangdangParserStock:
    """Test cases for stock() method"""

    def test_stock_returns_default_value(self):
        """Test stock returns default value of 1"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        stock = parser.stock()
        assert stock == 1


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestDangdangParserImageUrl:
    """Test cases for image_url() method"""

    def test_image_url_extraction_success(self):
        """Test image URL extraction with valid HTML"""
        html = """
        <html>
            <img id="largePic" src="http://img32.ddimg.cn/1/2/3_h.jpg" />
        </html>
        """
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        url = parser.image_url()
        assert url == "http://img32.ddimg.cn/1/2/3_h.jpg"

    def test_image_url_extraction_fallback(self):
        """Test image URL extraction with missing element returns fallback"""
        html = "<html><body>No image here</body></html>"
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        url = parser.image_url()
        assert url == "http://img32.ddimg.cn/7/35/60129142-1_h.jpg"


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestDangdangParserSimpleMethods:
    """Test cases for simple methods that return None"""

    def test_desc_returns_none(self):
        """Test desc() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        assert parser.desc() is None

    def test_price_url_returns_none(self):
        """Test price_url() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        assert parser.price_url() is None

    def test_product_code_returns_none(self):
        """Test product_code() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        assert parser.product_code() is None

    def test_standard_returns_none(self):
        """Test standard() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        assert parser.standard() is None

    def test_end_product_returns_none(self):
        """Test end_product() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        assert parser.end_product() is None

    def test_merchant_returns_none(self):
        """Test merchant() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        assert parser.merchant() is None

    def test_brand_returns_none(self):
        """Test brand() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        assert parser.brand() is None

    def test_brand_type_returns_none(self):
        """Test brand_type() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        assert parser.brand_type() is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestDangdangParserScore:
    """Test cases for score() method"""

    def test_score_extraction_five_stars(self):
        """Test score extraction with 5 red stars"""
        html = """
        <html>
            <p class="fraction">
                <img src="http://img.ddimg.cn/red_star.png" />
                <img src="http://img.ddimg.cn/red_star.png" />
                <img src="http://img.ddimg.cn/red_star.png" />
                <img src="http://img.ddimg.cn/red_star.png" />
                <img src="http://img.ddimg.cn/red_star.png" />
            </p>
        </html>
        """
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        score = parser.score()
        assert score == 5

    def test_score_extraction_mixed_stars(self):
        """Test score extraction with mixed red and gray stars"""
        html = """
        <html>
            <p class="fraction">
                <img src="http://img.ddimg.cn/red_star.png" />
                <img src="http://img.ddimg.cn/red_star.png" />
                <img src="http://img.ddimg.cn/red_star.png" />
                <img src="http://img.ddimg.cn/gray_star.png" />
                <img src="http://img.ddimg.cn/gray_star.png" />
            </p>
        </html>
        """
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        score = parser.score()
        assert score == 3

    def test_score_extraction_no_stars(self):
        """Test score extraction with no stars"""
        html = "<html><body>No stars here</body></html>"
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        score = parser.score()
        assert score == 0


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestDangdangParserComments:
    """Test cases for comments() method"""

    def test_comments_extraction_single_comment(self):
        """Test comments extraction with single comment"""
        html = """
        <html>
            <div id="comm_all">
                <h5><a>Great product!</a></h5>
                <div class="text">2023-10-15 12:00:00This is a great product.</div>
                <div class="title">
                    <span class="time">2023-10-15</span>
                    <span class="star">
                        <img src="http://img.ddimg.cn/red_star.png" />
                        <img src="http://img.ddimg.cn/red_star.png" />
                        <img src="http://img.ddimg.cn/red_star.png" />
                        <img src="http://img.ddimg.cn/red_star.png" />
                        <img src="http://img.ddimg.cn/red_star.png" />
                    </span>
                </div>
            </div>
        </html>
        """
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        comments = parser.comments()
        assert len(comments) == 1
        assert comments[0]["title"] == "Great product!"
        assert comments[0]["content"] == "This is a great product."
        assert comments[0]["star"] == 5
        assert isinstance(comments[0]["publish_at"], datetime)

    def test_comments_extraction_multiple_comments(self):
        """Test comments extraction with multiple comments"""
        html = """
        <html>
            <div id="comm_all">
                <h5><a>Comment 1</a></h5>
                <h5><a>Comment 2</a></h5>
                <div class="text">Content 1</div>
                <div class="text">Content 2</div>
                <div class="title"><span class="time">2023-10-15</span><span class="star"></span></div>
                <div class="title"><span class="time">2023-10-16</span><span class="star"></span></div>
            </div>
        </html>
        """
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        comments = parser.comments()
        assert len(comments) == 2
        assert comments[0]["title"] == "Comment 1"
        assert comments[1]["title"] == "Comment 2"

    def test_comments_extraction_with_datetime_format(self):
        """Test comments extraction with datetime format"""
        html = """
        <html>
            <div id="comm_all">
                <h5><a>Test</a></h5>
                <div class="text">Content</div>
                <div class="title">
                    <span class="time">2023-10-15 14:30:45</span>
                    <span class="star"></span>
                </div>
            </div>
        </html>
        """
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        comments = parser.comments()
        assert len(comments) == 1
        assert comments[0]["publish_at"].year == 2023
        assert comments[0]["publish_at"].month == 10
        assert comments[0]["publish_at"].day == 15

    def test_comments_extraction_invalid_date(self):
        """Test comments extraction with invalid date falls back to now()"""
        html = """
        <html>
            <div id="comm_all">
                <h5><a>Test</a></h5>
                <div class="text">Content</div>
                <div class="title">
                    <span class="time">invalid-date</span>
                    <span class="star"></span>
                </div>
            </div>
        </html>
        """
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        comments = parser.comments()
        assert len(comments) == 1
        # Should default to now()
        assert isinstance(comments[0]["publish_at"], datetime)

    def test_comments_extraction_no_comments(self):
        """Test comments extraction with no comments"""
        html = "<html><body>No comments here</body></html>"
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        comments = parser.comments()
        assert comments == []

    def test_comments_content_date_prefix_removal(self):
        """Test comments content removes date/time prefix"""
        html = """
        <html>
            <div id="comm_all">
                <h5><a>Test</a></h5>
                <div class="text">2023-10-15 12:30:45 This is the actual content</div>
                <div class="title"><span class="time">2023-10-15</span><span class="star"></span></div>
            </div>
        </html>
        """
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        comments = parser.comments()
        assert len(comments) == 1
        assert comments[0]["content"] == "This is the actual content"


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestDangdangParserCategories:
    """Test cases for belongs_to_categories() method"""

    def test_categories_extraction_single_category(self):
        """Test categories extraction with single category"""
        html = """
        <html>
            <div class="crumb">
                <a href="http://category.dangdang.com/list?cat=01.00.00.00.00.00">Electronics</a>
            </div>
        </html>
        """
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        categories = parser.belongs_to_categories()
        assert len(categories) == 1
        assert categories[0]["name"] == "Electronics"
        assert categories[0]["url"] == "http://category.dangdang.com/list?cat=01.00.00.00.00.00"

    def test_categories_extraction_multiple_categories(self):
        """Test categories extraction with multiple categories"""
        html = """
        <html>
            <div class="crumb">
                <a href="http://category.dangdang.com/list?cat=01">Electronics</a>
                <a href="http://category.dangdang.com/list?cat=01.01">Phones</a>
                <a href="http://category.dangdang.com/list?cat=01.01.01">Smartphones</a>
            </div>
        </html>
        """
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        categories = parser.belongs_to_categories()
        assert len(categories) == 3
        assert categories[0]["name"] == "Electronics"
        assert categories[1]["name"] == "Phones"
        assert categories[2]["name"] == "Smartphones"

    def test_categories_extraction_filters_non_list_links(self):
        """Test categories extraction filters out non-list links"""
        html = """
        <html>
            <div class="crumb">
                <a href="http://www.dangdang.com/">Home</a>
                <a href="http://category.dangdang.com/list?cat=01">Electronics</a>
                <a href="http://www.dangdang.com/about">About</a>
            </div>
        </html>
        """
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        categories = parser.belongs_to_categories()
        assert len(categories) == 1
        assert categories[0]["name"] == "Electronics"

    def test_categories_extraction_no_categories(self):
        """Test categories extraction with no categories"""
        html = "<html><body>No categories here</body></html>"
        product = Mock(html=html, kind="dangdang", id="123")
        parser = DangdangParser(product)

        categories = parser.belongs_to_categories()
        assert categories == []


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestDangdangParserAttributes:
    """Test cases for attributes() method"""

    def test_attributes_returns_complete_dict(self):
        """Test attributes() returns complete dictionary"""
        html = """
        <html>
            <div class="dp_wrap"><h1>Test Product</h1></div>
            <span id="salePriceTag">￥999</span>
            <img id="largePic" src="http://img.ddimg.cn/test.jpg" />
            <p class="fraction">
                <img src="http://img.ddimg.cn/red_star.png" />
                <img src="http://img.ddimg.cn/red_star.png" />
                <img src="http://img.ddimg.cn/red_star.png" />
            </p>
            <div class="crumb">
                <a href="http://category.dangdang.com/list?cat=01">Electronics</a>
            </div>
        </html>
        """
        product = Mock(html=html, kind="dangdang", id="prod123")
        parser = DangdangParser(product)

        attrs = parser.attributes()

        assert attrs["kind"] == "dangdang"
        assert attrs["title"] == "Test Product"
        assert attrs["price"] == 999
        assert attrs["stock"] == 1
        assert attrs["image_url"] == "http://img.ddimg.cn/test.jpg"
        assert attrs["score"] == 3
        assert attrs["product_url_id"] == "prod123"
        assert attrs["desc"] is None
        assert attrs["price_url"] is None
        assert attrs["product_code"] is None
        assert attrs["standard"] is None
        assert attrs["end_product"] is None
        assert attrs["merchant"] is None
        assert attrs["brand"] is None
        assert attrs["brand_type"] is None
        assert isinstance(attrs["comments"], list)

    def test_attributes_with_minimal_html(self):
        """Test attributes() with minimal HTML"""
        html = "<html><body>Minimal</body></html>"
        product = Mock(html=html, kind="dangdang", id="prod456")
        parser = DangdangParser(product)

        attrs = parser.attributes()

        assert attrs["kind"] == "dangdang"
        assert attrs["product_url_id"] == "prod456"
        assert attrs["title"] is None
        assert attrs["price"] is None
        assert attrs["comments"] == []
