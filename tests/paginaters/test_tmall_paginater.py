"""
Comprehensive unit tests for spider.paginater.tmall_paginater
"""
import pytest
from unittest.mock import Mock, patch
from spider.paginater.tmall_paginater import TmallPaginater
from spider.paginater import Paginater


@pytest.mark.unit
@pytest.mark.paginater
@pytest.mark.unit
class TestTmallPaginaterBase:
    """Test cases for TmallPaginater base functionality"""

    def test_tmall_paginater_exists(self):
        """Test TmallPaginater exists"""
        assert TmallPaginater is not None

    def test_tmall_paginater_inherits_paginater(self):
        """Test TmallPaginater inherits from Paginater"""
        assert issubclass(TmallPaginater, Paginater)


@pytest.mark.unit
@pytest.mark.paginater
@pytest.mark.unit
class TestTmallPaginaterPaginationList:
    """Test cases for TmallPaginater pagination_list method"""

    def test_pagination_list_single_page(self):
        """Test pagination with single page"""
        html = """
        <html>
            <input id="totalPage" value="1"/>
            <form id="filterPageForm" action="http://list.tmall.com/search_product.htm?cat=123&n=40"></form>
        </html>
        """
        item = Mock(url="http://list.tmall.com/search_product.htm?cat=123", html=html)
        paginater = TmallPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 1
        assert "s=0" in urls[0]

    def test_pagination_list_multiple_pages(self):
        """Test pagination with multiple pages"""
        html = """
        <html>
            <input id="totalPage" value="5"/>
            <form id="filterPageForm" action="http://list.tmall.com/search_product.htm?cat=123&n=40"></form>
        </html>
        """
        item = Mock(url="http://list.tmall.com/search_product.htm?cat=123", html=html)
        paginater = TmallPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 5

    def test_pagination_list_s_parameter_calculation(self):
        """Test that s parameter is calculated correctly: s = n * (page - 1)"""
        html = """
        <html>
            <input id="totalPage" value="3"/>
            <form id="filterPageForm" action="http://list.tmall.com/search_product.htm?cat=123&n=40"></form>
        </html>
        """
        item = Mock(url="http://list.tmall.com/search_product.htm?cat=123", html=html)
        paginater = TmallPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 3
        # Page 1: s = 40 * (1-1) = 0
        assert "s=0" in urls[0]
        # Page 2: s = 40 * (2-1) = 40
        assert "s=40" in urls[1]
        # Page 3: s = 40 * (3-1) = 80
        assert "s=80" in urls[2]

    def test_pagination_list_no_total_page(self):
        """Test pagination when totalPage element is missing"""
        html = """
        <html>
            <form id="filterPageForm" action="http://list.tmall.com/search_product.htm?cat=123&n=40"></form>
        </html>
        """
        item = Mock(url="http://list.tmall.com/search_product.htm?cat=123", html=html)
        paginater = TmallPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 1

    def test_pagination_list_no_form(self):
        """Test pagination when form element is missing"""
        html = """
        <html>
            <input id="totalPage" value="3"/>
        </html>
        """
        item = Mock(url="http://list.tmall.com/search_product.htm?cat=123", html=html)
        paginater = TmallPaginater(item)

        urls = paginater.pagination_list()
        assert isinstance(urls, list)

    def test_pagination_list_preserves_other_params(self):
        """Test that other query parameters are preserved"""
        html = """
        <html>
            <input id="totalPage" value="2"/>
            <form id="filterPageForm" action="http://list.tmall.com/search_product.htm?cat=123&n=40&sort=price"></form>
        </html>
        """
        item = Mock(url="http://list.tmall.com/search_product.htm?cat=123", html=html)
        paginater = TmallPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 2
        for url in urls:
            assert "cat=123" in url
            assert "sort=price" in url
            assert "n=40" in url

    def test_pagination_list_no_n_parameter(self):
        """Test pagination when n parameter is missing"""
        html = """
        <html>
            <input id="totalPage" value="2"/>
            <form id="filterPageForm" action="http://list.tmall.com/search_product.htm?cat=123"></form>
        </html>
        """
        item = Mock(url="http://list.tmall.com/search_product.htm?cat=123", html=html)
        paginater = TmallPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 2
        # When n=0, s should always be 0
        assert "s=0" in urls[0]
        assert "s=0" in urls[1]

    def test_pagination_list_returns_list(self):
        """Test pagination_list returns a list"""
        html = """
        <html>
            <input id="totalPage" value="1"/>
            <form id="filterPageForm" action="http://list.tmall.com/search_product.htm?cat=123&n=40"></form>
        </html>
        """
        item = Mock(url="http://list.tmall.com/search_product.htm?cat=123", html=html)
        paginater = TmallPaginater(item)

        result = paginater.pagination_list()
        assert isinstance(result, list)
