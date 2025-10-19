"""
Comprehensive unit tests for spider.fetcher.jingdong_fetcher
"""
import pytest
from unittest.mock import Mock, patch
from spider.fetcher.jingdong_fetcher import JingdongFetcher
from spider.fetcher import Fetcher


@pytest.mark.unit
@pytest.mark.fetcher
@pytest.mark.unit
class TestJingdongFetcherBase:
    """Test cases for JingdongFetcher base functionality"""

    def test_jingdong_fetcher_exists(self):
        """Test JingdongFetcher exists"""
        assert JingdongFetcher is not None

    def test_jingdong_fetcher_inherits_fetcher(self):
        """Test JingdongFetcher inherits from Fetcher"""
        assert issubclass(JingdongFetcher, Fetcher)

    def test_jingdong_fetcher_has_url(self):
        """Test JingdongFetcher has URL"""
        assert hasattr(JingdongFetcher, 'URL')
        assert JingdongFetcher.URL == "http://www.360buy.com/allSort.aspx"

    def test_jingdong_fetcher_has_base_url(self):
        """Test JingdongFetcher has BASE_URL"""
        assert hasattr(JingdongFetcher, 'BASE_URL')
        assert JingdongFetcher.BASE_URL == "http://www.360buy.com"


@pytest.mark.unit
@pytest.mark.fetcher
@pytest.mark.unit
class TestJingdongFetcherCategoryList:
    """Test cases for JingdongFetcher category_list method"""

    @patch('spider.fetcher.jingdong_fetcher.requests.get')
    def test_category_list_makes_request(self, mock_get):
        """Test category_list makes HTTP request"""
        mock_response = Mock()
        mock_response.content = b'<html><div class="mc"><em><a href="products/671-672.html">Test</a></em></div></html>'
        mock_get.return_value = mock_response

        JingdongFetcher.category_list()
        mock_get.assert_called_once_with("http://www.360buy.com/allSort.aspx")

    @patch('spider.fetcher.jingdong_fetcher.requests.get')
    def test_category_list_returns_list(self, mock_get):
        """Test category_list returns list"""
        mock_response = Mock()
        mock_response.content = b'<html><div class="mc"><em><a href="products/test.html">Test</a></em></div></html>'
        mock_get.return_value = mock_response

        result = JingdongFetcher.category_list()
        assert isinstance(result, list)

    @patch('spider.fetcher.jingdong_fetcher.requests.get')
    def test_category_list_structure(self, mock_get):
        """Test category_list returns correct structure"""
        html = b'''<html>
            <div class="mc">
                <em><a href="products/electronics.html">Electronics</a></em>
                <em><a href="products/books.html">Books</a></em>
            </div>
        </html>'''
        mock_response = Mock()
        mock_response.content = html
        mock_get.return_value = mock_response

        result = JingdongFetcher.category_list()
        assert len(result) == 2
        for category in result:
            assert 'name' in category
            assert 'url' in category

    @patch('spider.fetcher.jingdong_fetcher.requests.get')
    def test_category_list_filters_href_prefix(self, mock_get):
        """Test category_list only includes hrefs starting with 'products'"""
        html = b'''<html>
            <div class="mc">
                <em><a href="products/test.html">Valid</a></em>
                <em><a href="other/test.html">Invalid</a></em>
            </div>
        </html>'''
        mock_response = Mock()
        mock_response.content = html
        mock_get.return_value = mock_response

        result = JingdongFetcher.category_list()
        assert len(result) == 1
        assert result[0]['name'] == 'Valid'

    @patch('spider.fetcher.jingdong_fetcher.requests.get')
    def test_category_list_url_join(self, mock_get):
        """Test category_list joins URLs with BASE_URL"""
        html = b'<html><div class="mc"><em><a href="products/test.html">Test</a></em></div></html>'
        mock_response = Mock()
        mock_response.content = html
        mock_get.return_value = mock_response

        result = JingdongFetcher.category_list()
        assert len(result) == 1
        assert result[0]['url'] == "http://www.360buy.com/products/test.html"

    @patch('spider.fetcher.jingdong_fetcher.requests.get')
    def test_category_list_gb18030_decode(self, mock_get):
        """Test category_list decodes GB18030 correctly"""
        html = '<html><div class="mc"><em><a href="products/test.html">测试</a></em></div></html>'.encode('GB18030')
        mock_response = Mock()
        mock_response.content = html
        mock_get.return_value = mock_response

        result = JingdongFetcher.category_list()
        assert len(result) == 1
        assert result[0]['name'] == '测试'
