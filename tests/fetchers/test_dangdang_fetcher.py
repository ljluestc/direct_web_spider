"""
Comprehensive unit tests for spider.fetcher.dangdang_fetcher
"""
import pytest
from unittest.mock import Mock, patch
import json
from spider.fetcher.dangdang_fetcher import DangdangFetcher
from spider.fetcher import Fetcher


@pytest.mark.unit
@pytest.mark.dangdang
@pytest.mark.unit
class TestDangdangFetcherBase:
    """Test cases for DangdangFetcher base functionality"""

    def test_dangdang_fetcher_exists(self):
        """Test DangdangFetcher exists"""
        assert DangdangFetcher is not None

    def test_dangdang_fetcher_is_class(self):
        """Test DangdangFetcher is a class"""
        assert isinstance(DangdangFetcher, type)

    def test_dangdang_fetcher_inherits_fetcher(self):
        """Test DangdangFetcher inherits from Fetcher base"""
        assert issubclass(DangdangFetcher, Fetcher)

    def test_dangdang_fetcher_has_url(self):
        """Test DangdangFetcher has URL class variable"""
        assert hasattr(DangdangFetcher, 'URL')
        assert DangdangFetcher.URL == "http://www.dangdang.com/Found/category.js"

    def test_dangdang_fetcher_has_category_list(self):
        """Test DangdangFetcher has category_list classmethod"""
        assert hasattr(DangdangFetcher, 'category_list')
        assert callable(DangdangFetcher.category_list)


@pytest.mark.unit
@pytest.mark.dangdang
@pytest.mark.unit
class TestDangdangFetcherCategoryList:
    """Test cases for DangdangFetcher category_list method"""

    @patch('spider.fetcher.dangdang_fetcher.requests.get')
    def test_category_list_makes_request(self, mock_get):
        """Test category_list makes HTTP request to correct URL"""
        # Setup
        mock_response = Mock()
        mock_response.content = b'json_category={"test": {"n": "Test", "u": "#dd#book/list?cat=01.00.00.00.00.00"}}menudataloaded'
        mock_get.return_value = mock_response

        # Execute
        DangdangFetcher.category_list()

        # Verify
        mock_get.assert_called_once_with("http://www.dangdang.com/Found/category.js")

    @patch('spider.fetcher.dangdang_fetcher.requests.get')
    def test_category_list_returns_list(self, mock_get):
        """Test category_list returns list"""
        # Setup
        mock_response = Mock()
        mock_response.content = b'json_category={"1": {"n": "Books", "u": "#dd#book/list?cat=01.00.00.00.00.00"}}menudataloaded'
        mock_get.return_value = mock_response

        # Execute
        result = DangdangFetcher.category_list()

        # Verify
        assert isinstance(result, list)

    @patch('spider.fetcher.dangdang_fetcher.requests.get')
    def test_category_list_returns_correct_structure(self, mock_get):
        """Test category_list returns dicts with name and url"""
        # Setup
        json_data = {
            "1": {"n": "Books", "u": "#dd#book/list?cat=01.00.00.00.00.00"},
            "2": {"n": "Electronics", "u": "#dd#digital/list?cat=02.00.00.00.00.00"}
        }
        json_str = json.dumps(json_data)
        mock_response = Mock()
        mock_response.content = f'json_category={json_str}menudataloaded'.encode('utf-8')
        mock_get.return_value = mock_response

        # Execute
        result = DangdangFetcher.category_list()

        # Verify
        assert len(result) == 2
        for category in result:
            assert 'name' in category
            assert 'url' in category
            assert category['name'] in ['Books', 'Electronics']
            assert 'dangdang.com' in category['url']
            assert 'list?cat' in category['url']

    @patch('spider.fetcher.dangdang_fetcher.requests.get')
    def test_category_list_url_transformation(self, mock_get):
        """Test category_list transforms #dd# to .dangdang.com/"""
        # Setup
        mock_response = Mock()
        mock_response.content = b'json_category={"1": {"n": "Test", "u": "#dd#book/list?cat=01.00.00.00.00.00"}}menudataloaded'
        mock_get.return_value = mock_response

        # Execute
        result = DangdangFetcher.category_list()

        # Verify - #dd# is replaced with .dangdang.com/ in the URL
        assert len(result) == 1
        assert result[0]['url'] == "http://.dangdang.com/book/list?cat=01.00.00.00.00.00"

    @patch('spider.fetcher.dangdang_fetcher.requests.get')
    def test_category_list_filters_non_list_urls(self, mock_get):
        """Test category_list only includes URLs containing 'list?cat'"""
        # Setup
        json_data = {
            "1": {"n": "Books", "u": "#dd#book/list?cat=01.00.00.00.00.00"},
            "2": {"n": "Other", "u": "#dd#other/page"}  # Should be filtered out
        }
        json_str = json.dumps(json_data)
        mock_response = Mock()
        mock_response.content = f'json_category={json_str}menudataloaded'.encode('utf-8')
        mock_get.return_value = mock_response

        # Execute
        result = DangdangFetcher.category_list()

        # Verify - only Books should be included
        assert len(result) == 1
        assert result[0]['name'] == 'Books'

    @patch('spider.fetcher.dangdang_fetcher.requests.get')
    def test_category_list_handles_page_structure_change(self, mock_get):
        """Test category_list raises exception when page structure changes"""
        # Setup - invalid response without expected pattern
        mock_response = Mock()
        mock_response.content = b'invalid response without json_category'
        mock_get.return_value = mock_response

        # Execute and verify
        with pytest.raises(Exception) as exc_info:
            DangdangFetcher.category_list()

        assert "当当网页面结构改变了" in str(exc_info.value)

    @patch('spider.fetcher.dangdang_fetcher.requests.get')
    def test_category_list_empty_result(self, mock_get):
        """Test category_list with no valid categories"""
        # Setup - categories without 'list?cat' in URL
        json_data = {
            "1": {"n": "Invalid", "u": "#dd#other/page"}
        }
        json_str = json.dumps(json_data)
        mock_response = Mock()
        mock_response.content = f'json_category={json_str}menudataloaded'.encode('utf-8')
        mock_get.return_value = mock_response

        # Execute
        result = DangdangFetcher.category_list()

        # Verify
        assert isinstance(result, list)
        assert len(result) == 0

    @patch('spider.fetcher.dangdang_fetcher.requests.get')
    def test_category_list_utf8_decode(self, mock_get):
        """Test category_list decodes UTF-8 response correctly"""
        # Setup with Chinese characters
        json_data = {
            "1": {"n": "图书", "u": "#dd#book/list?cat=01.00.00.00.00.00"}
        }
        json_str = json.dumps(json_data, ensure_ascii=False)
        mock_response = Mock()
        mock_response.content = f'json_category={json_str}menudataloaded'.encode('utf-8')
        mock_get.return_value = mock_response

        # Execute
        result = DangdangFetcher.category_list()

        # Verify
        assert len(result) == 1
        assert result[0]['name'] == '图书'
