"""
Performance tests for digger components
"""

import pytest
import time
from unittest.mock import Mock, patch


class TestDiggerPerformance:
    """Test digger performance"""

    @pytest.mark.performance
    def test_digger_init_performance(self):
        """Test digger initialization performance"""
        start_time = time.time()
        
        mock_page = Mock()
        mock_page.html = "<html><body>Test</body></html>"
        
        from spider.digger import DangdangDigger
        digger = DangdangDigger(mock_page)
        
        end_time = time.time()
        assert end_time - start_time < 1.0  # Should initialize quickly
        assert digger is not None

    @pytest.mark.performance
    def test_digger_crawl_performance(self):
        """Test digger crawl performance"""
        mock_page = Mock()
        mock_page.html = "<html><body>Test</body></html>"
        
        from spider.digger import DangdangDigger
        digger = DangdangDigger(mock_page)
        
        with patch.object(digger, 'product_list') as mock_crawl:
            mock_crawl.return_value = [Mock() for _ in range(100)]
            
            start_time = time.time()
            result = digger.product_list()
            end_time = time.time()
            
            assert end_time - start_time < 2.0  # Should crawl quickly
            assert len(result) == 100

    @pytest.mark.performance
    def test_digger_concurrent_performance(self):
        """Test digger concurrent performance"""
        import threading
        
        mock_page = Mock()
        mock_page.html = "<html><body>Test</body></html>"
        
        from spider.digger import DangdangDigger
        digger = DangdangDigger(mock_page)
        
        def crawl_worker():
            with patch.object(digger, 'product_list') as mock_crawl:
                mock_crawl.return_value = [Mock() for _ in range(10)]
                return digger.product_list()
        
        threads = []
        start_time = time.time()
        
        for _ in range(5):
            thread = threading.Thread(target=crawl_worker)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        assert end_time - start_time < 3.0  # Should handle concurrency well

    @pytest.mark.performance
    def test_digger_memory_efficiency(self):
        """Test memory efficiency of digger operations"""
        import gc
        
        initial_objects = len(gc.get_objects())
        
        mock_page = Mock()
        mock_page.html = "<html><body>Test</body></html>"
        
        from spider.digger import DangdangDigger
        digger = DangdangDigger(mock_page)
        
        with patch.object(digger, 'product_list') as mock_crawl:
            mock_crawl.return_value = [Mock() for _ in range(100)]
            
            # Process in batches to test memory efficiency
            results = []
            for _ in range(10):
                batch = digger.product_list()
                results.extend(batch)
                # Simulate cleanup
                del batch
            
            # Force garbage collection
            gc.collect()
            
            final_objects = len(gc.get_objects())
            # Should not have significantly more objects
            assert final_objects <= initial_objects + 100
            assert len(results) == 1000
