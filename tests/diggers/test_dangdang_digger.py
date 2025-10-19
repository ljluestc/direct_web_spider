"""
Comprehensive unit tests for spider.digger.dangdang_digger
"""
import pytest
from unittest.mock import Mock
from spider.digger.dangdang_digger import DangdangDigger
from spider.digger import Digger


@pytest.mark.unit
@pytest.mark.digger
@pytest.mark.unit
class TestDangdangDiggerBase:
    """Test cases for DangdangDigger base functionality"""

    def test_dangdang_digger_exists(self):
        """Test DangdangDigger exists"""
        assert DangdangDigger is not None

    def test_dangdang_digger_inherits_digger(self):
        """Test DangdangDigger inherits from Digger"""
        assert issubclass(DangdangDigger, Digger)


@pytest.mark.unit
@pytest.mark.digger
@pytest.mark.unit
class TestDangdangDiggerProductList:
    """Test cases for DangdangDigger product_list method"""

    def test_product_list_single_product(self):
        """Test product_list with single product"""
        html = """
        <html>
            <div class="mode_goods">
                <div class="name">
                    <a href="http://product.dangdang.com/123.html">Product 1</a>
                </div>
            </div>
        </html>
        """
        item = Mock(html=html, url="http://category.dangdang.com")
        digger = DangdangDigger(item)

        urls = digger.product_list()
        assert len(urls) == 1
        assert urls[0] == "http://product.dangdang.com/123.html"

    def test_product_list_multiple_products(self):
        """Test product_list with multiple products"""
        html = """
        <html>
            <div class="mode_goods">
                <div class="name"><a href="http://product.dangdang.com/1.html">Product 1</a></div>
                <div class="name"><a href="http://product.dangdang.com/2.html">Product 2</a></div>
                <div class="name"><a href="http://product.dangdang.com/3.html">Product 3</a></div>
            </div>
        </html>
        """
        item = Mock(html=html, url="http://category.dangdang.com")
        digger = DangdangDigger(item)

        urls = digger.product_list()
        assert len(urls) == 3
        assert "http://product.dangdang.com/1.html" in urls
        assert "http://product.dangdang.com/2.html" in urls
        assert "http://product.dangdang.com/3.html" in urls

    def test_product_list_no_products(self):
        """Test product_list with no products"""
        html = """
        <html>
            <div class="mode_goods">
                <div class="name"><span>No link</span></div>
            </div>
        </html>
        """
        item = Mock(html=html, url="http://category.dangdang.com")
        digger = DangdangDigger(item)

        urls = digger.product_list()
        assert len(urls) == 0

    def test_product_list_filters_empty_hrefs(self):
        """Test product_list filters out elements without href"""
        html = """
        <html>
            <div class="mode_goods">
                <div class="name"><a href="">Empty href</a></div>
                <div class="name"><a>No href</a></div>
                <div class="name"><a href="http://product.dangdang.com/valid.html">Valid</a></div>
            </div>
        </html>
        """
        item = Mock(html=html, url="http://category.dangdang.com")
        digger = DangdangDigger(item)

        urls = digger.product_list()
        assert len(urls) == 1
        assert urls[0] == "http://product.dangdang.com/valid.html"

    def test_product_list_returns_list(self):
        """Test product_list returns a list"""
        html = """
        <html>
            <div class="mode_goods">
                <div class="name"><a href="http://product.dangdang.com/123.html">Product</a></div>
            </div>
        </html>
        """
        item = Mock(html=html, url="http://category.dangdang.com")
        digger = DangdangDigger(item)

        result = digger.product_list()
        assert isinstance(result, list)
