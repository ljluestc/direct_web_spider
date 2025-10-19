"""
Comprehensive unit tests for spider.paginater
"""
import pytest
from unittest.mock import Mock
from spider.paginater import Paginater
from spider.logger import LoggerMixin


@pytest.mark.unit
class TestPaginaterBase:
    """Test cases for Paginater base class"""

    def test_paginater_exists(self):
        """Test Paginater exists"""
        assert Paginater is not None

    def test_paginater_is_class(self):
        """Test Paginater is a class"""
        assert isinstance(Paginater, type)

    def test_paginater_inherits_logger_mixin(self):
        """Test Paginater inherits LoggerMixin"""
        assert issubclass(Paginater, LoggerMixin)

    def test_paginater_init_with_item(self):
        """Test Paginater __init__ with category item"""
        mock_item = Mock()
        mock_item.url = "http://test.com/category"
        mock_item.html = "<html><body>Pages</body></html>"
        paginater = Paginater(mock_item)
        assert paginater.url == "http://test.com/category"

    def test_paginater_creates_beautifulsoup_doc(self):
        """Test Paginater creates BeautifulSoup doc"""
        mock_item = Mock()
        mock_item.url = "http://test.com"
        mock_item.html = "<html><body>Content</body></html>"
        paginater = Paginater(mock_item)
        assert paginater.doc is not None
        assert hasattr(paginater.doc, 'find')

    def test_paginater_has_pagination_list_method(self):
        """Test Paginater has pagination_list method"""
        assert hasattr(Paginater, 'pagination_list')
        assert callable(Paginater.pagination_list)

    def test_paginater_pagination_list_raises_not_implemented(self):
        """Test pagination_list raises NotImplementedError"""
        mock_item = Mock(url="http://test.com", html="<html></html>")
        paginater = Paginater(mock_item)
        with pytest.raises(NotImplementedError):
            paginater.pagination_list()

    def test_subclass_can_override_pagination_list(self):
        """Test subclass can override pagination_list"""
        class TestPaginater(Paginater):
            def pagination_list(self):
                return ["http://test.com?page=1", "http://test.com?page=2"]

        mock_item = Mock(url="http://test.com", html="<html></html>")
        paginater = TestPaginater(mock_item)
        result = paginater.pagination_list()
        assert len(result) == 2
        assert "page=1" in result[0]
