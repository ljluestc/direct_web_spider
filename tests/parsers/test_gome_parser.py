"""
Comprehensive unit tests for spider.parser.gome_parser
"""
import pytest
from unittest.mock import Mock
from spider.parser.gome_parser import GomeParser
from spider.parser import Parser


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestGomeParserBase:
    """Test cases for GomeParser base functionality"""

    def test_gome_parser_exists(self):
        """Test GomeParser exists"""
        assert GomeParser is not None

    def test_gome_parser_is_class(self):
        """Test GomeParser is a class"""
        assert isinstance(GomeParser, type)

    def test_gome_parser_inherits_parser(self):
        """Test GomeParser inherits from Parser"""
        assert issubclass(GomeParser, Parser)

    def test_gome_parser_initialization(self):
        """Test GomeParser initialization"""
        product = Mock(html="<html><body>Test</body></html>", kind="gome", id="123")
        parser = GomeParser(product)
        assert parser is not None
        assert parser.product == product
        assert parser.doc is not None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestGomeParserTitle:
    """Test cases for title() method"""

    def test_title_extraction_success(self):
        """Test title extraction with valid HTML"""
        html = """
        <html>
            <div id="name">HP Pavilion Gaming Laptop</div>
        </html>
        """
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        title = parser.title()
        assert title == "HP Pavilion Gaming Laptop"

    def test_title_extraction_with_whitespace(self):
        """Test title extraction with extra whitespace"""
        html = """
        <html>
            <div id="name">  Acer Predator  </div>
        </html>
        """
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        title = parser.title()
        assert title == "Acer Predator"

    def test_title_extraction_missing_element(self):
        """Test title extraction with missing element"""
        html = "<html><body>No title here</body></html>"
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        title = parser.title()
        assert title is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestGomeParserPrice:
    """Test cases for price() method"""

    def test_price_returns_none(self):
        """Test price() returns None (AJAX loaded)"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        assert parser.price() is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestGomeParserStock:
    """Test cases for stock() method"""

    def test_stock_returns_one(self):
        """Test stock() returns 1 (default)"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        assert parser.stock() == 1


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestGomeParserImageUrl:
    """Test cases for image_url() method"""

    def test_image_url_extraction_success(self):
        """Test image URL extraction with valid HTML"""
        html = """
        <html>
            <div class="p_img_bar">
                <img src="http://img.gome.com/12345.jpg" />
            </div>
        </html>
        """
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        url = parser.image_url()
        assert url == "http://img.gome.com/12345.jpg"

    def test_image_url_extraction_missing_element(self):
        """Test image URL extraction with missing element"""
        html = "<html><body>No image here</body></html>"
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        url = parser.image_url()
        assert url is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestGomeParserDesc:
    """Test cases for desc() method"""

    def test_desc_extraction_success(self):
        """Test desc extraction with valid HTML"""
        html = """
        <html>
            <div class="description">
                <p>This is a great product</p>
                <p>With many features</p>
            </div>
        </html>
        """
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        desc = parser.desc()
        assert desc is not None
        assert "great product" in desc
        assert "many features" in desc

    def test_desc_extraction_missing_element(self):
        """Test desc extraction with missing element"""
        html = "<html><body>No description here</body></html>"
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        desc = parser.desc()
        assert desc is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestGomeParserPriceUrl:
    """Test cases for price_url() method"""

    def test_price_url_extraction_success(self):
        """Test price URL extraction with valid HTML"""
        html = """
        <html>
            <div id="gomeprice">
                <img src="http://price.gome.com/12345.gif" />
            </div>
        </html>
        """
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        url = parser.price_url()
        assert url == "http://price.gome.com/12345.gif"

    def test_price_url_extraction_missing_element(self):
        """Test price URL extraction with missing element"""
        html = "<html><body>No price URL here</body></html>"
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        url = parser.price_url()
        assert url is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestGomeParserScore:
    """Test cases for score() method"""

    def test_score_extraction_success(self):
        """Test score extraction with valid class"""
        html = """
        <html>
            <div id="positive">
                <div class="star star4">Rating</div>
            </div>
        </html>
        """
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        score = parser.score()
        assert score == 4

    def test_score_extraction_five_stars(self):
        """Test score extraction with 5 stars"""
        html = """
        <html>
            <div id="positive">
                <div class="star star5">Perfect</div>
            </div>
        </html>
        """
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        score = parser.score()
        assert score == 5

    def test_score_extraction_one_star(self):
        """Test score extraction with 1 star"""
        html = """
        <html>
            <div id="positive">
                <div class="star star1">Poor</div>
            </div>
        </html>
        """
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        score = parser.score()
        assert score == 1

    def test_score_extraction_missing_element(self):
        """Test score extraction with missing element"""
        html = "<html><body>No score here</body></html>"
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        score = parser.score()
        assert score == 0

    def test_score_class_as_string(self):
        """Test score when class attribute is a string (not list)"""
        from bs4 import BeautifulSoup
        html = """
        <html>
            <div id="positive">
                <div class="star star3">Rating</div>
            </div>
        </html>
        """
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        # Mock the element's get() method to return a string instead of list
        elem = parser.doc.select_one("#positive div.star")
        original_get = elem.get
        elem.get = lambda attr, default=None: "star star3" if attr == "class" else original_get(attr, default)

        score = parser.score()
        assert score == 3

    def test_score_no_digits_in_class(self):
        """Test score when class has no digits (branch 55->60)"""
        html = """
        <html>
            <div id="positive">
                <div class="star nodigits">Rating</div>
            </div>
        </html>
        """
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        score = parser.score()
        assert score == 0.0


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestGomeParserProductCode:
    """Test cases for product_code() method"""

    def test_product_code_extraction_success(self):
        """Test product code extraction with valid HTML"""
        html = """
        <html>
            <div id="sku">SKU: 12345678</div>
        </html>
        """
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        code = parser.product_code()
        assert code is not None
        assert "12345678" in code

    def test_product_code_extraction_missing_element(self):
        """Test product code extraction with missing element"""
        html = "<html><body>No product code here</body></html>"
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        code = parser.product_code()
        assert code is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestGomeParserStandard:
    """Test cases for standard() method"""

    def test_standard_extraction_success(self):
        """Test standard extraction with valid HTML"""
        html = """
        <html>
            <div class="Ptable">
                <table>
                    <tr><td>CPU</td><td>Intel i7</td></tr>
                    <tr><td>RAM</td><td>16GB</td></tr>
                </table>
            </div>
        </html>
        """
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        standard = parser.standard()
        assert standard is not None
        assert "Intel i7" in standard
        assert "16GB" in standard

    def test_standard_extraction_missing_element(self):
        """Test standard extraction with missing element"""
        html = "<html><body>No standard here</body></html>"
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        standard = parser.standard()
        assert standard is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestGomeParserBelongsToCategories:
    """Test cases for belongs_to_categories() method"""

    def test_belongs_to_categories_single(self):
        """Test category extraction with single category"""
        html = """
        <html>
            <div id="navigation">
                <a href="../category/electronics">Electronics</a>
            </div>
        </html>
        """
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        categories = parser.belongs_to_categories()
        assert len(categories) == 1
        assert categories[0]["name"] == "Electronics"
        assert categories[0]["url"] == "http://www.gome.com.cn/category/electronics"

    def test_belongs_to_categories_multiple(self):
        """Test category extraction with multiple categories"""
        html = """
        <html>
            <div id="navigation">
                <a href="../category/electronics">Electronics</a>
                <a href="../category/computers">Computers</a>
                <a href="../category/laptops">Laptops</a>
            </div>
        </html>
        """
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        categories = parser.belongs_to_categories()
        assert len(categories) == 3
        assert categories[0]["name"] == "Electronics"
        assert categories[1]["name"] == "Computers"
        assert categories[2]["name"] == "Laptops"

    def test_belongs_to_categories_filters_index_brand(self):
        """Test that URLs containing 'index' or 'brand' are filtered"""
        html = """
        <html>
            <div id="navigation">
                <a href="../index.html">Home</a>
                <a href="../category/electronics">Electronics</a>
                <a href="../brand/sony">Sony</a>
            </div>
        </html>
        """
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        categories = parser.belongs_to_categories()
        assert len(categories) == 1
        assert categories[0]["name"] == "Electronics"

    def test_belongs_to_categories_missing_element(self):
        """Test category extraction with missing element"""
        html = "<html><body>No categories here</body></html>"
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        categories = parser.belongs_to_categories()
        assert categories == []


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestGomeParserSimpleMethods:
    """Test cases for simple methods that return None or empty"""

    def test_comments_returns_empty_list(self):
        """Test comments() returns empty list"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        assert parser.comments() == []

    def test_end_product_returns_none(self):
        """Test end_product() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        assert parser.end_product() is None

    def test_merchant_returns_none(self):
        """Test merchant() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        assert parser.merchant() is None

    def test_brand_returns_none(self):
        """Test brand() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        assert parser.brand() is None

    def test_brand_type_returns_none(self):
        """Test brand_type() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="gome", id="123")
        parser = GomeParser(product)

        assert parser.brand_type() is None
