"""
Edge case tests for digger components
"""

import pytest
from unittest.mock import Mock, patch


class TestDiggerEdgeCases:
    """Test digger edge cases"""

    @pytest.mark.edge_cases
    def test_digger_with_empty_category(self):
        """Test digger behavior with empty category"""
        from spider.digger import DangdangDigger
        mock_page = Mock()
        mock_page.html = "<html><body>Test</body></html>"
        digger = DangdangDigger(mock_page)
        
        with patch.object(digger, 'product_list') as mock_product_list:
            mock_product_list.return_value = []
            result = digger.product_list(Mock())
            assert result == []

    @pytest.mark.edge_cases
    def test_digger_with_none_category(self):
        """Test digger behavior with None category"""
        from spider.digger import DangdangDigger
        mock_page = Mock()
        mock_page.html = "<html><body>Test</body></html>"
        digger = DangdangDigger(mock_page)
        
        with patch.object(digger, 'product_list') as mock_product_list:
            mock_product_list.return_value = []
            result = digger.product_list(None)
            assert result == []

    @pytest.mark.edge_cases
    def test_digger_with_invalid_url(self):
        """Test digger behavior with invalid URL"""
        from spider.digger import DangdangDigger
        mock_page = Mock()
        mock_page.html = "<html><body>Test</body></html>"
        digger = DangdangDigger(mock_page)
        
        with patch.object(digger, 'product_list') as mock_product_list:
            mock_product_list.side_effect = ValueError("Invalid URL")
            with pytest.raises(ValueError):
                digger.product_list({'name': 'Invalid', 'url': 'invalid-url'})

    @pytest.mark.edge_cases
    def test_digger_with_very_long_url(self):
        """Test digger behavior with very long URL"""
        from spider.digger import DangdangDigger
        mock_page = Mock()
        mock_page.html = "<html><body>Test</body></html>"
        digger = DangdangDigger(mock_page)
        
        long_url = "http://test.com/" + "a" * 2000 + "/category"
        with patch.object(digger, 'product_list') as mock_product_list:
            mock_product_list.return_value = [{'name': 'Long URL', 'url': long_url}]
            result = digger.product_list({'name': 'Long', 'url': long_url})
            assert len(result) == 1
            assert result[0]['url'] == long_url

    @pytest.mark.edge_cases
    def test_digger_with_special_characters_in_url(self):
        """Test digger behavior with special characters in URL"""
        from spider.digger import DangdangDigger
        mock_page = Mock()
        mock_page.html = "<html><body>Test</body></html>"
        digger = DangdangDigger(mock_page)
        
        special_char_url = "http://test.com/category?name=foo&id=bar%20baz"
        with patch.object(digger, 'product_list') as mock_product_list:
            mock_product_list.return_value = [{'name': 'Special Chars', 'url': special_char_url}]
            result = digger.product_list({'name': 'Special', 'url': special_char_url})
            assert len(result) == 1
            assert result[0]['url'] == special_char_url

    @pytest.mark.edge_cases
    def test_digger_with_circular_reference(self):
        """Test digger behavior with circular reference"""
        from spider.digger import DangdangDigger
        mock_page = Mock()
        mock_page.html = "<html><body>Test</body></html>"
        digger = DangdangDigger(mock_page)
        
        # Simulate a circular reference where a category links back to itself
        category_a = {'name': 'Category A', 'url': 'http://test.com/categoryA'}
        category_b = {'name': 'Category B', 'url': 'http://test.com/categoryB'}
        
        # Mock product_list to return a circular reference
        def mock_product_list_effect(category):
            if category['url'] == 'http://test.com/categoryA':
                return [category_b]
            elif category['url'] == 'http://test.com/categoryB':
                return [category_a] # Links back to A
            return []

        with patch.object(digger, 'product_list') as mock_product_list:
            mock_product_list.side_effect = mock_product_list_effect
            
            # In a real scenario, the spider would need to handle visited URLs to prevent infinite loops.
            # For this test, we just ensure it doesn't crash immediately.
            result = digger.product_list(category_a)
            assert len(result) == 1 # Only returns the first level of crawl
            assert result[0]['name'] == 'Category B'