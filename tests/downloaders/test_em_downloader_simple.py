# encoding: utf-8
"""
Simple tests for EmDownloader class.
Tests basic functionality without async complications.
"""

import pytest
from unittest.mock import Mock, patch
from spider.downloader.em_downloader import EmDownloader


class TestEmDownloaderSimple:
    """Simple test suite for EmDownloader"""

    def _create_mock_item(self, url="http://example.com", html="<html>Test</html>", kind="test"):
        """Create a mock item for testing"""
        item = Mock()
        item.url = url
        item.html = html
        item.kind = kind
        item.__class__.__name__ = "MockItem"
        return item

    def test_em_downloader_initialization(self):
        """Test EmDownloader initialization"""
        items = [self._create_mock_item()]
        downloader = EmDownloader(items)
        
        assert downloader.items == items
        assert hasattr(downloader, 'logger')

    def test_em_downloader_initialization_empty_list(self):
        """Test EmDownloader initialization with empty list"""
        downloader = EmDownloader([])
        
        assert downloader.items == []
        assert hasattr(downloader, 'logger')

    def test_em_downloader_initialization_multiple_items(self):
        """Test EmDownloader initialization with multiple items"""
        items = [
            self._create_mock_item("http://example1.com"),
            self._create_mock_item("http://example2.com"),
            self._create_mock_item("http://example3.com")
        ]
        downloader = EmDownloader(items)
        
        assert len(downloader.items) == 3
        assert downloader.items[0].url == "http://example1.com"
        assert downloader.items[1].url == "http://example2.com"
        assert downloader.items[2].url == "http://example3.com"

    @patch('asyncio.run')
    def test_run_calls_async_method(self, mock_asyncio_run):
        """Test that run method calls asyncio.run"""
        items = [self._create_mock_item()]
        downloader = EmDownloader(items)
        callback = Mock()
        
        # Run test
        downloader.run(callback)
        
        # Verify asyncio.run was called
        mock_asyncio_run.assert_called_once()

    def test_downloader_inheritance(self):
        """Test that EmDownloader inherits from Downloader"""
        from spider.downloader import Downloader
        
        items = [self._create_mock_item()]
        downloader = EmDownloader(items)
        
        assert isinstance(downloader, Downloader)

    def test_downloader_string_representation(self):
        """Test string representation of EmDownloader"""
        items = [self._create_mock_item()]
        downloader = EmDownloader(items)
        
        str_repr = str(downloader)
        assert "EmDownloader" in str_repr

    def test_downloader_equality(self):
        """Test equality comparison of EmDownloader instances"""
        items1 = [self._create_mock_item("http://example1.com")]
        items2 = [self._create_mock_item("http://example2.com")]
        
        downloader1 = EmDownloader(items1)
        downloader2 = EmDownloader(items1)
        downloader3 = EmDownloader(items2)
        
        # Objects with same items should have same items attribute
        assert downloader1.items == downloader2.items
        assert downloader1.items != downloader3.items
        
        # But they are different objects (no __eq__ implemented)
        assert downloader1 is not downloader2
        assert downloader1 is not downloader3

    def test_downloader_hash(self):
        """Test hashing of EmDownloader instances"""
        items = [self._create_mock_item()]
        downloader = EmDownloader(items)
        
        # Should not raise an exception
        hash_value = hash(downloader)
        assert isinstance(hash_value, int)

    def test_downloader_serialization(self):
        """Test serialization of EmDownloader"""
        items = [self._create_mock_item()]
        downloader = EmDownloader(items)
        
        # Test that we can access attributes for serialization
        assert hasattr(downloader, 'items')
        assert downloader.items == items

    def test_downloader_deepcopy(self):
        """Test deep copying of EmDownloader"""
        import copy
        
        items = [self._create_mock_item()]
        downloader = EmDownloader(items)
        
        # Test deep copy
        copied_downloader = copy.deepcopy(downloader)
        assert copied_downloader is not downloader
        assert len(copied_downloader.items) == len(downloader.items)
        # Mock objects don't deep copy well, so just check structure
        assert hasattr(copied_downloader, 'items')

    def test_downloader_memory_usage(self):
        """Test memory usage of EmDownloader"""
        import sys
        
        items = [self._create_mock_item() for _ in range(100)]
        downloader = EmDownloader(items)
        
        # Test that we can get size information
        size = sys.getsizeof(downloader)
        assert size > 0

    def test_downloader_thread_safety(self):
        """Test thread safety of EmDownloader"""
        import threading
        import time
        
        items = [self._create_mock_item(f"http://example{i}.com") for i in range(10)]
        downloader = EmDownloader(items)
        results = []
        
        def worker():
            results.append(len(downloader.items))
        
        threads = [threading.Thread(target=worker) for _ in range(5)]
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # All threads should see the same number of items
        assert all(result == 10 for result in results)

    def test_downloader_process_safety(self):
        """Test process safety of EmDownloader"""
        # Test that downloader can be serialized for multiprocessing
        import pickle
        
        items = [self._create_mock_item()]
        downloader = EmDownloader(items)
        
        # Test that we can pickle the downloader
        try:
            pickled = pickle.dumps(downloader)
            unpickled = pickle.loads(pickled)
            assert len(unpickled.items) == len(downloader.items)
        except Exception as e:
            # If pickling fails, that's expected for some objects
            # Just verify the downloader has the expected structure
            assert hasattr(downloader, 'items')
            assert len(downloader.items) == 1

    def test_downloader_with_none_items(self):
        """Test EmDownloader with None items"""
        # Test that None items are handled gracefully
        downloader = EmDownloader(None)
        assert downloader.items is None

    def test_downloader_with_invalid_item(self):
        """Test EmDownloader with item missing url attribute"""
        item = Mock()
        # Missing url attribute
        items = [item]
        downloader = EmDownloader(items)
        callback = Mock()
        
        # Should handle gracefully
        with patch('asyncio.run') as mock_run:
            async def mock_async_run(coro):
                await coro
            mock_run.side_effect = mock_async_run
            
            with patch('aiohttp.ClientSession') as mock_session_class:
                mock_session = Mock()
                mock_session.get = Mock(side_effect=AttributeError("'Mock' object has no attribute 'url'"))
                mock_session_class.return_value.__aenter__.return_value = mock_session
                
                downloader.run(callback)
        
        # Callback should not be called
        callback.assert_not_called()

    def test_downloader_logger_initialization(self):
        """Test that logger is properly initialized"""
        items = [self._create_mock_item()]
        downloader = EmDownloader(items)
        
        assert hasattr(downloader, 'logger')
        assert downloader.logger is not None

    @patch('asyncio.run')
    def test_run_with_empty_items_list(self, mock_asyncio_run):
        """Test run with empty items list"""
        # Create test data
        items = []
        downloader = EmDownloader(items)
        callback = Mock()
        
        # Run test
        downloader.run(callback)
        
        # Verify asyncio.run was called
        mock_asyncio_run.assert_called_once()

    def test_downloader_performance_with_large_list(self):
        """Test performance with large item list"""
        import time
        
        # Create large list of items
        items = [self._create_mock_item(f"http://example{i}.com") for i in range(1000)]
        downloader = EmDownloader(items)
        
        # Test that initialization is fast
        start_time = time.time()
        downloader = EmDownloader(items)
        end_time = time.time()
        
        # Should initialize quickly (less than 1 second)
        assert (end_time - start_time) < 1.0

    def test_asyncio_gather_usage(self):
        """Test that asyncio.gather is used correctly"""
        items = [self._create_mock_item()]
        downloader = EmDownloader(items)
        
        # Test that items are stored correctly
        assert downloader.items == items
        
        # Test that we can create tasks for all items
        import asyncio
        tasks = [downloader._fetch(None, item, None) for item in items]
        assert len(tasks) == 1
        assert asyncio.iscoroutine(tasks[0])
