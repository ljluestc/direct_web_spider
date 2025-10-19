"""
Comprehensive unit tests for spider.fetcher.suning_fetcher
"""
import pytest
from unittest.mock import Mock, patch
from spider.fetcher.suning_fetcher import SuningFetcher
from spider.fetcher import Fetcher


@pytest.mark.unit
@pytest.mark.fetcher
@pytest.mark.unit
class TestSuningFetcherBase:
    """Test cases for SuningFetcher base functionality"""

    def test_suning_fetcher_exists(self):
        """Test SuningFetcher exists"""
        assert SuningFetcher is not None

    def test_suning_fetcher_inherits_fetcher(self):
        """Test SuningFetcher inherits from Fetcher"""
        assert issubclass(SuningFetcher, Fetcher)

    def test_suning_fetcher_has_url(self):
        """Test SuningFetcher has URL"""
        assert hasattr(SuningFetcher, 'URL')
        assert "suning.com" in SuningFetcher.URL

    def test_suning_fetcher_has_base_url(self):
        """Test SuningFetcher has BASE_URL"""
        assert hasattr(SuningFetcher, 'BASE_URL')
        assert SuningFetcher.BASE_URL == "http://www.suning.com"


@pytest.mark.unit
@pytest.mark.fetcher
@pytest.mark.unit
class TestSuningFetcherCategoryList:
    """Test cases for SuningFetcher category_list method"""

    @patch('spider.fetcher.suning_fetcher.requests.get')
    def test_category_list_makes_request(self, mock_get):
        """Test category_list makes HTTP request"""
        mock_response = Mock()
        mock_response.content = b'<html><div class="contentmain"><div class="allProContent"><div class="cont-left"><a href="/test">Test</a></div></div></div></html>'
        mock_get.return_value = mock_response

        SuningFetcher.category_list()
        assert mock_get.called

    @patch('spider.fetcher.suning_fetcher.requests.get')
    def test_category_list_returns_list(self, mock_get):
        """Test category_list returns list"""
        mock_response = Mock()
        mock_response.content = b'<html><div class="contentmain"><div class="allProContent"><div class="cont-left"><a>Test</a></div></div></div></html>'
        mock_get.return_value = mock_response

        result = SuningFetcher.category_list()
        assert isinstance(result, list)

    @patch('spider.fetcher.suning_fetcher.requests.get')
    def test_category_list_structure(self, mock_get):
        """Test category_list returns correct structure"""
        html = b'''<html>
            <div class="contentmain">
                <div class="allProContent">
                    <div class="cont-left">
                        <a href="/electronics">Electronics</a>
                        <a href="/books">Books</a>
                    </div>
                </div>
            </div>
        </html>'''
        mock_response = Mock()
        mock_response.content = html
        mock_get.return_value = mock_response

        result = SuningFetcher.category_list()
        assert len(result) == 2
        for category in result:
            assert 'name' in category
            assert 'url' in category

    @patch('spider.fetcher.suning_fetcher.requests.get')
    def test_category_list_url_join(self, mock_get):
        """Test category_list joins URLs with BASE_URL"""
        html = b'<html><div class="contentmain"><div class="allProContent"><div class="cont-left"><a href="/test.html">Test</a></div></div></div></html>'
        mock_response = Mock()
        mock_response.content = html
        mock_get.return_value = mock_response

        result = SuningFetcher.category_list()
        assert len(result) == 1
        assert result[0]['url'] == "http://www.suning.com/test.html"
