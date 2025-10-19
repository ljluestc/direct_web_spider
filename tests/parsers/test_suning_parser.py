"""
Comprehensive unit tests for spider.parser.suning_parser
"""
import pytest
from unittest.mock import Mock
from spider.parser.suning_parser import SuningParser
from spider.parser import Parser


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestSuningParserBase:
    """Test cases for SuningParser base functionality"""

    def test_suning_parser_exists(self):
        """Test SuningParser exists"""
        assert SuningParser is not None

    def test_suning_parser_is_class(self):
        """Test SuningParser is a class"""
        assert isinstance(SuningParser, type)

    def test_suning_parser_inherits_parser(self):
        """Test SuningParser inherits from Parser"""
        assert issubclass(SuningParser, Parser)

    def test_suning_parser_initialization(self):
        """Test SuningParser initialization"""
        product = Mock(html="<html><body>Test</body></html>", kind="suning", id="123")
        parser = SuningParser(product)
        assert parser is not None
        assert parser.product == product
        assert parser.doc is not None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestSuningParserTitle:
    """Test cases for title() method"""

    def test_title_extraction_success(self):
        """Test title extraction with valid HTML"""
        html = """
        <html>
            <div class="product_title_name">Lenovo ThinkPad X1 Carbon</div>
        </html>
        """
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        title = parser.title()
        assert title == "Lenovo ThinkPad X1 Carbon"

    def test_title_extraction_with_whitespace(self):
        """Test title extraction with extra whitespace"""
        html = """
        <html>
            <div class="product_title_name">  Dell XPS 15  </div>
        </html>
        """
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        title = parser.title()
        assert title == "Dell XPS 15"

    def test_title_extraction_missing_element(self):
        """Test title extraction with missing element"""
        html = "<html><body>No title here</body></html>"
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        title = parser.title()
        assert title is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestSuningParserPrice:
    """Test cases for price() method"""

    def test_price_returns_none(self):
        """Test price() returns None (AJAX loaded)"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        assert parser.price() is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestSuningParserStock:
    """Test cases for stock() method"""

    def test_stock_extraction_in_stock(self):
        """Test stock extraction with '现货' keyword"""
        html = """
        <html>
            <div id="deleverStatus">现货</div>
        </html>
        """
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        stock = parser.stock()
        assert stock == 1

    def test_stock_extraction_no_xianhuo(self):
        """Test stock extraction without '现货' keyword"""
        html = """
        <html>
            <div id="deleverStatus">预售</div>
        </html>
        """
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        stock = parser.stock()
        assert stock == 0

    def test_stock_extraction_missing_element(self):
        """Test stock extraction with missing element"""
        html = "<html><body>No stock info</body></html>"
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        stock = parser.stock()
        assert stock == 0


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestSuningParserImageUrl:
    """Test cases for image_url() method"""

    def test_image_url_extraction_success(self):
        """Test image URL extraction with valid HTML"""
        html = """
        <html>
            <div class="product_b_image">
                <img src="http://image.suning.com/12345.jpg" />
            </div>
        </html>
        """
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        url = parser.image_url()
        assert url == "http://image.suning.com/12345.jpg"

    def test_image_url_extraction_missing_element(self):
        """Test image URL extraction with missing element"""
        html = "<html><body>No image here</body></html>"
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        url = parser.image_url()
        assert url is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestSuningParserScore:
    """Test cases for score() method"""

    def test_score_extraction_perfect_score(self):
        """Test score extraction with no noscore elements"""
        html = """
        <html>
            <div class="sn_stars">
                <em class="noscore"></em>
            </div>
        </html>
        """
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        score = parser.score()
        # 5 - 1 = 4
        assert score == 4

    def test_score_extraction_multiple_noscore(self):
        """Test score extraction with multiple noscore elements"""
        html = """
        <html>
            <div class="sn_stars">
                <em class="noscore"></em>
                <em class="noscore"></em>
                <em class="noscore"></em>
            </div>
        </html>
        """
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        score = parser.score()
        # 5 - 3 = 2
        assert score == 2

    def test_score_extraction_all_noscore(self):
        """Test score extraction with all 5 noscore elements"""
        html = """
        <html>
            <div class="sn_stars">
                <em class="noscore"></em>
                <em class="noscore"></em>
                <em class="noscore"></em>
                <em class="noscore"></em>
                <em class="noscore"></em>
            </div>
        </html>
        """
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        score = parser.score()
        # 5 - 5 = 0
        assert score == 0

    def test_score_extraction_no_noscore(self):
        """Test score extraction with no noscore elements"""
        html = """
        <html>
            <div class="sn_stars">
            </div>
        </html>
        """
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        score = parser.score()
        # 5 - 0 = 5
        assert score == 5

    def test_score_extraction_missing_element(self):
        """Test score extraction with missing sn_stars element"""
        html = "<html><body>No score here</body></html>"
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        score = parser.score()
        # No stars found, returns 5 - 0 = 5
        assert score == 5


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestSuningParserStandard:
    """Test cases for standard() method"""

    def test_standard_returns_empty_string(self):
        """Test standard() returns empty string"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        assert parser.standard() == ""


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestSuningParserProductCode:
    """Test cases for product_code() method"""

    def test_product_code_extraction_success(self):
        """Test product code extraction with valid HTML"""
        html = """
        <html>
            <div class="product_title_cout">产品编号：12345678</div>
        </html>
        """
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        code = parser.product_code()
        assert code == 12345678

    def test_product_code_extraction_whitespace(self):
        """Test product code extraction with whitespace"""
        html = """
        <html>
            <div class="product_title_cout">产品编号：  98765432  </div>
        </html>
        """
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        code = parser.product_code()
        assert code == 98765432

    def test_product_code_extraction_invalid_value(self):
        """Test product code extraction with invalid value"""
        html = """
        <html>
            <div class="product_title_cout">产品编号：not a number</div>
        </html>
        """
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        code = parser.product_code()
        assert code is None

    def test_product_code_extraction_missing_element(self):
        """Test product code extraction with missing element"""
        html = "<html><body>No product code here</body></html>"
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        code = parser.product_code()
        assert code is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestSuningParserSimpleMethods:
    """Test cases for simple methods that return None or empty"""

    def test_price_url_returns_none(self):
        """Test price_url() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        assert parser.price_url() is None

    def test_desc_returns_none(self):
        """Test desc() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        assert parser.desc() is None

    def test_comments_returns_empty_list(self):
        """Test comments() returns empty list"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        assert parser.comments() == []

    def test_end_product_returns_none(self):
        """Test end_product() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        assert parser.end_product() is None

    def test_merchant_returns_none(self):
        """Test merchant() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        assert parser.merchant() is None

    def test_brand_returns_none(self):
        """Test brand() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        assert parser.brand() is None

    def test_brand_type_returns_none(self):
        """Test brand_type() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        assert parser.brand_type() is None

    def test_belongs_to_categories_single(self):
        """Test category extraction with single category"""
        html = """
        <html>
            <div class="path">
                <a href="/category/electronics.html">Electronics</a>
            </div>
        </html>
        """
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        categories = parser.belongs_to_categories()
        assert len(categories) == 1
        assert categories[0]["name"] == "Electronics"
        assert categories[0]["url"] == "/category/electronics.html"

    def test_belongs_to_categories_multiple(self):
        """Test category extraction with multiple categories"""
        html = """
        <html>
            <div class="path">
                <a href="/category/electronics.html">Electronics</a>
                <a href="/category/computers.html">Computers</a>
            </div>
        </html>
        """
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        categories = parser.belongs_to_categories()
        assert len(categories) == 2
        assert categories[0]["name"] == "Electronics"
        assert categories[1]["name"] == "Computers"

    def test_belongs_to_categories_filters_non_html(self):
        """Test that URLs without 'html' are filtered"""
        html = """
        <html>
            <div class="path">
                <a href="/category/electronics.html">Electronics</a>
                <a href="/category/home">Home</a>
            </div>
        </html>
        """
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        categories = parser.belongs_to_categories()
        assert len(categories) == 1
        assert categories[0]["name"] == "Electronics"

    def test_belongs_to_categories_returns_empty_list(self):
        """Test belongs_to_categories() returns empty list"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="suning", id="123")
        parser = SuningParser(product)

        assert parser.belongs_to_categories() == []
