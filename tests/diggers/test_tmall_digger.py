"""Comprehensive unit tests for spider.digger.tmall_digger"""
import pytest
from unittest.mock import Mock
from spider.digger.tmall_digger import TmallDigger
from spider.digger import Digger

@pytest.mark.unit
@pytest.mark.digger
@pytest.mark.unit
class TestTmallDiggerBase:
    def test_tmall_digger_exists(self):
        assert TmallDigger is not None
    def test_tmall_digger_inherits_digger(self):
        assert issubclass(TmallDigger, Digger)

@pytest.mark.unit
@pytest.mark.digger
@pytest.mark.unit
class TestTmallDiggerProductList:
    def test_product_list_single_product(self):
        html = """<html><div class="product"><a href="http://detail.tmall.com/item.htm?id=123">Product 1</a></div></html>"""
        digger = TmallDigger(Mock(html=html, url="http://list.tmall.com"))
        assert len(digger.product_list()) == 1
    def test_product_list_multiple_products(self):
        html = """<html><div class="product"><a href="http://detail.tmall.com/1.htm">P1</a></div><div class="product"><a href="http://detail.tmall.com/2.htm">P2</a></div></html>"""
        assert len(TmallDigger(Mock(html=html, url="http://list.tmall.com")).product_list()) == 2
    def test_product_list_filters_empty_hrefs(self):
        html = """<html><div class="product"><a href="">Empty</a></div><div class="product"><a href="http://detail.tmall.com/valid.htm">Valid</a></div></html>"""
        assert len(TmallDigger(Mock(html=html, url="http://list.tmall.com")).product_list()) == 1
    def test_product_list_returns_list(self):
        html = """<html><div class="product"><a href="http://detail.tmall.com/1.htm">P</a></div></html>"""
        assert isinstance(TmallDigger(Mock(html=html, url="http://list.tmall.com")).product_list(), list)
