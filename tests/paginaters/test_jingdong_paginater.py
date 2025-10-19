"""
Comprehensive unit tests for spider.paginater.jingdong_paginater
"""
import pytest
from unittest.mock import Mock
from spider.paginater.jingdong_paginater import JingdongPaginater
from spider.paginater import Paginater


@pytest.mark.unit
@pytest.mark.paginater
@pytest.mark.unit
class TestJingdongPaginaterBase:
    """Test cases for JingdongPaginater base functionality"""

    def test_jingdong_paginater_exists(self):
        """Test JingdongPaginater exists"""
        assert JingdongPaginater is not None

    def test_jingdong_paginater_is_class(self):
        """Test JingdongPaginater is a class"""
        assert isinstance(JingdongPaginater, type)

    def test_jingdong_paginater_inherits_paginater(self):
        """Test JingdongPaginater inherits from Paginater"""
        assert issubclass(JingdongPaginater, Paginater)

    def test_jingdong_paginater_initialization(self):
        """Test JingdongPaginater initialization"""
        html = "<html><body>Test</body></html>"
        item = Mock(url="http://channel.jd.com/computers.html", html=html)
        paginater = JingdongPaginater(item)
        assert paginater is not None
        assert paginater.url == "http://channel.jd.com/computers.html"
        assert paginater.doc is not None


@pytest.mark.unit
@pytest.mark.paginater
@pytest.mark.unit
class TestJingdongPaginaterPaginationList:
    """Test cases for pagination_list() method"""

    def test_pagination_list_single_page(self):
        """Test pagination with single page"""
        html = """
        <html>
            <div class="pagin">
                <a>1</a>
            </div>
        </html>
        """
        item = Mock(url="http://channel.jd.com/computers.html", html=html)
        paginater = JingdongPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 1
        assert urls[0] == "http://channel.jd.com/computers-0-0-0-0-0-0-0-1-1-1.html"

    def test_pagination_list_multiple_pages(self):
        """Test pagination with multiple pages"""
        html = """
        <html>
            <div class="pagin">
                <a>1</a>
                <a>2</a>
                <a>3</a>
                <a>4</a>
                <a>5</a>
            </div>
        </html>
        """
        item = Mock(url="http://channel.jd.com/computers.html", html=html)
        paginater = JingdongPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 5
        assert urls[0] == "http://channel.jd.com/computers-0-0-0-0-0-0-0-1-1-1.html"
        assert urls[1] == "http://channel.jd.com/computers-0-0-0-0-0-0-0-1-1-2.html"
        assert urls[4] == "http://channel.jd.com/computers-0-0-0-0-0-0-0-1-1-5.html"

    def test_pagination_list_with_non_numeric_links(self):
        """Test pagination ignoring non-numeric links"""
        html = """
        <html>
            <div class="pagin">
                <a>上一页</a>
                <a>1</a>
                <a>2</a>
                <a>3</a>
                <a>下一页</a>
            </div>
        </html>
        """
        item = Mock(url="http://channel.jd.com/computers.html", html=html)
        paginater = JingdongPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 3
        assert all("-0-0-0-0-0-0-0-1-1-" in url for url in urls)

    def test_pagination_list_missing_div_pagin(self):
        """Test pagination when div.pagin is missing"""
        html = "<html><body>No pagination</body></html>"
        item = Mock(url="http://channel.jd.com/computers.html", html=html)
        paginater = JingdongPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 1
        assert urls[0] == "http://channel.jd.com/computers-0-0-0-0-0-0-0-1-1-1.html"

    def test_pagination_list_url_replacement(self):
        """Test that .html is correctly replaced"""
        html = """
        <html>
            <div class="pagin">
                <a>1</a>
                <a>2</a>
            </div>
        </html>
        """
        item = Mock(url="http://channel.jd.com/category.html", html=html)
        paginater = JingdongPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 2
        assert all(".html" in url for url in urls)
        assert all("-0-0-0-0-0-0-0-1-1-" in url for url in urls)
        assert urls[0].endswith("-1.html")
        assert urls[1].endswith("-2.html")

    def test_pagination_list_large_page_numbers(self):
        """Test pagination with large page numbers"""
        html = """
        <html>
            <div class="pagin">
                <a>98</a>
                <a>99</a>
                <a>100</a>
            </div>
        </html>
        """
        item = Mock(url="http://channel.jd.com/computers.html", html=html)
        paginater = JingdongPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 100
        assert urls[0].endswith("-1.html")
        assert urls[99].endswith("-100.html")
