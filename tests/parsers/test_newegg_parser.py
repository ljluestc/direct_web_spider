"""
Comprehensive unit tests for spider.parser.newegg_parser
"""
import pytest
from unittest.mock import Mock
from datetime import datetime
from spider.parser.newegg_parser import NeweggParser
from spider.parser import Parser


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestNeweggParserBase:
    """Test cases for NeweggParser base functionality"""

    def test_newegg_parser_exists(self):
        """Test NeweggParser exists"""
        assert NeweggParser is not None

    def test_newegg_parser_is_class(self):
        """Test NeweggParser is a class"""
        assert isinstance(NeweggParser, type)

    def test_newegg_parser_inherits_parser(self):
        """Test NeweggParser inherits from Parser"""
        assert issubclass(NeweggParser, Parser)

    def test_newegg_parser_initialization(self):
        """Test NeweggParser initialization"""
        product = Mock(html="<html><body>Test</body></html>", kind="newegg", id="123")
        parser = NeweggParser(product)
        assert parser is not None
        assert parser.product == product
        assert parser.doc is not None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestNeweggParserTitle:
    """Test cases for title() method"""

    def test_title_extraction_success(self):
        """Test title extraction with valid HTML"""
        html = """
        <html>
            <div class="proHeader">
                <h1>ASUS ROG Gaming Laptop</h1>
            </div>
        </html>
        """
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        title = parser.title()
        assert title == "ASUS ROG Gaming Laptop"

    def test_title_extraction_missing_element(self):
        """Test title extraction with missing element"""
        html = "<html><body>No title here</body></html>"
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        title = parser.title()
        assert title is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestNeweggParserPrice:
    """Test cases for price() method"""

    def test_price_returns_none(self):
        """Test price() returns None (AJAX loaded)"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        assert parser.price() is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestNeweggParserPriceUrl:
    """Test cases for price_url() method"""

    def test_price_url_extraction_success(self):
        """Test price URL extraction with valid HTML"""
        html = """
        <html>
            <div class="neweggPrice">
                <img src="http://promotions.newegg.com/price/12345.gif" />
            </div>
        </html>
        """
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        url = parser.price_url()
        assert url == "http://promotions.newegg.com/price/12345.gif"

    def test_price_url_extraction_missing_element(self):
        """Test price URL extraction with missing element"""
        html = "<html><body>No price image here</body></html>"
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        url = parser.price_url()
        assert url is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestNeweggParserStock:
    """Test cases for stock() method"""

    def test_stock_extraction_in_stock(self):
        """Test stock extraction with '有货' keyword"""
        html = """
        <html>
            <div class="detailList">
                <span class="lightly">有货</span>
            </div>
        </html>
        """
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        stock = parser.stock()
        assert stock == 1

    def test_stock_extraction_out_of_stock(self):
        """Test stock extraction with '无货' keyword"""
        html = """
        <html>
            <div class="detailList">
                <span class="lightly">无货</span>
            </div>
        </html>
        """
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        stock = parser.stock()
        assert stock == 0

    def test_stock_extraction_missing_element(self):
        """Test stock extraction with missing element"""
        html = "<html><body>No stock info</body></html>"
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        stock = parser.stock()
        assert stock == 0


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestNeweggParserImageUrl:
    """Test cases for image_url() method"""

    def test_image_url_extraction_success(self):
        """Test image URL extraction with valid HTML"""
        html = """
        <html>
            <a id="bigImg" href="http://images.newegg.com/12345_large.jpg">Image</a>
        </html>
        """
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        url = parser.image_url()
        assert url == "http://images.newegg.com/12345_large.jpg"

    def test_image_url_extraction_missing_element(self):
        """Test image URL extraction with missing element"""
        html = "<html><body>No image here</body></html>"
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        url = parser.image_url()
        assert url is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestNeweggParserScore:
    """Test cases for score() method"""

    def test_score_extraction_success(self):
        """Test score extraction with valid HTML"""
        html = """
        <html>
            <div class="score">
                <span>4.5</span>
            </div>
        </html>
        """
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        score = parser.score()
        assert score == 4.5

    def test_score_extraction_integer(self):
        """Test score extraction with integer value"""
        html = """
        <html>
            <div class="score">
                <span>5</span>
            </div>
        </html>
        """
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        score = parser.score()
        assert score == 5.0

    def test_score_extraction_invalid_value(self):
        """Test score extraction with invalid value"""
        html = """
        <html>
            <div class="score">
                <span>invalid</span>
            </div>
        </html>
        """
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        score = parser.score()
        assert score == 0.0

    def test_score_extraction_missing_element(self):
        """Test score extraction with missing element"""
        html = "<html><body>No score here</body></html>"
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        score = parser.score()
        assert score == 0.0


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestNeweggParserStandard:
    """Test cases for standard() method"""

    def test_standard_extraction_success(self):
        """Test standard extraction with valid HTML"""
        html = """
        <html>
            <div class="proDescTab">
                <table><tr><td>CPU: AMD Ryzen 7</td></tr></table>
            </div>
        </html>
        """
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        standard = parser.standard()
        assert standard is not None
        assert "CPU: AMD Ryzen 7" in standard

    def test_standard_extraction_missing_element(self):
        """Test standard extraction with missing element"""
        html = "<html><body>No standard here</body></html>"
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        standard = parser.standard()
        assert standard is None


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestNeweggParserComments:
    """Test cases for comments() method"""

    def test_comments_extraction_single_comment(self):
        """Test comments extraction with single comment"""
        html = """
        <html>
            <div id="comment_1">
                <div class="listCell">
                    <div class="title"><h2>Excellent Product</h2></div>
                    <div class="pubDate">2023-10-15</div>
                    <div class="rankIcon"><strong>5.0</strong></div>
                    <div class="content">
                        <div class="textBlock">This is a great laptop.</div>
                        <div class="textBlock">Highly recommended!</div>
                    </div>
                </div>
            </div>
        </html>
        """
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        comments = parser.comments()
        assert len(comments) == 1
        assert comments[0]["title"] == "Excellent Product"
        assert "great laptop" in comments[0]["content"]
        assert comments[0]["star"] == 5.0
        assert isinstance(comments[0]["publish_at"], datetime)

    def test_comments_extraction_multiple_comments(self):
        """Test comments extraction with multiple comments"""
        html = """
        <html>
            <div id="comment_1">
                <div class="listCell">
                    <div class="title"><h2>Comment 1</h2></div>
                    <div class="pubDate">2023-10-15</div>
                    <div class="rankIcon"><strong>4.0</strong></div>
                    <div class="content"><div class="textBlock">Content 1</div></div>
                </div>
                <div class="listCell">
                    <div class="title"><h2>Comment 2</h2></div>
                    <div class="pubDate">2023-10-16</div>
                    <div class="rankIcon"><strong>3.5</strong></div>
                    <div class="content"><div class="textBlock">Content 2</div></div>
                </div>
            </div>
        </html>
        """
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        comments = parser.comments()
        assert len(comments) == 2
        assert comments[0]["title"] == "Comment 1"
        assert comments[1]["title"] == "Comment 2"
        assert comments[0]["star"] == 4.0
        assert comments[1]["star"] == 3.5

    def test_comments_extraction_invalid_date(self):
        """Test comments extraction with invalid date"""
        html = """
        <html>
            <div id="comment_1">
                <div class="listCell">
                    <div class="title"><h2>Test</h2></div>
                    <div class="pubDate">invalid-date</div>
                    <div class="rankIcon"><strong>5.0</strong></div>
                    <div class="content"><div class="textBlock">Content</div></div>
                </div>
            </div>
        </html>
        """
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        comments = parser.comments()
        assert len(comments) == 1
        # Should default to now()
        assert isinstance(comments[0]["publish_at"], datetime)

    def test_comments_extraction_no_comments(self):
        """Test comments extraction with no comments"""
        html = "<html><body>No comments here</body></html>"
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        comments = parser.comments()
        assert comments == []


@pytest.mark.unit
@pytest.mark.parser
@pytest.mark.unit
class TestNeweggParserSimpleMethods:
    """Test cases for simple methods that return None or empty"""

    def test_desc_returns_none(self):
        """Test desc() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        assert parser.desc() is None

    def test_product_code_returns_none(self):
        """Test product_code() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        assert parser.product_code() is None

    def test_end_product_returns_none(self):
        """Test end_product() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        assert parser.end_product() is None

    def test_merchant_returns_none(self):
        """Test merchant() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        assert parser.merchant() is None

    def test_brand_returns_none(self):
        """Test brand() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        assert parser.brand() is None

    def test_brand_type_returns_none(self):
        """Test brand_type() returns None"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        assert parser.brand_type() is None

    def test_belongs_to_categories_returns_empty_list(self):
        """Test belongs_to_categories() returns empty list"""
        html = "<html><body>Test</body></html>"
        product = Mock(html=html, kind="newegg", id="123")
        parser = NeweggParser(product)

        assert parser.belongs_to_categories() == []
