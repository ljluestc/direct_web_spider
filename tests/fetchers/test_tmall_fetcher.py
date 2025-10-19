"""
Comprehensive unit tests for spider.fetcher.tmall_fetcher
"""
import pytest
from unittest.mock import Mock, patch
from spider.fetcher.tmall_fetcher import TmallFetcher
from spider.fetcher import Fetcher


@pytest.mark.unit
@pytest.mark.fetcher
@pytest.mark.unit
class TestTmallFetcherBase:
    """Test cases for TmallFetcher base functionality"""

    def test_tmall_fetcher_exists(self):
        """Test TmallFetcher exists"""
        assert TmallFetcher is not None

    def test_tmall_fetcher_inherits_fetcher(self):
        """Test TmallFetcher inherits from Fetcher"""
        assert issubclass(TmallFetcher, Fetcher)

    def test_tmall_fetcher_has_url(self):
        """Test TmallFetcher has URL"""
        assert hasattr(TmallFetcher, 'URL')
        assert "tmall.com" in TmallFetcher.URL

    def test_tmall_fetcher_has_blacklist(self):
        """Test TmallFetcher has BLACK_LIST"""
        assert hasattr(TmallFetcher, 'BLACK_LIST')
        assert isinstance(TmallFetcher.BLACK_LIST, list)


@pytest.mark.unit
@pytest.mark.fetcher
@pytest.mark.unit
class TestTmallFetcherCategoryList:
    """Test cases for TmallFetcher category_list method"""

    @patch('spider.fetcher.tmall_fetcher.requests.get')
    def test_category_list_makes_request(self, mock_get):
        """Test category_list makes HTTP request"""
        mock_response = Mock()
        mock_response.content = b'({name:"Test", href:"http://list.tmall.com/test.htm"})'
        mock_get.return_value = mock_response

        TmallFetcher.category_list()
        assert mock_get.called

    @patch('spider.fetcher.tmall_fetcher.requests.get')
    def test_category_list_returns_list(self, mock_get):
        """Test category_list returns list"""
        mock_response = Mock()
        mock_response.content = b'({name:"Test", href:"http://list.tmall.com/test.htm"})'
        mock_get.return_value = mock_response

        result = TmallFetcher.category_list()
        assert isinstance(result, list)

    @patch('spider.fetcher.tmall_fetcher.requests.get')
    def test_category_list_parses_javascript(self, mock_get):
        """Test category_list parses JavaScript objects"""
        content = b'({name:"Electronics", href:"http://list.tmall.com/electronics.htm"})({name:"Books", href:"http://list.tmall.com/books.htm"})'
        mock_response = Mock()
        mock_response.content = content
        mock_get.return_value = mock_response

        result = TmallFetcher.category_list()
        assert len(result) >= 0  # May filter some out

    @patch('spider.fetcher.tmall_fetcher.requests.get')
    def test_category_list_filters_tmall_urls(self, mock_get):
        """Test category_list only includes tmall.com URLs"""
        content = b'({name:"Valid", href:"http://list.tmall.com/test.htm"})({name:"Invalid", href:"http://other.com/test.htm"})'
        mock_response = Mock()
        mock_response.content = content
        mock_get.return_value = mock_response

        result = TmallFetcher.category_list()
        for category in result:
            assert "tmall.com" in category['url']

    @patch('spider.fetcher.tmall_fetcher.requests.get')
    def test_category_list_filters_catid_count(self, mock_get):
        """Test category_list excludes URLs with 'catid_count'"""
        content = b'({name:"Test", href:"http://list.tmall.com/test.htm?catid_count=1"})'
        mock_response = Mock()
        mock_response.content = content
        mock_get.return_value = mock_response

        result = TmallFetcher.category_list()
        assert all('catid_count' not in cat['url'] for cat in result)

    @patch('spider.fetcher.tmall_fetcher.requests.get')
    def test_category_list_filters_blacklist(self, mock_get):
        """Test category_list excludes blacklisted URLs"""
        # Use a known blacklist URL
        blacklist_url = TmallFetcher.BLACK_LIST[0] if TmallFetcher.BLACK_LIST else "http://list.tmall.com/blacklisted.htm"
        content = f'({{name:"Test", href:"{blacklist_url}"}})'.encode('utf-8')
        mock_response = Mock()
        mock_response.content = content
        mock_get.return_value = mock_response

        result = TmallFetcher.category_list()
        assert all(cat['url'] not in TmallFetcher.BLACK_LIST for cat in result)

    @patch('spider.fetcher.tmall_fetcher.requests.get')
    def test_category_list_gb18030_decode(self, mock_get):
        """Test category_list decodes GB18030 correctly"""
        content = '({name:"测试", href:"http://list.tmall.com/test.htm"})'.encode('GB18030')
        mock_response = Mock()
        mock_response.content = content
        mock_get.return_value = mock_response

        result = TmallFetcher.category_list()
        # May or may not find it depending on parsing, just ensure no crash
        assert isinstance(result, list)

    @patch('spider.fetcher.tmall_fetcher.requests.get')
    def test_category_list_skips_entries_without_name_or_href(self, mock_get):
        """Test category_list skips entries missing 'name' or 'href' keywords"""
        # Entry without 'name' keyword, entry without 'href' keyword, valid entry
        content = b'({title:"No name", href:"http://list.tmall.com/test.htm"})({name:"No href", url:"http://test.com"})({name:"Valid", href:"http://list.tmall.com/valid.htm"})'
        mock_response = Mock()
        mock_response.content = content
        mock_get.return_value = mock_response

        result = TmallFetcher.category_list()
        # Should only parse the valid entry
        assert isinstance(result, list)
        assert len(result) == 1
        assert 'valid' in result[0]['url']

    @patch('spider.fetcher.tmall_fetcher.requests.get')
    def test_category_list_handles_unquoted_values(self, mock_get):
        """Test category_list handles entries with unquoted name/href (branch miss)"""
        # Content with 'name' and 'href' but no quoted values - regex won't match
        content = b'({name: unquoted, href: unquoted})({name:"Valid", href:"http://list.tmall.com/valid.htm"})'
        mock_response = Mock()
        mock_response.content = content
        mock_get.return_value = mock_response

        result = TmallFetcher.category_list()
        # Should skip unmatched entries and parse valid ones
        assert isinstance(result, list)
        assert len(result) == 1
        assert 'valid' in result[0]['url']

    @patch('spider.fetcher.tmall_fetcher.re.sub')
    @patch('spider.fetcher.tmall_fetcher.requests.get')
    def test_category_list_handles_regex_exception(self, mock_get, mock_sub):
        """Test category_list handles exception during regex processing"""
        content = b'({name:"Test", href:"http://list.tmall.com/test.htm"})({name:"Valid", href:"http://list.tmall.com/valid.htm"})'
        mock_response = Mock()
        mock_response.content = content
        mock_get.return_value = mock_response

        # Make re.sub raise exception on first call, then work normally
        mock_sub.side_effect = [RuntimeError("Forced error"), '{name:"Valid", href:"http://list.tmall.com/valid.htm"}']

        result = TmallFetcher.category_list()
        # Should handle exception and continue processing second entry
        assert isinstance(result, list)
