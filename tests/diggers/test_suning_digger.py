"""Comprehensive unit tests for spider.digger.suning_digger"""
import pytest
from unittest.mock import Mock
from spider.digger.suning_digger import SuningDigger
from spider.digger import Digger

@pytest.mark.unit
@pytest.mark.digger
@pytest.mark.unit
class TestSuningDiggerBase:
    def test_suning_digger_exists(self):
        assert SuningDigger is not None
    def test_suning_digger_inherits_digger(self):
        assert issubclass(SuningDigger, Digger)

@pytest.mark.unit
@pytest.mark.digger
@pytest.mark.unit
class TestSuningDiggerProductList:
    def test_product_list_single_product(self):
        html = """<html><div id="product_container"><li><div class="pro_img"><a href="/product/123.html">Product 1</a></div></li></div></html>"""
        urls = SuningDigger(Mock(html=html, url="http://www.suning.com")).product_list()
        assert len(urls) == 1
        assert urls[0] == "http://www.suning.com/product/123.html"
    def test_product_list_multiple_products(self):
        html = """<html><div id="product_container"><li><div class="pro_img"><a href="/product/1.html">P1</a></div></li><li><div class="pro_img"><a href="/product/2.html">P2</a></div></li></div></html>"""
        assert len(SuningDigger(Mock(html=html, url="http://www.suning.com")).product_list()) == 2
    def test_product_list_prepends_base_url(self):
        html = """<html><div id="product_container"><li><div class="pro_img"><a href="/product/test.html">Test</a></div></li></div></html>"""
        urls = SuningDigger(Mock(html=html, url="http://www.suning.com")).product_list()
        assert urls[0].startswith("http://www.suning.com")
    def test_product_list_filters_empty_hrefs(self):
        html = """<html><div id="product_container"><li><div class="pro_img"><a href="">Empty</a></div></li><li><div class="pro_img"><a href="/product/valid.html">Valid</a></div></li></div></html>"""
        assert len(SuningDigger(Mock(html=html, url="http://www.suning.com")).product_list()) == 1
    def test_product_list_returns_list(self):
        html = """<html><div id="product_container"><li><div class="pro_img"><a href="/product/1.html">P</a></div></li></div></html>"""
        assert isinstance(SuningDigger(Mock(html=html, url="http://www.suning.com")).product_list(), list)
