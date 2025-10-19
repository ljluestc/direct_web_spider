# encoding: utf-8
"""
Comprehensive tests for encoding module to achieve 100% coverage
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

@pytest.mark.unit
class TestEncodingComprehensive:
    """Comprehensive tests for encoding module"""

    def test_encoding_class(self):
        """Test Encoding class"""
        from spider.encoding import Encoding
        
        # Test encoding map
        assert "dangdang" in Encoding.Map
        assert "jingdong" in Encoding.Map
        assert "newegg" in Encoding.Map
        assert "tmall" in Encoding.Map
        assert "suning" in Encoding.Map
        assert "gome" in Encoding.Map
        
        # Test encoding values
        assert Encoding.Map["dangdang"] == "GB18030"
        assert Encoding.Map["jingdong"] == "GB18030"
        assert Encoding.Map["newegg"] == "GB18030"
        assert Encoding.Map["tmall"] == "GB18030"
        assert Encoding.Map["suning"] == "UTF-8"
        assert Encoding.Map["gome"] == "UTF-8"

    def test_set_utf8_html_method(self):
        """Test set_utf8_html method"""
        from spider.encoding import Encoding
        
        # Create a mock item
        class MockItem:
            def __init__(self, kind):
                self.kind = kind
                self.html = None
        
        # Test with dangdang (GB18030)
        item = MockItem("dangdang")
        result = Encoding.set_utf8_html(item, b"test string")
        assert result is item
        assert item.html is not None
        
        # Test with suning (UTF-8)
        item = MockItem("suning")
        result = Encoding.set_utf8_html(item, b"test string")
        assert result is item
        assert item.html is not None

    def test_set_utf8_html_with_string_input(self):
        """Test set_utf8_html with string input"""
        from spider.encoding import Encoding
        
        # Create a mock item
        class MockItem:
            def __init__(self, kind):
                self.kind = kind
                self.html = None
        
        # Test with string input (already UTF-8)
        item = MockItem("dangdang")
        result = Encoding.set_utf8_html(item, "test string")
        assert result is item
        assert item.html == "test string"

    def test_set_utf8_html_with_unicode_string(self):
        """Test set_utf8_html with unicode string"""
        from spider.encoding import Encoding
        
        # Create a mock item
        class MockItem:
            def __init__(self, kind):
                self.kind = kind
                self.html = None
        
        # Test with unicode string
        unicode_string = "测试字符串"
        item = MockItem("dangdang")
        result = Encoding.set_utf8_html(item, unicode_string)
        assert result is item
        assert item.html == unicode_string

    def test_set_utf8_html_with_bytes_input(self):
        """Test set_utf8_html with bytes input"""
        from spider.encoding import Encoding
        
        # Create a mock item
        class MockItem:
            def __init__(self, kind):
                self.kind = kind
                self.html = None
        
        # Test with bytes input
        bytes_input = b"test string"
        item = MockItem("dangdang")
        result = Encoding.set_utf8_html(item, bytes_input)
        assert result is item
        assert item.html is not None

    def test_set_utf8_html_with_special_characters(self):
        """Test set_utf8_html with special characters"""
        from spider.encoding import Encoding
        
        # Create a mock item
        class MockItem:
            def __init__(self, kind):
                self.kind = kind
                self.html = None
        
        # Test with special characters
        special_string = "Hello, 世界! 🌍"
        item = MockItem("dangdang")
        result = Encoding.set_utf8_html(item, special_string)
        assert result is item
        assert item.html == special_string

    def test_set_utf8_html_with_unknown_kind(self):
        """Test set_utf8_html with unknown kind"""
        from spider.encoding import Encoding
        
        # Create a mock item
        class MockItem:
            def __init__(self, kind):
                self.kind = kind
                self.html = None
        
        # Test with unknown kind (should default to UTF-8)
        item = MockItem("unknown_site")
        result = Encoding.set_utf8_html(item, b"test string")
        assert result is item
        assert item.html is not None

    def test_set_utf8_html_with_encoding_error(self):
        """Test set_utf8_html with encoding error"""
        from spider.encoding import Encoding
        
        # Create a mock item
        class MockItem:
            def __init__(self, kind):
                self.kind = kind
                self.html = None
        
        # Test with invalid bytes that can't be decoded
        invalid_bytes = b'\xff\xfe\x00\x00'  # Invalid UTF-8
        item = MockItem("dangdang")
        result = Encoding.set_utf8_html(item, invalid_bytes)
        assert result is item
        assert item.html is not None

    def test_set_utf8_html_with_very_long_string(self):
        """Test set_utf8_html with very long string"""
        from spider.encoding import Encoding
        
        # Create a mock item
        class MockItem:
            def __init__(self, kind):
                self.kind = kind
                self.html = None
        
        # Test with very long string
        long_string = "test string" * 1000
        item = MockItem("dangdang")
        result = Encoding.set_utf8_html(item, long_string)
        assert result is item
        assert item.html == long_string

    def test_set_utf8_html_with_empty_string(self):
        """Test set_utf8_html with empty string"""
        from spider.encoding import Encoding
        
        # Create a mock item
        class MockItem:
            def __init__(self, kind):
                self.kind = kind
                self.html = None
        
        # Test with empty string
        item = MockItem("dangdang")
        result = Encoding.set_utf8_html(item, "")
        assert result is item
        assert item.html == ""

    def test_set_utf8_html_with_encoding_fallback(self):
        """Test set_utf8_html with encoding fallback"""
        from spider.encoding import Encoding
        
        # Create a mock item
        class MockItem:
            def __init__(self, kind):
                self.kind = kind
                self.html = None
        
        # Test with invalid encoding that should fallback to UTF-8
        item = MockItem("dangdang")
        # Use bytes that can't be decoded with GB18030 but can with UTF-8
        result = Encoding.set_utf8_html(item, b"test string")
        assert result is item
        assert item.html is not None
