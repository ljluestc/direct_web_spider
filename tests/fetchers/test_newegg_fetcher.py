"""
Comprehensive unit tests for spider.fetcher.newegg_fetcher
"""
import pytest
from unittest.mock import Mock, patch
from spider.fetcher.newegg_fetcher import NeweggFetcher
from spider.fetcher import Fetcher


@pytest.mark.unit
@pytest.mark.fetcher
@pytest.mark.unit
class TestNeweggFetcherBase:
    """Test cases for NeweggFetcher base functionality"""

    def test_newegg_fetcher_exists(self):
        """Test NeweggFetcher exists"""
        assert NeweggFetcher is not None

    def test_newegg_fetcher_inherits_fetcher(self):
        """Test NeweggFetcher inherits from Fetcher"""
        assert issubclass(NeweggFetcher, Fetcher)

    def test_newegg_fetcher_has_url(self):
        """Test NeweggFetcher has URL"""
        assert hasattr(NeweggFetcher, 'URL')
        assert NeweggFetcher.URL == "http://www.newegg.com.cn/CategoryList.htm"


@pytest.mark.unit
@pytest.mark.fetcher
@pytest.mark.unit
class TestNeweggFetcherCategoryList:
    """Test cases for NeweggFetcher category_list method"""

    @patch('spider.fetcher.newegg_fetcher.requests.get')
    def test_category_list_makes_request(self, mock_get):
        """Test category_list makes HTTP request"""
        mock_response = Mock()
        mock_response.content = b'<html><div class="allCateList"><dd><a href="/test.htm">Test</a></dd></div></html>'
        mock_get.return_value = mock_response

        NeweggFetcher.category_list()
        mock_get.assert_called_once_with("http://www.newegg.com.cn/CategoryList.htm")

    @patch('spider.fetcher.newegg_fetcher.requests.get')
    def test_category_list_returns_list(self, mock_get):
        """Test category_list returns list"""
        mock_response = Mock()
        mock_response.content = b'<html><div class="allCateList"><dd><a>Test</a></dd></div></html>'
        mock_get.return_value = mock_response

        result = NeweggFetcher.category_list()
        assert isinstance(result, list)

    @patch('spider.fetcher.newegg_fetcher.requests.get')
    def test_category_list_structure(self, mock_get):
        """Test category_list returns correct structure"""
        html = b'''<html>
            <div class="allCateList">
                <dd><a href="/electronics.htm">Electronics</a></dd>
                <dd><a href="/computers.htm">Computers</a></dd>
            </div>
        </html>'''
        mock_response = Mock()
        mock_response.content = html
        mock_get.return_value = mock_response

        result = NeweggFetcher.category_list()
        assert len(result) == 2
        for category in result:
            assert 'name' in category
            assert 'url' in category
            assert category['name'] in ['Electronics', 'Computers']

    @patch('spider.fetcher.newegg_fetcher.requests.get')
    def test_category_list_utf8_decode(self, mock_get):
        """Test category_list decodes UTF-8 correctly"""
        html = '<html><div class="allCateList"><dd><a href="/test.htm">测试</a></dd></div></html>'.encode('utf-8')
        mock_response = Mock()
        mock_response.content = html
        mock_get.return_value = mock_response

        result = NeweggFetcher.category_list()
        assert len(result) == 1
        assert result[0]['name'] == '测试'
