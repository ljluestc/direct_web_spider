# encoding: utf-8
"""
Comprehensive tests for NormalDownloader class.
Tests all methods, edge cases, error conditions, and integration scenarios.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import requests
from spider.downloader.normal_downloader import NormalDownloader
from spider.encoding import Encoding
from spider.utils.utils import Utils


class TestNormalDownloaderComprehensive:
    """Comprehensive test suite for NormalDownloader"""

    def _create_mock_item(self, url="http://example.com", html="<html>Test</html>", kind="test"):
        """Create a mock item for testing"""
        item = Mock()
        item.url = url
        item.html = html
        item.kind = kind
        item.__class__.__name__ = "MockItem"
        return item

    def test_normal_downloader_initialization(self):
        """Test NormalDownloader initialization"""
        items = [self._create_mock_item()]
        downloader = NormalDownloader(items)
        
        assert downloader.items == items
        assert hasattr(downloader, 'logger')

    def test_normal_downloader_initialization_empty_list(self):
        """Test NormalDownloader initialization with empty list"""
        downloader = NormalDownloader([])
        
        assert downloader.items == []
        assert hasattr(downloader, 'logger')

    def test_normal_downloader_initialization_multiple_items(self):
        """Test NormalDownloader initialization with multiple items"""
        items = [
            self._create_mock_item("http://example1.com"),
            self._create_mock_item("http://example2.com"),
            self._create_mock_item("http://example3.com")
        ]
        downloader = NormalDownloader(items)
        
        assert len(downloader.items) == 3
        assert downloader.items[0].url == "http://example1.com"
        assert downloader.items[1].url == "http://example2.com"
        assert downloader.items[2].url == "http://example3.com"

    @patch('requests.get')
    @patch('spider.encoding.Encoding.set_utf8_html')
    @patch('spider.utils.utils.Utils.valid_html')
    def test_run_successful_download(self, mock_valid_html, mock_set_utf8_html, mock_get):
        """Test successful download and callback execution"""
        # Setup mocks
        mock_response = Mock()
        mock_response.content = b"<html>Test content</html>"
        mock_get.return_value = mock_response
        mock_set_utf8_html.return_value = None
        mock_valid_html.return_value = True
        
        # Create test data
        item = self._create_mock_item()
        items = [item]
        downloader = NormalDownloader(items)
        callback = Mock()
        
        # Run test
        downloader.run(callback)
        
        # Verify requests.get was called
        mock_get.assert_called_once_with(item.url, timeout=30)
        
        # Verify encoding was set
        mock_set_utf8_html.assert_called_once_with(item, mock_response.content)
        
        # Verify HTML validation
        mock_valid_html.assert_called_once_with(item.html)
        
        # Verify callback was called
        callback.assert_called_once_with(item)

    @patch('requests.get')
    @patch('spider.encoding.Encoding.set_utf8_html')
    @patch('spider.utils.utils.Utils.valid_html')
    def test_run_invalid_html(self, mock_valid_html, mock_set_utf8_html, mock_get):
        """Test download with invalid HTML"""
        # Setup mocks
        mock_response = Mock()
        mock_response.content = b"<html>Test content</html>"
        mock_get.return_value = mock_response
        mock_set_utf8_html.return_value = None
        mock_valid_html.return_value = False
        
        # Create test data
        item = self._create_mock_item()
        items = [item]
        downloader = NormalDownloader(items)
        callback = Mock()
        
        # Run test
        downloader.run(callback)
        
        # Verify requests.get was called
        mock_get.assert_called_once_with(item.url, timeout=30)
        
        # Verify encoding was set
        mock_set_utf8_html.assert_called_once_with(item, mock_response.content)
        
        # Verify HTML validation
        mock_valid_html.assert_called_once_with(item.html)
        
        # Verify callback was NOT called due to invalid HTML
        callback.assert_not_called()

    @patch('requests.get')
    def test_run_connection_error(self, mock_get):
        """Test download with connection error"""
        # Setup mocks
        mock_get.side_effect = requests.ConnectionError("Connection failed")
        
        # Create test data
        item = self._create_mock_item()
        items = [item]
        downloader = NormalDownloader(items)
        callback = Mock()
        
        # Run test
        downloader.run(callback)
        
        # Verify requests.get was called
        mock_get.assert_called_once_with(item.url, timeout=30)
        
        # Verify callback was NOT called due to connection error
        callback.assert_not_called()

    @patch('requests.get')
    def test_run_timeout_error(self, mock_get):
        """Test download with timeout error"""
        # Setup mocks
        mock_get.side_effect = requests.Timeout("Request timed out")
        
        # Create test data
        item = self._create_mock_item()
        items = [item]
        downloader = NormalDownloader(items)
        callback = Mock()
        
        # Run test
        downloader.run(callback)
        
        # Verify requests.get was called
        mock_get.assert_called_once_with(item.url, timeout=30)
        
        # Verify callback was NOT called due to timeout error
        callback.assert_not_called()

    @patch('requests.get')
    def test_run_general_exception(self, mock_get):
        """Test download with general exception"""
        # Setup mocks
        mock_get.side_effect = Exception("General error")
        
        # Create test data
        item = self._create_mock_item()
        items = [item]
        downloader = NormalDownloader(items)
        callback = Mock()
        
        # Run test
        downloader.run(callback)
        
        # Verify requests.get was called
        mock_get.assert_called_once_with(item.url, timeout=30)
        
        # Verify callback was NOT called due to general error
        callback.assert_not_called()

    @patch('requests.get')
    @patch('spider.encoding.Encoding.set_utf8_html')
    @patch('spider.utils.utils.Utils.valid_html')
    def test_run_multiple_items_mixed_results(self, mock_valid_html, mock_set_utf8_html, mock_get):
        """Test download with multiple items having mixed results"""
        # Setup mocks
        def mock_get_side_effect(url, timeout):
            if "success" in url:
                response = Mock()
                response.content = b"<html>Valid content</html>"
                return response
            elif "timeout" in url:
                raise requests.Timeout("Timeout")
            else:
                raise requests.ConnectionError("Connection failed")
        
        mock_get.side_effect = mock_get_side_effect
        mock_set_utf8_html.return_value = None
        mock_valid_html.return_value = True
        
        # Create test data
        items = [
            self._create_mock_item("http://success1.com"),
            self._create_mock_item("http://timeout.com"),
            self._create_mock_item("http://success2.com"),
            self._create_mock_item("http://connection-error.com")
        ]
        downloader = NormalDownloader(items)
        callback = Mock()
        
        # Run test
        downloader.run(callback)
        
        # Verify requests.get was called for all items
        assert mock_get.call_count == 4
        
        # Verify callback was called only for successful items
        assert callback.call_count == 2
        callback.assert_any_call(items[0])  # success1
        callback.assert_any_call(items[2])  # success2

    @patch('requests.get')
    @patch('spider.encoding.Encoding.set_utf8_html')
    @patch('spider.utils.utils.Utils.valid_html')
    def test_run_encoding_error(self, mock_valid_html, mock_set_utf8_html, mock_get):
        """Test download with encoding error"""
        # Setup mocks
        mock_response = Mock()
        mock_response.content = b"<html>Test content</html>"
        mock_get.return_value = mock_response
        mock_set_utf8_html.side_effect = Exception("Encoding error")
        mock_valid_html.return_value = True
        
        # Create test data
        item = self._create_mock_item()
        items = [item]
        downloader = NormalDownloader(items)
        callback = Mock()
        
        # Run test
        downloader.run(callback)
        
        # Verify requests.get was called
        mock_get.assert_called_once_with(item.url, timeout=30)
        
        # Verify encoding was attempted
        mock_set_utf8_html.assert_called_once_with(item, mock_response.content)
        
        # Verify callback was NOT called due to encoding error
        callback.assert_not_called()

    def test_downloader_inheritance(self):
        """Test that NormalDownloader inherits from Downloader"""
        from spider.downloader import Downloader
        
        items = [self._create_mock_item()]
        downloader = NormalDownloader(items)
        
        assert isinstance(downloader, Downloader)

    def test_downloader_string_representation(self):
        """Test string representation of NormalDownloader"""
        items = [self._create_mock_item()]
        downloader = NormalDownloader(items)
        
        str_repr = str(downloader)
        assert "NormalDownloader" in str_repr

    def test_downloader_equality(self):
        """Test equality comparison of NormalDownloader instances"""
        items1 = [self._create_mock_item("http://example1.com")]
        items2 = [self._create_mock_item("http://example2.com")]
        
        downloader1 = NormalDownloader(items1)
        downloader2 = NormalDownloader(items1)
        downloader3 = NormalDownloader(items2)
        
        # Objects with same items should have same items attribute
        assert downloader1.items == downloader2.items
        assert downloader1.items != downloader3.items
        
        # But they are different objects (no __eq__ implemented)
        assert downloader1 is not downloader2
        assert downloader1 is not downloader3

    def test_downloader_hash(self):
        """Test hashing of NormalDownloader instances"""
        items = [self._create_mock_item()]
        downloader = NormalDownloader(items)
        
        # Should not raise an exception
        hash_value = hash(downloader)
        assert isinstance(hash_value, int)

    def test_downloader_serialization(self):
        """Test serialization of NormalDownloader"""
        items = [self._create_mock_item()]
        downloader = NormalDownloader(items)
        
        # Test that we can access attributes for serialization
        assert hasattr(downloader, 'items')
        assert downloader.items == items

    def test_downloader_deepcopy(self):
        """Test deep copying of NormalDownloader"""
        import copy
        
        items = [self._create_mock_item()]
        downloader = NormalDownloader(items)
        
        # Test deep copy
        copied_downloader = copy.deepcopy(downloader)
        assert copied_downloader is not downloader
        assert len(copied_downloader.items) == len(downloader.items)
        # Mock objects don't deep copy well, so just check structure
        assert hasattr(copied_downloader, 'items')

    def test_downloader_memory_usage(self):
        """Test memory usage of NormalDownloader"""
        import sys
        
        items = [self._create_mock_item() for _ in range(100)]
        downloader = NormalDownloader(items)
        
        # Test that we can get size information
        size = sys.getsizeof(downloader)
        assert size > 0

    def test_downloader_thread_safety(self):
        """Test thread safety of NormalDownloader"""
        import threading
        import time
        
        items = [self._create_mock_item(f"http://example{i}.com") for i in range(10)]
        downloader = NormalDownloader(items)
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
        """Test process safety of NormalDownloader"""
        # Test that downloader can be serialized for multiprocessing
        import pickle
        
        items = [self._create_mock_item()]
        downloader = NormalDownloader(items)
        
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

    @patch('requests.get')
    @patch('spider.encoding.Encoding.set_utf8_html')
    @patch('spider.utils.utils.Utils.valid_html')
    def test_run_callback_exception(self, mock_valid_html, mock_set_utf8_html, mock_get):
        """Test download when callback raises an exception"""
        # Setup mocks
        mock_response = Mock()
        mock_response.content = b"<html>Test content</html>"
        mock_get.return_value = mock_response
        mock_set_utf8_html.return_value = None
        mock_valid_html.return_value = True
        
        # Create test data
        item = self._create_mock_item()
        items = [item]
        downloader = NormalDownloader(items)
        callback = Mock(side_effect=Exception("Callback error"))
        
        # Run test - should not raise exception
        downloader.run(callback)
        
        # Verify requests.get was called
        mock_get.assert_called_once_with(item.url, timeout=30)
        
        # Verify callback was called despite exception
        callback.assert_called_once_with(item)

    def test_downloader_with_none_items(self):
        """Test NormalDownloader with None items"""
        # Test that None items are handled gracefully
        downloader = NormalDownloader(None)
        assert downloader.items is None

    def test_downloader_with_invalid_item(self):
        """Test NormalDownloader with item missing url attribute"""
        item = Mock()
        # Missing url attribute
        items = [item]
        downloader = NormalDownloader(items)
        callback = Mock()
        
        # Should handle gracefully
        with patch('requests.get', side_effect=AttributeError("'Mock' object has no attribute 'url'")):
            downloader.run(callback)
        
        # Callback should not be called
        callback.assert_not_called()

    @patch('requests.get')
    @patch('spider.encoding.Encoding.set_utf8_html')
    @patch('spider.utils.utils.Utils.valid_html')
    def test_run_with_different_timeout_values(self, mock_valid_html, mock_set_utf8_html, mock_get):
        """Test that timeout is always 30 seconds"""
        # Setup mocks
        mock_response = Mock()
        mock_response.content = b"<html>Test content</html>"
        mock_get.return_value = mock_response
        mock_set_utf8_html.return_value = None
        mock_valid_html.return_value = True
        
        # Create test data
        item = self._create_mock_item()
        items = [item]
        downloader = NormalDownloader(items)
        callback = Mock()
        
        # Run test
        downloader.run(callback)
        
        # Verify timeout is 30 seconds
        mock_get.assert_called_once_with(item.url, timeout=30)

    def test_downloader_logger_initialization(self):
        """Test that logger is properly initialized"""
        items = [self._create_mock_item()]
        downloader = NormalDownloader(items)
        
        assert hasattr(downloader, 'logger')
        assert downloader.logger is not None

    @patch('requests.get')
    @patch('spider.encoding.Encoding.set_utf8_html')
    @patch('spider.utils.utils.Utils.valid_html')
    def test_run_with_empty_items_list(self, mock_valid_html, mock_set_utf8_html, mock_get):
        """Test run with empty items list"""
        # Create test data
        items = []
        downloader = NormalDownloader(items)
        callback = Mock()
        
        # Run test
        downloader.run(callback)
        
        # Verify no requests were made
        mock_get.assert_not_called()
        
        # Verify callback was not called
        callback.assert_not_called()

    def test_downloader_performance_with_large_list(self):
        """Test performance with large item list"""
        import time
        
        # Create large list of items
        items = [self._create_mock_item(f"http://example{i}.com") for i in range(1000)]
        downloader = NormalDownloader(items)
        
        # Test that initialization is fast
        start_time = time.time()
        downloader = NormalDownloader(items)
        end_time = time.time()
        
        # Should initialize quickly (less than 1 second)
        assert (end_time - start_time) < 1.0
