"""
Comprehensive unit tests for spider.paginater.gome_paginater
"""
import pytest
from unittest.mock import Mock, patch
from spider.paginater.gome_paginater import GomePaginater
from spider.paginater import Paginater


@pytest.mark.unit
@pytest.mark.paginater
@pytest.mark.unit
class TestGomePaginaterBase:
    """Test cases for GomePaginater base functionality"""

    def test_gome_paginater_exists(self):
        """Test GomePaginater exists"""
        assert GomePaginater is not None

    def test_gome_paginater_inherits_paginater(self):
        """Test GomePaginater inherits from Paginater"""
        assert issubclass(GomePaginater, Paginater)


@pytest.mark.unit
@pytest.mark.paginater
@pytest.mark.unit
class TestGomePaginaterParseUrlInfo:
    """Test cases for GomePaginater _parse_url_info method"""

    def test_parse_url_info_complete_url(self):
        """Test URL parsing with multiple numbers"""
        url = "http://www.gome.com.cn/category/cat12345678-cat87654321-v456.html"
        item = Mock(url=url, html="<html></html>")
        paginater = GomePaginater(item)

        info = paginater._parse_url_info()
        assert info['topCtgyId'] == '12345678'
        assert info['ctgyId'] == '87654321'
        assert info['ctgLevel'] == '456'
        assert info['order'] == 3

    def test_parse_url_info_minimal_url(self):
        """Test URL parsing with minimal numbers"""
        url = "http://www.gome.com.cn/category.html"
        item = Mock(url=url, html="<html></html>")
        paginater = GomePaginater(item)

        info = paginater._parse_url_info()
        assert info['topCtgyId'] == ''
        assert info['ctgyId'] == ''
        assert info['ctgLevel'] == ''

    def test_parse_url_info_returns_dict(self):
        """Test that _parse_url_info returns a dictionary"""
        url = "http://www.gome.com.cn/category/123-456.html"
        item = Mock(url=url, html="<html></html>")
        paginater = GomePaginater(item)

        info = paginater._parse_url_info()
        assert isinstance(info, dict)
        assert 'topCtgyId' in info
        assert 'ctgyId' in info
        assert 'ctgLevel' in info
        assert 'order' in info


@pytest.mark.unit
@pytest.mark.paginater
@pytest.mark.unit
class TestGomePaginaterPaginationList:
    """Test cases for GomePaginater pagination_list method"""

    def test_pagination_list_single_page(self):
        """Test pagination with single page"""
        html = """
        <html>
            <div class="thispage">1/1</div>
        </html>
        """
        url = "http://www.gome.com.cn/category/cat12345678-cat87654321-v456.html"
        item = Mock(url=url, html=html)
        paginater = GomePaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 1
        assert "p=1" in urls[0]

    def test_pagination_list_multiple_pages(self):
        """Test pagination with multiple pages"""
        html = """
        <html>
            <div class="thispage">1/5</div>
        </html>
        """
        url = "http://www.gome.com.cn/category/cat12345678-cat87654321-v456.html"
        item = Mock(url=url, html=html)
        paginater = GomePaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 5

    def test_pagination_list_page_parameter(self):
        """Test that page parameter increments correctly"""
        html = """
        <html>
            <div class="thispage">1/3</div>
        </html>
        """
        url = "http://www.gome.com.cn/category/cat12345678-cat87654321-v456.html"
        item = Mock(url=url, html=html)
        paginater = GomePaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 3
        assert "p=1" in urls[0]
        assert "p=2" in urls[1]
        assert "p=3" in urls[2]

    def test_pagination_list_no_thispage(self):
        """Test pagination when thispage element is missing"""
        html = """
        <html>
            <div>No pagination</div>
        </html>
        """
        url = "http://www.gome.com.cn/category/cat12345678-cat87654321-v456.html"
        item = Mock(url=url, html=html)
        paginater = GomePaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 1

    def test_pagination_list_url_structure(self):
        """Test that URLs have correct structure"""
        html = """
        <html>
            <div class="thispage">1/2</div>
        </html>
        """
        url = "http://www.gome.com.cn/category/cat12345678-cat87654321-v456.html"
        item = Mock(url=url, html=html)
        paginater = GomePaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 2
        for url in urls:
            assert url.startswith("http://search.gome.com.cn/product.do?")
            assert "topCtgyId=12345678" in url
            assert "ctgyId=87654321" in url
            assert "ctgLevel=456" in url
            assert "order=3" in url

    def test_pagination_list_returns_list(self):
        """Test pagination_list returns a list"""
        html = """
        <html>
            <div class="thispage">1/1</div>
        </html>
        """
        url = "http://www.gome.com.cn/category/cat123-cat456.html"
        item = Mock(url=url, html=html)
        paginater = GomePaginater(item)

        result = paginater.pagination_list()
        assert isinstance(result, list)
