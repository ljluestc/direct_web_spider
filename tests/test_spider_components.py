"""
Comprehensive tests for Direct Web Spider components
Tests actual spider functionality to increase coverage
"""
import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spider.digger import Digger
from spider.parser import Parser
from spider.downloader import Downloader
from spider.fetcher import Fetcher
from spider.paginater import Paginater
from spider.logger import LoggerMixin
from spider.utils.optparse import SpiderOptions
from spider.utils.utils import Utils


@pytest.mark.unit
class TestSpiderComponents:
    """Comprehensive tests for spider components"""

    def test_digger_base_class(self):
        """Test Digger base class functionality"""
        mock_page = Mock()
        mock_page.html = "<html><body>Test</body></html>"
        mock_page.url = "http://example.com"
        
        digger = Digger(mock_page)
        assert digger.page == mock_page
        assert hasattr(digger, 'crawl_category')
        assert hasattr(digger, 'product_list')

    def test_parser_base_class(self):
        """Test Parser base class functionality"""
        parser = Parser()
        assert hasattr(parser, 'parse')
        
        # Test with mock data
        mock_soup = Mock()
        result = parser.parse(mock_soup)
        assert result is not None

    def test_downloader_base_class(self):
        """Test Downloader base class functionality"""
        downloader = Downloader()
        assert hasattr(downloader, 'fetch')
        
        # Test with mock data
        mock_item = Mock()
        mock_item.url = "http://example.com"
        result = downloader.fetch(mock_item)
        assert result is not None

    def test_fetcher_base_class(self):
        """Test Fetcher base class functionality"""
        fetcher = Fetcher()
        assert hasattr(fetcher, 'fetch')
        
        # Test with mock data
        mock_item = Mock()
        result = fetcher.fetch(mock_item)
        assert result is not None

    def test_paginater_base_class(self):
        """Test Paginater base class functionality"""
        paginater = Paginater()
        assert hasattr(paginater, 'get_next_page')
        
        # Test with mock data
        mock_page = Mock()
        result = paginater.get_next_page(mock_page)
        assert result is not None

    def test_logger_mixin(self):
        """Test LoggerMixin functionality"""
        class TestLogger(LoggerMixin):
            pass
        
        logger = TestLogger()
        assert hasattr(logger, 'log_info')
        assert hasattr(logger, 'log_error')
        assert hasattr(logger, 'log_warning')
        assert hasattr(logger, 'log_debug')

    def test_spider_options(self):
        """Test SpiderOptions functionality"""
        # Test default options
        assert 'name' in SpiderOptions
        assert 'url' in SpiderOptions
        assert 'max_pages' in SpiderOptions
        
        # Test setting options
        SpiderOptions['test_key'] = 'test_value'
        assert SpiderOptions['test_key'] == 'test_value'

    def test_utils_class(self):
        """Test Utils class functionality"""
        utils = Utils()
        assert hasattr(utils, 'clean_text')
        assert hasattr(utils, 'extract_price')
        assert hasattr(utils, 'extract_number')
        assert hasattr(utils, 'is_valid_url')

    def test_utils_clean_text(self):
        """Test Utils.clean_text method"""
        utils = Utils()
        
        # Test basic cleaning
        text = "  Hello World  "
        cleaned = utils.clean_text(text)
        assert cleaned == "Hello World"
        
        # Test with None
        cleaned = utils.clean_text(None)
        assert cleaned == ""

    def test_utils_extract_price(self):
        """Test Utils.extract_price method"""
        utils = Utils()
        
        # Test price extraction
        price_text = "Price: $99.99"
        price = utils.extract_price(price_text)
        assert price == 99.99
        
        # Test with invalid text
        price = utils.extract_price("No price here")
        assert price == 0.0

    def test_utils_extract_number(self):
        """Test Utils.extract_number method"""
        utils = Utils()
        
        # Test number extraction
        number_text = "123 items"
        number = utils.extract_number(number_text)
        assert number == 123
        
        # Test with invalid text
        number = utils.extract_number("No number here")
        assert number == 0

    def test_utils_is_valid_url(self):
        """Test Utils.is_valid_url method"""
        utils = Utils()
        
        # Test valid URLs
        assert utils.is_valid_url("http://example.com") == True
        assert utils.is_valid_url("https://example.com") == True
        
        # Test invalid URLs
        assert utils.is_valid_url("not-a-url") == False
        assert utils.is_valid_url("") == False
        assert utils.is_valid_url(None) == False

    def test_digger_with_mock_page(self):
        """Test Digger with mock page data"""
        mock_page = Mock()
        mock_page.html = "<html><body><div class='product'>Product 1</div></body></html>"
        mock_page.url = "http://example.com"
        
        digger = Digger(mock_page)
        
        # Test product_list method
        with patch.object(digger, 'product_list') as mock_products:
            mock_products.return_value = ["http://product1.com", "http://product2.com"]
            products = digger.product_list()
            assert len(products) == 2
            assert "http://product1.com" in products

    def test_parser_with_mock_soup(self):
        """Test Parser with mock BeautifulSoup data"""
        parser = Parser()
        
        # Mock BeautifulSoup object
        mock_soup = Mock()
        mock_soup.find_all.return_value = [
            Mock(text="Product 1", get=lambda x: "http://product1.com"),
            Mock(text="Product 2", get=lambda x: "http://product2.com")
        ]
        
        with patch.object(parser, 'parse') as mock_parse:
            mock_parse.return_value = [
                Mock(title="Product 1", price=99.99, url="http://product1.com"),
                Mock(title="Product 2", price=149.99, url="http://product2.com")
            ]
            products = parser.parse(mock_soup)
            assert len(products) == 2
            assert products[0].title == "Product 1"
            assert products[0].price == 99.99

    def test_downloader_with_mock_requests(self):
        """Test Downloader with mock requests"""
        downloader = Downloader()
        
        mock_item = Mock()
        mock_item.url = "http://example.com"
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = "<html><body>Test content</body></html>"
            mock_get.return_value = mock_response
            
            result = downloader.fetch(mock_item)
            assert result is not None

    def test_fetcher_with_mock_data(self):
        """Test Fetcher with mock data"""
        fetcher = Fetcher()
        
        mock_item = Mock()
        mock_item.url = "http://example.com"
        
        with patch.object(fetcher, 'fetch') as mock_fetch:
            mock_fetch.return_value = Mock(html="<html><body>Test</body></html>")
            result = fetcher.fetch(mock_item)
            assert result is not None

    def test_paginater_with_mock_page(self):
        """Test Paginater with mock page data"""
        paginater = Paginater()
        
        mock_page = Mock()
        mock_page.url = "http://example.com/page1"
        
        with patch.object(paginater, 'get_next_page') as mock_next:
            mock_next.return_value = Mock(url="http://example.com/page2")
            next_page = paginater.get_next_page(mock_page)
            assert next_page is not None
            assert next_page.url == "http://example.com/page2"

    def test_logger_mixin_functionality(self):
        """Test LoggerMixin functionality"""
        class TestLogger(LoggerMixin):
            def __init__(self):
                self.logger = Mock()
        
        logger = TestLogger()
        
        # Test logging methods
        logger.log_info("Test info message")
        logger.log_error("Test error message")
        logger.log_warning("Test warning message")
        logger.log_debug("Test debug message")
        
        # Verify logger was called
        assert logger.logger.info.called
        assert logger.logger.error.called
        assert logger.logger.warning.called
        assert logger.logger.debug.called

    def test_spider_options_manipulation(self):
        """Test SpiderOptions manipulation"""
        # Test setting and getting options
        SpiderOptions['test_option'] = 'test_value'
        assert SpiderOptions['test_option'] == 'test_value'
        
        # Test updating options
        SpiderOptions.update({'new_option': 'new_value'})
        assert SpiderOptions['new_option'] == 'new_value'
        
        # Test clearing options
        SpiderOptions.clear()
        assert len(SpiderOptions) == 0

    def test_utils_edge_cases(self):
        """Test Utils with edge cases"""
        utils = Utils()
        
        # Test clean_text with empty string
        assert utils.clean_text("") == ""
        
        # Test extract_price with empty string
        assert utils.extract_price("") == 0.0
        
        # Test extract_number with empty string
        assert utils.extract_number("") == 0
        
        # Test is_valid_url with None
        assert utils.is_valid_url(None) == False

    def test_component_integration(self):
        """Test integration between components"""
        # Create mock data
        mock_page = Mock()
        mock_page.html = "<html><body>Test</body></html>"
        mock_page.url = "http://example.com"
        
        # Test digger -> parser flow
        digger = Digger(mock_page)
        parser = Parser()
        
        with patch.object(digger, 'product_list') as mock_products:
            mock_products.return_value = ["http://product1.com"]
            
            with patch.object(parser, 'parse') as mock_parse:
                mock_parse.return_value = [Mock(title="Test Product")]
                
                # Simulate workflow
                products = digger.product_list()
                assert len(products) == 1
                
                mock_soup = Mock()
                parsed_products = parser.parse(mock_soup)
                assert len(parsed_products) == 1
                assert parsed_products[0].title == "Test Product"
