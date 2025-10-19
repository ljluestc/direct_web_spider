"""
Comprehensive unit tests for spider.fetcher.gome_fetcher
"""
import pytest
from unittest.mock import Mock, patch
from spider.fetcher.gome_fetcher import GomeFetcher
from spider.fetcher import Fetcher


@pytest.mark.unit
@pytest.mark.fetcher
@pytest.mark.unit
class TestGomeFetcherBase:
    """Test cases for GomeFetcher base functionality"""

    def test_gome_fetcher_exists(self):
        """Test GomeFetcher exists"""
        assert GomeFetcher is not None

    def test_gome_fetcher_inherits_fetcher(self):
        """Test GomeFetcher inherits from Fetcher"""
        assert issubclass(GomeFetcher, Fetcher)

    def test_gome_fetcher_has_url(self):
        """Test GomeFetcher has URL"""
        assert hasattr(GomeFetcher, 'URL')
        assert GomeFetcher.URL == "http://www.gome.com.cn/allSort.html"


@pytest.mark.unit
@pytest.mark.fetcher
@pytest.mark.unit
class TestGomeFetcherCategoryList:
    """Test cases for GomeFetcher category_list method"""

    @patch('spider.fetcher.gome_fetcher.requests.get')
    def test_category_list_makes_request(self, mock_get):
        """Test category_list makes HTTP request"""
        mock_response = Mock()
        mock_response.content = b'<html><div id="allsort"><a href="product/test">Test</a></div></html>'
        mock_get.return_value = mock_response

        GomeFetcher.category_list()
        mock_get.assert_called_once_with("http://www.gome.com.cn/allSort.html")

    @patch('spider.fetcher.gome_fetcher.requests.get')
    def test_category_list_returns_list(self, mock_get):
        """Test category_list returns list"""
        mock_response = Mock()
        mock_response.content = b'<html><div id="allsort"><a href="product/test">Test</a></div></html>'
        mock_get.return_value = mock_response

        result = GomeFetcher.category_list()
        assert isinstance(result, list)

    @patch('spider.fetcher.gome_fetcher.requests.get')
    def test_category_list_filters_product_urls(self, mock_get):
        """Test category_list only includes URLs with 'product'"""
        html = b'''<html>
            <div id="allsort">
                <a href="product/electronics">Electronics</a>
                <a href="other/page">Other</a>
            </div>
        </html>'''
        mock_response = Mock()
        mock_response.content = html
        mock_get.return_value = mock_response

        result = GomeFetcher.category_list()
        assert len(result) == 1
        assert result[0]['name'] == 'Electronics'

    @patch('spider.fetcher.gome_fetcher.requests.get')
    def test_category_list_structure(self, mock_get):
        """Test category_list returns correct structure"""
        html = b'''<html>
            <div id="allsort">
                <a href="product/electronics">Electronics</a>
                <a href="product/books">Books</a>
            </div>
        </html>'''
        mock_response = Mock()
        mock_response.content = html
        mock_get.return_value = mock_response

        result = GomeFetcher.category_list()
        assert len(result) == 2
        for category in result:
            assert 'name' in category
            assert 'url' in category
            assert 'product' in category['url']
