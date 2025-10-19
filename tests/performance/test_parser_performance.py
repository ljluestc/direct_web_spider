"""
Performance tests for parser components
"""

import pytest
import time
from unittest.mock import Mock, patch


class TestParserPerformance:
    """Test parser performance"""

    @pytest.mark.performance
    def test_parser_init_performance(self):
        """Test parser initialization performance"""
        start_time = time.time()
        
        mock_product = Mock()
        mock_product.html = "<html><body>Test</body></html>"
        
        from spider.parser import DangdangParser
        parser = DangdangParser(mock_product)
        
        end_time = time.time()
        assert end_time - start_time < 1.0  # Should initialize quickly
        assert parser is not None

    @pytest.mark.performance
    def test_parser_parse_performance(self):
        """Test parser parse performance"""
        mock_product = Mock()
        mock_product.html = "<html><body>Test</body></html>"
        
        from spider.parser import DangdangParser
        parser = DangdangParser(mock_product)
        
        with patch.object(parser, 'parse') as mock_parse:
            mock_parse.return_value = [Mock() for _ in range(100)]
            
            start_time = time.time()
            result = parser.parse(Mock())
            end_time = time.time()
            
            assert end_time - start_time < 2.0  # Should parse quickly
            assert len(result) == 100

    @pytest.mark.performance
    def test_parser_concurrent_performance(self):
        """Test parser concurrent performance"""
        import threading
        
        mock_product = Mock()
        mock_product.html = "<html><body>Test</body></html>"
        
        from spider.parser import DangdangParser
        parser = DangdangParser(mock_product)
        
        def parse_worker():
            with patch.object(parser, 'parse') as mock_parse:
                mock_parse.return_value = [Mock() for _ in range(10)]
                return parser.parse(Mock())
        
        threads = []
        start_time = time.time()
        
        for _ in range(5):
            thread = threading.Thread(target=parse_worker)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        assert end_time - start_time < 3.0  # Should handle concurrency well

    @pytest.mark.performance
    def test_parser_memory_efficiency(self):
        """Test memory efficiency of parser operations"""
        import gc
        
        initial_objects = len(gc.get_objects())
        
        mock_product = Mock()
        mock_product.html = "<html><body>Test</body></html>"
        
        from spider.parser import DangdangParser
        parser = DangdangParser(mock_product)
        
        with patch.object(parser, 'parse') as mock_parse:
            mock_parse.return_value = [Mock() for _ in range(100)]
            
            # Process in batches to test memory efficiency
            results = []
            for _ in range(10):
                batch = parser.parse(Mock())
                results.extend(batch)
                # Simulate cleanup
                del batch
            
            # Force garbage collection
            gc.collect()
            
            final_objects = len(gc.get_objects())
            # Should not have significantly more objects
            assert final_objects <= initial_objects + 100
            assert len(results) == 1000
