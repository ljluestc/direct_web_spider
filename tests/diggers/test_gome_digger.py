"""Comprehensive unit tests for spider.digger.gome_digger"""
import pytest
from unittest.mock import Mock
from spider.digger.gome_digger import GomeDigger
from spider.digger import Digger

@pytest.mark.unit
@pytest.mark.digger
@pytest.mark.unit
class TestGomeDiggerBase:
    def test_gome_digger_exists(self):
        assert GomeDigger is not None
    def test_gome_digger_inherits_digger(self):
        assert issubclass(GomeDigger, Digger)

@pytest.mark.unit
@pytest.mark.digger
@pytest.mark.unit
class TestGomeDiggerProductList:
    def test_product_list_single_product(self):
        html = """<html><div id="plist"><div class="p-img"><a href="http://item.gome.com.cn/123.html">Product 1</a></div></div></html>"""
        assert len(GomeDigger(Mock(html=html, url="http://www.gome.com.cn")).product_list()) == 1
    def test_product_list_multiple_products(self):
        html = """<html><div id="plist"><div class="p-img"><a href="http://item.gome.com.cn/1.html">P1</a></div><div class="p-img"><a href="http://item.gome.com.cn/2.html">P2</a></div></div></html>"""
        assert len(GomeDigger(Mock(html=html, url="http://www.gome.com.cn")).product_list()) == 2
    def test_product_list_filters_empty_hrefs(self):
        html = """<html><div id="plist"><div class="p-img"><a href="">Empty</a></div><div class="p-img"><a href="http://item.gome.com.cn/valid.html">Valid</a></div></div></html>"""
        assert len(GomeDigger(Mock(html=html, url="http://www.gome.com.cn")).product_list()) == 1
    def test_product_list_returns_list(self):
        html = """<html><div id="plist"><div class="p-img"><a href="http://item.gome.com.cn/1.html">P</a></div></div></html>"""
        assert isinstance(GomeDigger(Mock(html=html, url="http://www.gome.com.cn")).product_list(), list)
