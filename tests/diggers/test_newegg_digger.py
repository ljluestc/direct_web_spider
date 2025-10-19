"""Comprehensive unit tests for spider.digger.newegg_digger"""
import pytest
from unittest.mock import Mock
from spider.digger.newegg_digger import NeweggDigger
from spider.digger import Digger

@pytest.mark.unit
@pytest.mark.digger
@pytest.mark.unit
class TestNeweggDiggerBase:
    def test_newegg_digger_exists(self):
        assert NeweggDigger is not None
    def test_newegg_digger_inherits_digger(self):
        assert issubclass(NeweggDigger, Digger)

@pytest.mark.unit
@pytest.mark.digger
@pytest.mark.unit
class TestNeweggDiggerProductList:
    def test_product_list_single_product(self):
        html = """<html><div id="itemGrid1"><div class="itemCell"><dt><a href="http://www.newegg.com.cn/Product/123.htm">Product 1</a></dt></div></div></html>"""
        assert len(NeweggDigger(Mock(html=html, url="http://www.newegg.com.cn/ProductList")).product_list()) == 1
    def test_product_list_multiple_products(self):
        html = """<html><div id="itemGrid1"><div class="itemCell"><dt><a href="http://www.newegg.com.cn/Product/1.htm">P1</a></dt></div><div class="itemCell"><dt><a href="http://www.newegg.com.cn/Product/2.htm">P2</a></dt></div></div></html>"""
        assert len(NeweggDigger(Mock(html=html, url="http://www.newegg.com.cn/ProductList")).product_list()) == 2
    def test_product_list_filters_empty_hrefs(self):
        html = """<html><div id="itemGrid1"><div class="itemCell"><dt><a href="">Empty</a></dt></div><div class="itemCell"><dt><a href="http://www.newegg.com.cn/Product/valid.htm">Valid</a></dt></div></div></html>"""
        assert len(NeweggDigger(Mock(html=html, url="http://www.newegg.com.cn")).product_list()) == 1
    def test_product_list_returns_list(self):
        html = """<html><div id="itemGrid1"><div class="itemCell"><dt><a href="http://www.newegg.com.cn/Product/1.htm">P</a></dt></div></div></html>"""
        assert isinstance(NeweggDigger(Mock(html=html, url="http://www.newegg.com.cn")).product_list(), list)
