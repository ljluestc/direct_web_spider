"""
Comprehensive unit tests for spider.parser.jingdong_parser
"""
import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from spider.parser.jingdong_parser import JingdongParser
from spider.parser import Parser


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestJingdongParserBase:
    """Test cases for JingdongParser base functionality"""

    def test_jingdong_parser_exists(self):
        """Test JingdongParser exists"""
        assert JingdongParser is not None

    def test_jingdong_parser_is_class(self):
        """Test JingdongParser is a class"""
        assert isinstance(JingdongParser, type)

    def test_jingdong_parser_inherits_parser(self):
        """Test JingdongParser inherits from Parser"""
        assert issubclass(JingdongParser, Parser)

    def test_jingdong_parser_initialization(self):
        """Test JingdongParser initialization"""
        product = Mock(html="<html><body>Test</body></html>", kind="jingdong", id="123")
        parser = JingdongParser(product)
        assert parser is not None
        assert parser.product == product
        assert parser.doc is not None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestJingdongParserTitle:
    """Test cases for title() method"""

    def test_title_extraction_success(self):
        """Test title extraction with valid HTML"""
        html = """
        <html>
            <div id="name">
                <h1>Lenovo ThinkPad X1</h1>
            </div>
        </html>
        """
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        title = parser.title()
        assert title == "Lenovo ThinkPad X1"

    def test_title_extraction_missing_element(self):
        """Test title extraction with missing element"""
        html = "<html><body>No title here</body></html>"
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        title = parser.title()
        assert title is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestJingdongParserProductCode:
    """Test cases for product_code() method"""

    def test_product_code_extraction_success(self):
        """Test product code extraction with valid HTML"""
        html = """
        <html>
            <ul id="summary">
                <li><span>商品编号：JD123456</span></li>
            </ul>
        </html>
        """
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        code = parser.product_code()
        assert code == "JD123456"

    def test_product_code_extraction_removes_prefix(self):
        """Test product code extraction removes Chinese prefix"""
        html = """
        <html>
            <ul id="summary">
                <li><span>商品编号：XYZ789</span></li>
            </ul>
        </html>
        """
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        code = parser.product_code()
        assert code == "XYZ789"
        assert "商品编号" not in code

    def test_product_code_extraction_missing_element(self):
        """Test product code extraction with missing element"""
        html = "<html><body>No code here</body></html>"
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        code = parser.product_code()
        assert code is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestJingdongParserPrice:
    """Test cases for price() method"""

    def test_price_returns_none(self):
        """Test price() returns None (AJAX loaded)"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        assert parser.price() is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestJingdongParserPriceUrl:
    """Test cases for price_url() method"""

    def test_price_url_extraction_success(self):
        """Test price URL extraction with valid HTML"""
        html = """
        <html>
            <strong class="price">
                <img src="http://p1.jd.com/prices/101234.gif" />
            </strong>
        </html>
        """
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        url = parser.price_url()
        assert url == "http://p1.jd.com/prices/101234.gif"

    def test_price_url_extraction_missing_element(self):
        """Test price URL extraction with missing element"""
        html = "<html><body>No price image here</body></html>"
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        url = parser.price_url()
        assert url is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestJingdongParserStock:
    """Test cases for stock() method"""

    def test_stock_extraction_in_stock(self):
        """Test stock extraction with '发货' keyword"""
        html = """
        <html>
            <div id="stocktext">48小时发货</div>
        </html>
        """
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        stock = parser.stock()
        assert stock == 1

    def test_stock_extraction_out_of_stock(self):
        """Test stock extraction with '售完' keyword"""
        html = """
        <html>
            <div id="stocktext">已售完</div>
        </html>
        """
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        stock = parser.stock()
        assert stock == 0

    def test_stock_extraction_missing_element(self):
        """Test stock extraction with missing element logs and returns 0"""
        html = "<html><body>No stock info</body></html>"
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)
        mock_logger = Mock()
        parser._logger = mock_logger

        stock = parser.stock()
        assert stock == 0
        mock_logger.info.assert_called_once_with("stock issue!")


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestJingdongParserImageUrl:
    """Test cases for image_url() method"""

    def test_image_url_extraction_success(self):
        """Test image URL extraction with valid HTML"""
        html = """
        <html>
            <div id="preview">
                <img src="http://img.jd.com/12345_large.jpg" />
            </div>
        </html>
        """
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        url = parser.image_url()
        assert url == "http://img.jd.com/12345_large.jpg"

    def test_image_url_extraction_missing_element(self):
        """Test image URL extraction with missing element"""
        html = "<html><body>No image here</body></html>"
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        url = parser.image_url()
        assert url is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestJingdongParserScore:
    """Test cases for score() method"""

    def test_score_extraction_from_class(self):
        """Test score extraction from class attribute"""
        html = """
        <html>
            <div id="star-5">
                <div class="star50">5 stars</div>
            </div>
        </html>
        """
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        score = parser.score()
        assert score == 50

    def test_score_extraction_with_list_class(self):
        """Test score extraction with list class attribute"""
        html = """
        <html>
            <div id="star-rating">
                <div class="rating star40"></div>
            </div>
        </html>
        """
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        score = parser.score()
        assert score == 40

    def test_score_extraction_missing_element(self):
        """Test score extraction with missing element"""
        html = "<html><body>No score here</body></html>"
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        score = parser.score()
        assert score == 0


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestJingdongParserStandard:
    """Test cases for standard() method"""

    def test_standard_extraction_success(self):
        """Test standard extraction with valid HTML"""
        html = """
        <html>
            <div class="Ptable">
                <table><tr><td>Specifications</td></tr></table>
            </div>
        </html>
        """
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        standard = parser.standard()
        assert standard is not None
        assert "Specifications" in standard

    def test_standard_extraction_missing_element(self):
        """Test standard extraction with missing element"""
        html = "<html><body>No standard here</body></html>"
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        standard = parser.standard()
        assert standard is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestJingdongParserDesc:
    """Test cases for desc() method"""

    def test_desc_extraction_success(self):
        """Test desc extraction with valid HTML"""
        html = """
        <html>
            <div class="mc fore tabcon">
                <p>Product description here</p>
            </div>
        </html>
        """
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        desc = parser.desc()
        assert desc is not None
        assert "Product description" in desc

    def test_desc_extraction_missing_element(self):
        """Test desc extraction with missing element"""
        html = "<html><body>No desc here</body></html>"
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        desc = parser.desc()
        assert desc is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestJingdongParserComments:
    """Test cases for comments() method"""

    def test_comments_returns_empty_list(self):
        """Test comments() returns empty list (AJAX loaded)"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        comments = parser.comments()
        assert comments == []


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestJingdongParserCategories:
    """Test cases for belongs_to_categories() method"""

    def test_categories_extraction_with_products_url(self):
        """Test categories extraction with 'products' in URL"""
        html = """
        <html>
            <div class="crumb">
                <a href="http://www.jd.com/products/123.html">Electronics</a>
                <a href="http://www.jd.com/products/456.html">Laptops</a>
            </div>
        </html>
        """
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        categories = parser.belongs_to_categories()
        assert len(categories) == 2
        assert categories[0]["name"] == "Electronics"
        assert categories[1]["name"] == "Laptops"

    def test_categories_extraction_with_html_extension(self):
        """Test categories extraction with .com/xxx.html pattern"""
        html = """
        <html>
            <div class="crumb">
                <a href="http://www.jd.com/laptop.html">Laptops</a>
            </div>
        </html>
        """
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        categories = parser.belongs_to_categories()
        assert len(categories) == 1
        assert categories[0]["name"] == "Laptops"
        assert categories[0]["url"] == "http://www.jd.com/laptop.html"

    def test_categories_extraction_filters_non_matching_links(self):
        """Test categories extraction filters out non-matching links"""
        html = """
        <html>
            <div class="crumb">
                <a href="http://www.jd.com/">Home</a>
                <a href="http://www.jd.com/products/123.html">Electronics</a>
                <a href="http://www.jd.com/about">About</a>
            </div>
        </html>
        """
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        categories = parser.belongs_to_categories()
        assert len(categories) == 1
        assert categories[0]["name"] == "Electronics"


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestJingdongParserSimpleMethods:
    """Test cases for simple methods that return None"""

    def test_end_product_returns_none(self):
        """Test end_product() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        assert parser.end_product() is None

    def test_merchant_returns_none(self):
        """Test merchant() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        assert parser.merchant() is None

    def test_brand_returns_none(self):
        """Test brand() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        assert parser.brand() is None

    def test_brand_type_returns_none(self):
        """Test brand_type() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="jingdong", id="123")
        parser = JingdongParser(product)

        assert parser.brand_type() is None
