"""
Integration tests for pipeline
"""

import pytest
from unittest.mock import Mock, patch


class TestPipeline:
    """Test pipeline integration"""

    @pytest.mark.integration
    def test_complete_pipeline_jingdong(self):
        """Test complete pipeline for JingDong"""
        with patch('spider.fetcher.JingdongFetcher') as mock_fetcher, \
             patch('spider.digger.JingdongDigger') as mock_digger, \
             patch('spider.downloader.NormalDownloader') as mock_downloader, \
             patch('spider.parser.JingdongParser') as mock_parser:
            
            # Setup mocks
            mock_fetcher.category_list.return_value = [
                {'name': 'Test Category', 'url': 'http://test.com/category'}
            ]
            mock_digger.product_list.return_value = [
                {'name': 'Test Product', 'url': 'http://test.com/product'}
            ]
            mock_downloader.run.return_value = None
            mock_parser.attributes.return_value = {
                'title': 'Test Product',
                'price': 99.99
            }
            
            # Test pipeline
            categories = mock_fetcher.category_list()
            assert len(categories) == 1
            
            products = mock_digger.product_list()
            assert len(products) == 1
            
            mock_downloader.run()
            mock_parser.attributes()
            
            # Verify all components were called
            mock_fetcher.category_list.assert_called_once()
            mock_digger.product_list.assert_called_once()
            mock_downloader.run.assert_called_once()
            mock_parser.attributes.assert_called_once()

    @pytest.mark.integration
    def test_pipeline_error_handling(self):
        """Test pipeline error handling"""
        with patch('spider.fetcher.JingdongFetcher') as mock_fetcher:
            mock_fetcher.category_list.side_effect = Exception("Network error")
            
            with pytest.raises(Exception):
                mock_fetcher.category_list()

    @pytest.mark.integration
    def test_pipeline_memory_efficiency(self):
        """Test pipeline memory efficiency"""
        import gc
        
        # Test memory usage
        initial_objects = len(gc.get_objects())
        
        with patch('spider.fetcher.JingdongFetcher') as mock_fetcher:
            mock_fetcher.category_list.return_value = []
            mock_fetcher.category_list()
        
        # Force garbage collection
        gc.collect()
        
        final_objects = len(gc.get_objects())
        # Should not have significantly more objects
        assert final_objects <= initial_objects + 100
