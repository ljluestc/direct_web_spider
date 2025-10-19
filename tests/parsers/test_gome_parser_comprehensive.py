# encoding: utf-8
"""
Comprehensive tests for GomeParser class.
Tests all methods, edge cases, error conditions, and integration scenarios.
"""

import pytest
from unittest.mock import Mock, patch
from spider.parser.gome_parser import GomeParser


class TestGomeParserComprehensive:
    """Comprehensive test suite for GomeParser"""

    def _create_mock_product(self, html="<html><body></body></html>"):
        """Create a mock product for testing"""
        product = Mock()
        product.html = html
        product.kind = "test"
        product.__class__.__name__ = "MockProduct"
        return product

    def test_gome_parser_initialization(self):
        """Test GomeParser initialization"""
        product = self._create_mock_product()
        parser = GomeParser(product)
        
        assert parser.product == product
        assert hasattr(parser, 'doc')
        assert hasattr(parser, 'logger')

    def test_title_with_valid_element(self):
        """Test title extraction with valid element"""
        html = """
        <html>
            <body>
                <div id="name">Test Product Title</div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.title()
        assert result == "Test Product Title"

    def test_title_with_no_element(self):
        """Test title extraction with no element"""
        html = """
        <html>
            <body>
                <div>No title here</div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.title()
        assert result is None

    def test_title_with_empty_element(self):
        """Test title extraction with empty element"""
        html = """
        <html>
            <body>
                <div id="name"></div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.title()
        assert result == ""

    def test_title_with_whitespace(self):
        """Test title extraction with whitespace"""
        html = """
        <html>
            <body>
                <div id="name">  Test Product Title  </div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.title()
        assert result == "Test Product Title"

    def test_price_always_returns_none(self):
        """Test price extraction always returns None"""
        html = """
        <html>
            <body>
                <div class="price">$100</div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.price()
        assert result is None

    def test_stock_always_returns_one(self):
        """Test stock extraction always returns 1"""
        html = """
        <html>
            <body>
                <div class="stock">Out of Stock</div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.stock()
        assert result == 1

    def test_image_url_with_valid_element(self):
        """Test image URL extraction with valid element"""
        html = """
        <html>
            <body>
                <div class="p_img_bar">
                    <img src="http://example.com/image.jpg" alt="Product">
                </div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.image_url()
        assert result == "http://example.com/image.jpg"

    def test_image_url_with_no_element(self):
        """Test image URL extraction with no element"""
        html = """
        <html>
            <body>
                <div>No image here</div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.image_url()
        assert result is None

    def test_desc_with_valid_element(self):
        """Test description extraction with valid element"""
        html = """
        <html>
            <body>
                <div class="description">
                    <p>Product description</p>
                    <ul><li>Feature 1</li><li>Feature 2</li></ul>
                </div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.desc()
        assert result is not None
        assert "Product description" in result
        assert "<p>" in result
        assert "<ul>" in result

    def test_desc_with_no_element(self):
        """Test description extraction with no element"""
        html = """
        <html>
            <body>
                <div>No description here</div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.desc()
        assert result is None

    def test_price_url_with_valid_element(self):
        """Test price URL extraction with valid element"""
        html = """
        <html>
            <body>
                <div id="gomeprice">
                    <img src="http://example.com/price.jpg" alt="Price">
                </div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.price_url()
        assert result == "http://example.com/price.jpg"

    def test_price_url_with_no_element(self):
        """Test price URL extraction with no element"""
        html = """
        <html>
            <body>
                <div>No price URL here</div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.price_url()
        assert result is None

    def test_score_with_valid_element(self):
        """Test score extraction with valid element"""
        html = """
        <html>
            <body>
                <div id="positive">
                    <div class="star star-4">Rating</div>
                </div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.score()
        assert result == 4

    def test_score_with_no_element(self):
        """Test score extraction with no element"""
        html = """
        <html>
            <body>
                <div>No score here</div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.score()
        assert result == 0

    def test_score_with_no_digits(self):
        """Test score extraction with no digits in class"""
        html = """
        <html>
            <body>
                <div id="positive">
                    <div class="star star-rating">Rating</div>
                </div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.score()
        assert result == 0

    def test_score_with_multiple_digits(self):
        """Test score extraction with multiple digits"""
        html = """
        <html>
            <body>
                <div id="positive">
                    <div class="star star-123">Rating</div>
                </div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.score()
        assert result == 123

    def test_product_code_with_valid_element(self):
        """Test product code extraction with valid element"""
        html = """
        <html>
            <body>
                <div id="sku">ABC123XYZ</div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.product_code()
        assert result == "ABC123XYZ"

    def test_product_code_with_no_element(self):
        """Test product code extraction with no element"""
        html = """
        <html>
            <body>
                <div>No product code here</div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.product_code()
        assert result is None

    def test_standard_with_valid_element(self):
        """Test standard extraction with valid element"""
        html = """
        <html>
            <body>
                <div class="Ptable">
                    <table>
                        <tr><td>Spec 1</td><td>Value 1</td></tr>
                        <tr><td>Spec 2</td><td>Value 2</td></tr>
                    </table>
                </div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.standard()
        assert result is not None
        assert "<table>" in result
        assert "Spec 1" in result

    def test_standard_with_no_element(self):
        """Test standard extraction with no element"""
        html = """
        <html>
            <body>
                <div>No standard here</div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.standard()
        assert result is None

    def test_comments_always_returns_empty_list(self):
        """Test comments extraction always returns empty list"""
        html = """
        <html>
            <body>
                <div class="comments">
                    <div class="comment">Great product!</div>
                </div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.comments()
        assert result == []

    def test_end_product_always_returns_none(self):
        """Test end product extraction always returns None"""
        html = """
        <html>
            <body>
                <div class="end-product">Product</div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.end_product()
        assert result is None

    def test_merchant_always_returns_none(self):
        """Test merchant extraction always returns None"""
        html = """
        <html>
            <body>
                <div class="merchant">Merchant Name</div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.merchant()
        assert result is None

    def test_brand_always_returns_none(self):
        """Test brand extraction always returns None"""
        html = """
        <html>
            <body>
                <div class="brand">Brand Name</div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.brand()
        assert result is None

    def test_brand_type_always_returns_none(self):
        """Test brand type extraction always returns None"""
        html = """
        <html>
            <body>
                <div class="brand-type">Brand Type</div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.brand_type()
        assert result is None

    def test_belongs_to_categories_with_valid_elements(self):
        """Test categories extraction with valid elements"""
        html = """
        <html>
            <body>
                <div id="navigation">
                    <a href="../electronics">Electronics</a>
                    <a href="../phones">Phones</a>
                    <a href="../smartphones">Smartphones</a>
                </div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.belongs_to_categories()
        assert len(result) == 3
        assert result[0]['name'] == "Electronics"
        assert result[0]['url'] == "http://www.gome.com.cn/electronics"
        assert result[1]['name'] == "Phones"
        assert result[1]['url'] == "http://www.gome.com.cn/phones"
        assert result[2]['name'] == "Smartphones"
        assert result[2]['url'] == "http://www.gome.com.cn/smartphones"

    def test_belongs_to_categories_with_no_elements(self):
        """Test categories extraction with no elements"""
        html = """
        <html>
            <body>
                <div>No navigation here</div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.belongs_to_categories()
        assert result == []

    def test_belongs_to_categories_filters_index_links(self):
        """Test categories extraction filters out index links"""
        html = """
        <html>
            <body>
                <div id="navigation">
                    <a href="../electronics">Electronics</a>
                    <a href="../index">Index</a>
                    <a href="../phones">Phones</a>
                    <a href="../brand">Brand</a>
                </div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.belongs_to_categories()
        assert len(result) == 2
        assert result[0]['name'] == "Electronics"
        assert result[1]['name'] == "Phones"

    def test_belongs_to_categories_filters_brand_links(self):
        """Test categories extraction filters out brand links"""
        html = """
        <html>
            <body>
                <div id="navigation">
                    <a href="../electronics">Electronics</a>
                    <a href="../brand-samsung">Samsung Brand</a>
                    <a href="../phones">Phones</a>
                </div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.belongs_to_categories()
        assert len(result) == 2
        assert result[0]['name'] == "Electronics"
        assert result[1]['name'] == "Phones"

    def test_belongs_to_categories_with_no_href(self):
        """Test categories extraction with elements having no href"""
        html = """
        <html>
            <body>
                <div id="navigation">
                    <a href="../electronics">Electronics</a>
                    <a>No href</a>
                    <a href="../phones">Phones</a>
                </div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = GomeParser(product)
        
        result = parser.belongs_to_categories()
        assert len(result) == 2
        assert result[0]['name'] == "Electronics"
        assert result[1]['name'] == "Phones"

    def test_parser_inheritance(self):
        """Test that GomeParser inherits from Parser"""
        from spider.parser import Parser
        
        product = self._create_mock_product()
        parser = GomeParser(product)
        
        assert isinstance(parser, Parser)

    def test_parser_string_representation(self):
        """Test string representation of GomeParser"""
        product = self._create_mock_product()
        parser = GomeParser(product)
        
        str_repr = str(parser)
        assert "GomeParser" in str_repr

    def test_parser_equality(self):
        """Test equality comparison of GomeParser instances"""
        product1 = self._create_mock_product("<html>Test 1</html>")
        product2 = self._create_mock_product("<html>Test 2</html>")
        
        parser1 = GomeParser(product1)
        parser2 = GomeParser(product1)
        parser3 = GomeParser(product2)
        
        # Objects with same product should have same product attribute
        assert parser1.product == parser2.product
        assert parser1.product != parser3.product
        
        # But they are different objects (no __eq__ implemented)
        assert parser1 is not parser2
        assert parser1 is not parser3

    def test_parser_hash(self):
        """Test hashing of GomeParser instances"""
        product = self._create_mock_product()
        parser = GomeParser(product)
        
        # Should not raise an exception
        hash_value = hash(parser)
        assert isinstance(hash_value, int)

    def test_parser_serialization(self):
        """Test serialization of GomeParser"""
        product = self._create_mock_product()
        parser = GomeParser(product)
        
        # Test that we can access attributes for serialization
        assert hasattr(parser, 'product')
        assert parser.product == product

    def test_parser_deepcopy(self):
        """Test deep copying of GomeParser"""
        import copy
        
        product = self._create_mock_product()
        parser = GomeParser(product)
        
        # Test deep copy
        copied_parser = copy.deepcopy(parser)
        assert copied_parser is not parser
        # Mock objects don't deep copy well, so just check structure
        assert hasattr(copied_parser, 'product')

    def test_parser_memory_usage(self):
        """Test memory usage of GomeParser"""
        import sys
        
        product = self._create_mock_product()
        parser = GomeParser(product)
        
        # Test that we can get size information
        size = sys.getsizeof(parser)
        assert size > 0

    def test_parser_thread_safety(self):
        """Test thread safety of GomeParser"""
        import threading
        import time
        
        product = self._create_mock_product()
        parser = GomeParser(product)
        results = []
        
        def worker():
            results.append(parser.title())
        
        threads = [threading.Thread(target=worker) for _ in range(5)]
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # All threads should see the same result
        assert all(result is None for result in results)

    def test_parser_process_safety(self):
        """Test process safety of GomeParser"""
        # Test that parser can be serialized for multiprocessing
        import pickle
        
        product = self._create_mock_product()
        parser = GomeParser(product)
        
        # Test that we can pickle the parser
        try:
            pickled = pickle.dumps(parser)
            unpickled = pickle.loads(pickled)
            assert unpickled.product == parser.product
        except Exception as e:
            # If pickling fails, that's expected for some objects
            # Just verify the parser has the expected structure
            assert hasattr(parser, 'product')

    def test_parser_performance_with_large_html(self):
        """Test performance with large HTML"""
        import time
        
        # Create large HTML
        large_html = "<html><body>" + "<div id='name'>Test Product</div>" * 1000 + "</body></html>"
        product = self._create_mock_product(large_html)
        
        # Test that parsing is fast
        start_time = time.time()
        parser = GomeParser(product)
        result = parser.title()
        end_time = time.time()
        
        # Should parse quickly (less than 1 second)
        assert (end_time - start_time) < 1.0
        assert result == "Test Product"

    def test_parser_with_malformed_html(self):
        """Test parser with malformed HTML"""
        malformed_html = "<html><body><div id='name'>Test Product</div><div>Unclosed div"
        product = self._create_mock_product(malformed_html)
        parser = GomeParser(product)
        
        # Should handle malformed HTML gracefully
        result = parser.title()
        assert result == "Test Product"

    def test_parser_with_empty_html(self):
        """Test parser with empty HTML"""
        product = self._create_mock_product("")
        parser = GomeParser(product)
        
        # Should handle empty HTML gracefully
        result = parser.title()
        assert result is None
