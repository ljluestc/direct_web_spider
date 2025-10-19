"""
Comprehensive unit tests for spider.digger
"""
import pytest
from unittest.mock import Mock
from spider.digger import Digger
from spider.logger import LoggerMixin


@pytest.mark.unit
class TestDiggerBase:
    """Test cases for Digger base class"""

    def test_digger_exists(self):
        """Test Digger exists"""
        assert Digger is not None

    def test_digger_is_class(self):
        """Test Digger is a class"""
        assert isinstance(Digger, type)

    def test_digger_inherits_logger_mixin(self):
        """Test Digger inherits LoggerMixin"""
        assert issubclass(Digger, LoggerMixin)

    def test_digger_init_with_page(self):
        """Test Digger __init__ with page"""
        mock_page = Mock()
        mock_page.url = "http://test.com"
        mock_page.html = "<html><body>Products</body></html>"
        digger = Digger(mock_page)
        assert digger.url == "http://test.com"

    def test_digger_creates_beautifulsoup_doc(self):
        """Test Digger creates BeautifulSoup doc"""
        mock_page = Mock()
        mock_page.url = "http://test.com"
        mock_page.html = "<html><body>Content</body></html>"
        digger = Digger(mock_page)
        assert digger.doc is not None
        assert hasattr(digger.doc, 'find')

    def test_digger_has_product_list_method(self):
        """Test Digger has product_list method"""
        assert hasattr(Digger, 'product_list')
        assert callable(Digger.product_list)

    def test_digger_product_list_raises_not_implemented(self):
        """Test product_list raises NotImplementedError"""
        mock_page = Mock(url="http://test.com", html="<html></html>")
        digger = Digger(mock_page)
        with pytest.raises(NotImplementedError):
            digger.product_list()

    def test_subclass_can_override_product_list(self):
        """Test subclass can override product_list"""
        class TestDigger(Digger):
            def product_list(self):
                return ["http://product1.com", "http://product2.com"]

        mock_page = Mock(url="http://test.com", html="<html></html>")
        digger = TestDigger(mock_page)
        result = digger.product_list()
        assert len(result) == 2
        assert result[0] == "http://product1.com"
