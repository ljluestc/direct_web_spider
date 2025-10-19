"""
Comprehensive unit tests for spider.digger.jingdong_digger
"""
import pytest
from unittest.mock import Mock
from spider.digger.jingdong_digger import JingdongDigger
from spider.digger import Digger


@pytest.mark.unit
@pytest.mark.digger
@pytest.mark.unit
class TestJingdongDiggerBase:
    """Test cases for JingdongDigger base functionality"""

    def test_jingdong_digger_exists(self):
        """Test JingdongDigger exists"""
        assert JingdongDigger is not None

    def test_jingdong_digger_inherits_digger(self):
        """Test JingdongDigger inherits from Digger"""
        assert issubclass(JingdongDigger, Digger)


@pytest.mark.unit
@pytest.mark.digger
@pytest.mark.unit
class TestJingdongDiggerProductList:
    """Test cases for JingdongDigger product_list method"""

    def test_product_list_single_product(self):
        """Test product_list with single product"""
        html = """<html><div id="plist"><ul class="list-h"><div class="p-img"><a href="http://item.jd.com/123.html">Product 1</a></div></ul></div></html>"""
        item = Mock(html=html, url="http://list.jd.com")
        digger = JingdongDigger(item)
        urls = digger.product_list()
        assert len(urls) == 1

    def test_product_list_multiple_products(self):
        """Test product_list with multiple products"""
        html = """<html><div id="plist"><ul class="list-h"><div class="p-img"><a href="http://item.jd.com/1.html">Product 1</a></div><div class="p-img"><a href="http://item.jd.com/2.html">Product 2</a></div></ul></div></html>"""
        item = Mock(html=html, url="http://list.jd.com")
        digger = JingdongDigger(item)
        urls = digger.product_list()
        assert len(urls) == 2

    def test_product_list_filters_empty_hrefs(self):
        """Test product_list filters out empty hrefs"""
        html = """<html><div id="plist"><ul class="list-h"><div class="p-img"><a href="">Empty</a></div><div class="p-img"><a href="http://item.jd.com/valid.html">Valid</a></div></ul></div></html>"""
        item = Mock(html=html, url="http://list.jd.com")
        digger = JingdongDigger(item)
        urls = digger.product_list()
        assert len(urls) == 1

    def test_product_list_returns_list(self):
        """Test product_list returns a list"""
        html = """<html><div id="plist"><ul class="list-h"><div class="p-img"><a href="http://item.jd.com/1.html">Product</a></div></ul></div></html>"""
        item = Mock(html=html, url="http://list.jd.com")
        result = JingdongDigger(item).product_list()
        assert isinstance(result, list)
