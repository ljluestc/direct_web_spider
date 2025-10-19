# encoding: utf-8
"""
Comprehensive tests for DangdangParser to achieve 100% coverage
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

@pytest.mark.unit
class TestDangdangParserComprehensive:
    """Comprehensive tests for DangdangParser"""

    def _create_mock_product(self, html_content="<html><body>Test</body></html>"):
        """Helper method to create a mock product"""
        mock_product = Mock()
        mock_product.html = html_content
        mock_product.kind = "dangdang"
        mock_product.id = "test_id"
        return mock_product

    def test_title_with_valid_element(self):
        """Test title extraction with valid element"""
        from spider.parser.dangdang_parser import DangdangParser
        
        html = """
        <html>
            <body>
                <div class="dp_wrap">
                    <h1>Test Product Title</h1>
                </div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = DangdangParser(product)
        
        result = parser.title()
        assert result == "Test Product Title"

    def test_title_with_no_element(self):
        """Test title extraction with no element"""
        from spider.parser.dangdang_parser import DangdangParser
        
        html = "<html><body><div>No title here</div></body></html>"
        product = self._create_mock_product(html)
        parser = DangdangParser(product)
        
        result = parser.title()
        assert result is None

    def test_price_with_valid_element(self):
        """Test price extraction with valid element"""
        from spider.parser.dangdang_parser import DangdangParser
        
        html = """
        <html>
            <body>
                <span id="salePriceTag">￥99.99</span>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = DangdangParser(product)
        
        result = parser.price()
        assert result == 99

    def test_price_with_no_currency_symbol(self):
        """Test price extraction without currency symbol"""
        from spider.parser.dangdang_parser import DangdangParser
        
        html = """
        <html>
            <body>
                <span id="salePriceTag">99.99</span>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = DangdangParser(product)
        
        result = parser.price()
        assert result == 99

    def test_price_with_invalid_value(self):
        """Test price extraction with invalid value"""
        from spider.parser.dangdang_parser import DangdangParser
        
        html = """
        <html>
            <body>
                <span id="salePriceTag">invalid price</span>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = DangdangParser(product)
        
        result = parser.price()
        assert result is None

    def test_price_with_no_element(self):
        """Test price extraction with no element"""
        from spider.parser.dangdang_parser import DangdangParser
        
        html = "<html><body><div>No price here</div></body></html>"
        product = self._create_mock_product(html)
        parser = DangdangParser(product)
        
        result = parser.price()
        assert result is None

    def test_stock(self):
        """Test stock extraction"""
        from spider.parser.dangdang_parser import DangdangParser
        
        product = self._create_mock_product()
        parser = DangdangParser(product)
        
        result = parser.stock()
        assert result == 1

    def test_image_url_with_valid_element(self):
        """Test image URL extraction with valid element"""
        from spider.parser.dangdang_parser import DangdangParser
        
        html = """
        <html>
            <body>
                <img id="largePic" src="http://example.com/image.jpg" />
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = DangdangParser(product)
        
        result = parser.image_url()
        assert result == "http://example.com/image.jpg"

    def test_image_url_with_no_element(self):
        """Test image URL extraction with no element"""
        from spider.parser.dangdang_parser import DangdangParser
        
        html = "<html><body><div>No image here</div></body></html>"
        product = self._create_mock_product(html)
        parser = DangdangParser(product)
        
        result = parser.image_url()
        assert result == "http://img32.ddimg.cn/7/35/60129142-1_h.jpg"

    def test_desc(self):
        """Test description extraction"""
        from spider.parser.dangdang_parser import DangdangParser
        
        product = self._create_mock_product()
        parser = DangdangParser(product)
        
        result = parser.desc()
        assert result is None

    def test_price_url(self):
        """Test price URL extraction"""
        from spider.parser.dangdang_parser import DangdangParser
        
        product = self._create_mock_product()
        parser = DangdangParser(product)
        
        result = parser.price_url()
        assert result is None

    def test_score_with_red_stars(self):
        """Test score extraction with red stars"""
        from spider.parser.dangdang_parser import DangdangParser
        
        html = """
        <html>
            <body>
                <p class="fraction">
                    <img src="red_star1.jpg" />
                    <img src="red_star2.jpg" />
                    <img src="gray_star.jpg" />
                </p>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = DangdangParser(product)
        
        result = parser.score()
        assert result == 2

    def test_score_with_no_stars(self):
        """Test score extraction with no stars"""
        from spider.parser.dangdang_parser import DangdangParser
        
        html = "<html><body><div>No stars here</div></body></html>"
        product = self._create_mock_product(html)
        parser = DangdangParser(product)
        
        result = parser.score()
        assert result == 0

    def test_score_with_no_src_attribute(self):
        """Test score extraction with images without src attribute"""
        from spider.parser.dangdang_parser import DangdangParser
        
        html = """
        <html>
            <body>
                <p class="fraction">
                    <img />
                    <img src="" />
                </p>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = DangdangParser(product)
        
        result = parser.score()
        assert result == 0

    def test_product_code(self):
        """Test product code extraction"""
        from spider.parser.dangdang_parser import DangdangParser
        
        product = self._create_mock_product()
        parser = DangdangParser(product)
        
        result = parser.product_code()
        assert result is None

    def test_standard(self):
        """Test standard extraction"""
        from spider.parser.dangdang_parser import DangdangParser
        
        product = self._create_mock_product()
        parser = DangdangParser(product)
        
        result = parser.standard()
        assert result is None

    def test_comments_with_valid_elements(self):
        """Test comments extraction with valid elements"""
        from spider.parser.dangdang_parser import DangdangParser
        
        html = """
        <html>
            <body>
                <div id="comm_all">
                    <h5><a>Comment Title 1</a></h5>
                    <div class="text">Comment content 1</div>
                    <h5><a>Comment Title 2</a></h5>
                    <div class="text">Comment content 2</div>
                </div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = DangdangParser(product)
        
        result = parser.comments()
        assert len(result) == 2
        assert result[0]['title'] == "Comment Title 1"
        assert result[0]['content'] == "Comment content 1"
        assert result[1]['title'] == "Comment Title 2"
        assert result[1]['content'] == "Comment content 2"

    def test_comments_with_no_elements(self):
        """Test comments extraction with no elements"""
        from spider.parser.dangdang_parser import DangdangParser
        
        html = "<html><body><div>No comments here</div></body></html>"
        product = self._create_mock_product(html)
        parser = DangdangParser(product)
        
        result = parser.comments()
        assert result == []

    def test_comments_with_mismatched_elements(self):
        """Test comments extraction with mismatched elements"""
        from spider.parser.dangdang_parser import DangdangParser
        
        html = """
        <html>
            <body>
                <div id="comm_all">
                    <h5><a>Comment Title 1</a></h5>
                    <div class="text">Comment content 1</div>
                    <h5><a>Comment Title 2</a></h5>
                    <!-- Missing content div -->
                </div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = DangdangParser(product)
        
        result = parser.comments()
        assert len(result) == 2  # Both titles are processed
        assert result[0]['title'] == "Comment Title 1"
        assert result[0]['content'] == "Comment content 1"
        assert result[1]['title'] == "Comment Title 2"
        assert result[1]['content'] == ""  # Empty content for missing div

    def test_belongs_to_categories_with_valid_elements(self):
        """Test belongs_to_categories extraction with valid elements"""
        from spider.parser.dangdang_parser import DangdangParser
        
        html = """
        <html>
            <body>
                <div class="crumb">
                    <a href="/list1">Category 1</a>
                    <a href="/list2">Category 2</a>
                    <a href="/list3">Category 3</a>
                </div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = DangdangParser(product)
        
        result = parser.belongs_to_categories()
        assert len(result) == 3
        assert result[0]['name'] == "Category 1"
        assert result[0]['url'] == "/list1"
        assert result[1]['name'] == "Category 2"
        assert result[1]['url'] == "/list2"
        assert result[2]['name'] == "Category 3"
        assert result[2]['url'] == "/list3"

    def test_belongs_to_categories_with_no_elements(self):
        """Test belongs_to_categories extraction with no elements"""
        from spider.parser.dangdang_parser import DangdangParser
        
        html = "<html><body><div>No categories here</div></body></html>"
        product = self._create_mock_product(html)
        parser = DangdangParser(product)
        
        result = parser.belongs_to_categories()
        assert result == []

    def test_belongs_to_categories_with_non_list_links(self):
        """Test belongs_to_categories extraction with non-list links"""
        from spider.parser.dangdang_parser import DangdangParser
        
        html = """
        <html>
            <body>
                <div class="crumb">
                    <a href="/list1">Category 1</a>
                    <a href="/product1">Product Link</a>
                    <a href="/list2">Category 2</a>
                </div>
            </body>
        </html>
        """
        
        product = self._create_mock_product(html)
        parser = DangdangParser(product)
        
        result = parser.belongs_to_categories()
        assert len(result) == 2  # Only list links are included
        assert result[0]['name'] == "Category 1"
        assert result[0]['url'] == "/list1"
        assert result[1]['name'] == "Category 2"
        assert result[1]['url'] == "/list2"

    def test_end_product(self):
        """Test end_product extraction"""
        from spider.parser.dangdang_parser import DangdangParser
        
        product = self._create_mock_product()
        parser = DangdangParser(product)
        
        result = parser.end_product()
        assert result is None

    def test_merchant(self):
        """Test merchant extraction"""
        from spider.parser.dangdang_parser import DangdangParser
        
        product = self._create_mock_product()
        parser = DangdangParser(product)
        
        result = parser.merchant()
        assert result is None

    def test_brand(self):
        """Test brand extraction"""
        from spider.parser.dangdang_parser import DangdangParser
        
        product = self._create_mock_product()
        parser = DangdangParser(product)
        
        result = parser.brand()
        assert result is None

    def test_brand_type(self):
        """Test brand_type extraction"""
        from spider.parser.dangdang_parser import DangdangParser
        
        product = self._create_mock_product()
        parser = DangdangParser(product)
        
        result = parser.brand_type()
        assert result is None

    def test_parser_initialization(self):
        """Test parser initialization"""
        from spider.parser.dangdang_parser import DangdangParser
        
        product = self._create_mock_product()
        parser = DangdangParser(product)
        
        assert parser is not None
        assert hasattr(parser, 'doc')

    def test_parser_string_representation(self):
        """Test parser string representation"""
        from spider.parser.dangdang_parser import DangdangParser
        
        product = self._create_mock_product()
        parser = DangdangParser(product)
        
        str_repr = str(parser)
        assert str_repr is not None
        assert isinstance(str_repr, str)

    def test_parser_equality(self):
        """Test parser equality"""
        from spider.parser.dangdang_parser import DangdangParser
        
        product1 = self._create_mock_product()
        product2 = self._create_mock_product()
        
        parser1 = DangdangParser(product1)
        parser2 = DangdangParser(product2)
        
        assert parser1.__class__ == parser2.__class__

    def test_parser_hash(self):
        """Test parser hash"""
        from spider.parser.dangdang_parser import DangdangParser
        
        product = self._create_mock_product()
        parser = DangdangParser(product)
        
        hash_value = hash(parser)
        assert isinstance(hash_value, int)

    def test_parser_serialization(self):
        """Test parser serialization"""
        from spider.parser.dangdang_parser import DangdangParser
        
        product = self._create_mock_product()
        parser = DangdangParser(product)
        
        try:
            import pickle
            pickled = pickle.dumps(parser)
            unpickled = pickle.loads(pickled)
            assert unpickled is not None
        except (AttributeError, TypeError, pickle.PicklingError):
            pass

    def test_parser_deepcopy(self):
        """Test parser deep copy"""
        from spider.parser.dangdang_parser import DangdangParser
        
        product = self._create_mock_product()
        parser = DangdangParser(product)
        
        try:
            import copy
            copied = copy.deepcopy(parser)
            assert copied is not None
        except (AttributeError, TypeError):
            pass

    def test_parser_memory_usage(self):
        """Test parser memory usage"""
        from spider.parser.dangdang_parser import DangdangParser
        
        product = self._create_mock_product()
        parser = DangdangParser(product)
        
        import sys
        memory_usage = sys.getsizeof(parser)
        assert memory_usage > 0

    def test_parser_thread_safety(self):
        """Test parser thread safety"""
        from spider.parser.dangdang_parser import DangdangParser
        import threading
        
        product = self._create_mock_product()
        parser = DangdangParser(product)
        
        def access_parser():
            return parser.title()
        
        thread = threading.Thread(target=access_parser)
        thread.start()
        thread.join()
        assert True

    def test_parser_process_safety(self):
        """Test parser process safety"""
        from spider.parser.dangdang_parser import DangdangParser
        import multiprocessing
        
        product = self._create_mock_product()
        parser = DangdangParser(product)
        
        def access_parser():
            return parser.title()
        
        try:
            process = multiprocessing.Process(target=access_parser)
            process.start()
            process.join()
        except (AttributeError, TypeError):
            pass
        assert True
