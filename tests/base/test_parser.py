"""
Comprehensive unit tests for spider.parser
"""
import pytest
from unittest.mock import Mock
from spider.parser import Parser
from spider.logger import LoggerMixin


@pytest.mark.unit
class TestParserBase:
    """Test cases for Parser base class"""

    def test_parser_exists(self):
        """Test Parser exists"""
        assert Parser is not None

    def test_parser_is_class(self):
        """Test Parser is a class"""
        assert isinstance(Parser, type)

    def test_parser_inherits_logger_mixin(self):
        """Test Parser inherits LoggerMixin"""
        assert issubclass(Parser, LoggerMixin)

    def test_parser_init_with_product(self):
        """Test Parser __init__ with product"""
        mock_product = Mock()
        mock_product.html = "<html><body>Test</body></html>"
        parser = Parser(mock_product)
        assert parser.product == mock_product

    def test_parser_creates_beautifulsoup_doc(self):
        """Test Parser creates BeautifulSoup doc"""
        mock_product = Mock()
        mock_product.html = "<html><body>Content</body></html>"
        parser = Parser(mock_product)
        assert parser.doc is not None
        assert hasattr(parser.doc, 'find')

    def test_parser_has_attributes_method(self):
        """Test Parser has attributes method"""
        assert hasattr(Parser, 'attributes')
        assert callable(Parser.attributes)


@pytest.mark.unit
class TestParserAbstractMethods:
    """Test Parser abstract methods raise NotImplementedError"""

    def test_title_raises(self):
        mock = Mock(html="<html></html>")
        parser = Parser(mock)
        with pytest.raises(NotImplementedError):
            parser.title()

    def test_price_raises(self):
        mock = Mock(html="<html></html>")
        parser = Parser(mock)
        with pytest.raises(NotImplementedError):
            parser.price()

    def test_all_abstract_methods_raise(self):
        """Test all abstract methods raise NotImplementedError"""
        mock = Mock(html="<html></html>")
        parser = Parser(mock)
        methods = ['title', 'price', 'price_url', 'stock', 'image_url',
                   'desc', 'score', 'standard', 'product_code', 'comments',
                   'end_product', 'merchant', 'brand', 'brand_type',
                   'belongs_to_categories']
        for method in methods:
            with pytest.raises(NotImplementedError):
                getattr(parser, method)()
