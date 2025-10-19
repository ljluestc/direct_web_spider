"""
Comprehensive unit tests for spider.paginater.dangdang_paginater
"""
import pytest
from unittest.mock import Mock
from spider.paginater.dangdang_paginater import DangdangPaginater
from spider.paginater import Paginater


@pytest.mark.unit
@pytest.mark.paginater
@pytest.mark.unit
class TestDangdangPaginaterBase:
    """Test cases for DangdangPaginater base functionality"""

    def test_dangdang_paginater_exists(self):
        """Test DangdangPaginater exists"""
        assert DangdangPaginater is not None

    def test_dangdang_paginater_is_class(self):
        """Test DangdangPaginater is a class"""
        assert isinstance(DangdangPaginater, type)

    def test_dangdang_paginater_inherits_paginater(self):
        """Test DangdangPaginater inherits from Paginater"""
        assert issubclass(DangdangPaginater, Paginater)

    def test_dangdang_paginater_initialization(self):
        """Test DangdangPaginater initialization"""
        html = "<html><body>Test</body></html>"
        item = Mock(url="http://category.dangdang.com/test.html", html=html)
        paginater = DangdangPaginater(item)
        assert paginater is not None
        assert paginater.url == "http://category.dangdang.com/test.html"
        assert paginater.doc is not None


@pytest.mark.unit
@pytest.mark.paginater
@pytest.mark.unit
class TestDangdangPaginaterPaginationList:
    """Test cases for pagination_list() method"""

    def test_pagination_list_single_page(self):
        """Test pagination with single page"""
        html = """
        <html>
            <div id="all_num">1</div>
        </html>
        """
        item = Mock(url="http://category.dangdang.com/cp01.40.00.00.00.00.html", html=html)
        paginater = DangdangPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 1
        assert urls[0] == "http://category.dangdang.com/cp01.40.00.00.00.00.html&p=1"

    def test_pagination_list_multiple_pages(self):
        """Test pagination with multiple pages"""
        html = """
        <html>
            <div id="all_num">5</div>
        </html>
        """
        item = Mock(url="http://category.dangdang.com/cp01.40.00.00.00.00.html", html=html)
        paginater = DangdangPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 5
        assert urls[0] == "http://category.dangdang.com/cp01.40.00.00.00.00.html&p=1"
        assert urls[1] == "http://category.dangdang.com/cp01.40.00.00.00.00.html&p=2"
        assert urls[2] == "http://category.dangdang.com/cp01.40.00.00.00.00.html&p=3"
        assert urls[3] == "http://category.dangdang.com/cp01.40.00.00.00.00.html&p=4"
        assert urls[4] == "http://category.dangdang.com/cp01.40.00.00.00.00.html&p=5"

    def test_pagination_list_large_number_pages(self):
        """Test pagination with large number of pages"""
        html = """
        <html>
            <div id="all_num">100</div>
        </html>
        """
        item = Mock(url="http://category.dangdang.com/cp01.40.00.00.00.00.html", html=html)
        paginater = DangdangPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 100
        assert urls[0] == "http://category.dangdang.com/cp01.40.00.00.00.00.html&p=1"
        assert urls[99] == "http://category.dangdang.com/cp01.40.00.00.00.00.html&p=100"

    def test_pagination_list_with_text_around_number(self):
        """Test pagination when number is surrounded by text"""
        html = """
        <html>
            <div id="all_num">共 10 页</div>
        </html>
        """
        item = Mock(url="http://category.dangdang.com/cp01.40.00.00.00.00.html", html=html)
        paginater = DangdangPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 10
        assert urls[0] == "http://category.dangdang.com/cp01.40.00.00.00.00.html&p=1"
        assert urls[9] == "http://category.dangdang.com/cp01.40.00.00.00.00.html&p=10"

    def test_pagination_list_missing_element(self):
        """Test pagination when #all_num element is missing"""
        html = "<html><body>No pagination info</body></html>"
        item = Mock(url="http://category.dangdang.com/cp01.40.00.00.00.00.html", html=html)
        paginater = DangdangPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 1
        assert urls[0] == "http://category.dangdang.com/cp01.40.00.00.00.00.html&p=1"

    def test_pagination_list_no_number_in_text(self):
        """Test pagination when element has no number"""
        html = """
        <html>
            <div id="all_num">No pages</div>
        </html>
        """
        item = Mock(url="http://category.dangdang.com/cp01.40.00.00.00.00.html", html=html)
        paginater = DangdangPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 1
        assert urls[0] == "http://category.dangdang.com/cp01.40.00.00.00.00.html&p=1"

    def test_pagination_list_preserves_base_url(self):
        """Test that base URL is preserved in all generated URLs"""
        html = """
        <html>
            <div id="all_num">3</div>
        </html>
        """
        base_url = "http://category.dangdang.com/pg1-cp01.40.00.00.00.00.html?key=value"
        item = Mock(url=base_url, html=html)
        paginater = DangdangPaginater(item)

        urls = paginater.pagination_list()
        assert all(url.startswith(base_url + "&p=") for url in urls)
        assert all("key=value" in url for url in urls)

    def test_pagination_list_url_format(self):
        """Test that generated URLs follow correct format"""
        html = """
        <html>
            <div id="all_num">3</div>
        </html>
        """
        item = Mock(url="http://category.dangdang.com/test.html", html=html)
        paginater = DangdangPaginater(item)

        urls = paginater.pagination_list()
        for i, url in enumerate(urls, 1):
            assert url.endswith(f"&p={i}")
