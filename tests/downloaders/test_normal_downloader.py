"""
Comprehensive unit tests for spider.downloader.normal_downloader
"""
import pytest
from unittest.mock import Mock, patch, MagicMock, call
import requests
from spider.downloader.normal_downloader import NormalDownloader
from spider.downloader import Downloader


@pytest.mark.unit
@pytest.mark.downloader
@pytest.mark.unit
class TestNormalDownloaderBase:
    """Test cases for NormalDownloader base functionality"""

    def test_normal_downloader_exists(self):
        """Test NormalDownloader exists"""
        assert NormalDownloader is not None

    def test_normal_downloader_is_class(self):
        """Test NormalDownloader is a class"""
        assert isinstance(NormalDownloader, type)

    def test_normal_downloader_inherits_downloader(self):
        """Test NormalDownloader inherits from Downloader"""
        assert issubclass(NormalDownloader, Downloader)

    def test_normal_downloader_initialization(self):
        """Test NormalDownloader initialization with items"""
        items = [Mock(url="http://test1.com"), Mock(url="http://test2.com")]
        downloader = NormalDownloader(items)
        assert downloader is not None
        assert downloader.items == items
        assert len(downloader.items) == 2

    def test_normal_downloader_empty_items(self):
        """Test NormalDownloader with empty items list"""
        downloader = NormalDownloader([])
        assert downloader.items == []

    def test_normal_downloader_has_run_method(self):
        """Test NormalDownloader has run method"""
        downloader = NormalDownloader([])
        assert hasattr(downloader, 'run')
        assert callable(downloader.run)


@pytest.mark.unit
@pytest.mark.downloader
@pytest.mark.unit
class TestNormalDownloaderExecution:
    """Test cases for NormalDownloader execution"""

    @patch('spider.downloader.normal_downloader.requests.get')
    @patch('spider.downloader.normal_downloader.Encoding.set_utf8_html')
    @patch('spider.downloader.normal_downloader.Utils.valid_html')
    def test_successful_download_calls_callback(self, mock_valid_html, mock_encoding, mock_get):
        """Test successful download calls callback"""
        # Setup
        mock_response = Mock()
        mock_response.content = b"<html>Test</html>"
        mock_get.return_value = mock_response
        mock_valid_html.return_value = True

        mock_item = Mock(url="http://test.com", kind="dangdang")
        mock_item.html = "<html>Test</html>"
        downloader = NormalDownloader([mock_item])

        callback = Mock()

        # Execute
        downloader.run(callback)

        # Verify
        mock_get.assert_called_once_with(mock_item.url, timeout=30)
        mock_encoding.assert_called_once_with(mock_item, b"<html>Test</html>")
        mock_valid_html.assert_called_once()
        callback.assert_called_once_with(mock_item)

    @patch('spider.downloader.normal_downloader.requests.get')
    @patch('spider.downloader.normal_downloader.Encoding.set_utf8_html')
    @patch('spider.downloader.normal_downloader.Utils.valid_html')
    def test_multiple_items_sequential_processing(self, mock_valid_html, mock_encoding, mock_get):
        """Test multiple items are processed sequentially"""
        # Setup
        mock_response = Mock()
        mock_response.content = b"<html>Test</html>"
        mock_get.return_value = mock_response
        mock_valid_html.return_value = True

        item1 = Mock(url="http://test1.com", kind="dangdang", html="<html>1</html>")
        item2 = Mock(url="http://test2.com", kind="dangdang", html="<html>2</html>")
        item3 = Mock(url="http://test3.com", kind="dangdang", html="<html>3</html>")

        downloader = NormalDownloader([item1, item2, item3])
        callback = Mock()

        # Execute
        downloader.run(callback)

        # Verify
        assert mock_get.call_count == 3
        assert callback.call_count == 3
        callback.assert_has_calls([call(item1), call(item2), call(item3)])

    @patch('spider.downloader.normal_downloader.requests.get')
    def test_timeout_error_handling(self, mock_get):
        """Test timeout error is handled and logged"""
        # Setup
        mock_get.side_effect = requests.Timeout("Connection timeout")
        mock_item = Mock(url="http://test.com", kind="dangdang")
        mock_item.__class__.__name__ = "Page"

        downloader = NormalDownloader([mock_item])
        mock_logger = Mock()
        downloader._logger = mock_logger  # Set internal logger directly
        callback = Mock()

        # Execute
        downloader.run(callback)

        # Verify
        callback.assert_not_called()
        mock_logger.error.assert_called_once()
        error_msg = mock_logger.error.call_args[0][0]
        assert "Page" in error_msg
        assert "dangdang" in error_msg
        assert "http://test.com" in error_msg
        assert "Connection Error" in error_msg

    @patch('spider.downloader.normal_downloader.requests.get')
    def test_connection_error_handling(self, mock_get):
        """Test connection error is handled and logged"""
        # Setup
        mock_get.side_effect = requests.ConnectionError("Network unreachable")
        mock_item = Mock(url="http://test.com", kind="jingdong")
        mock_item.__class__.__name__ = "ProductUrl"

        downloader = NormalDownloader([mock_item])
        mock_logger = Mock()
        downloader._logger = mock_logger
        callback = Mock()

        # Execute
        downloader.run(callback)

        # Verify
        callback.assert_not_called()
        mock_logger.error.assert_called_once()
        error_msg = mock_logger.error.call_args[0][0]
        assert "ProductUrl" in error_msg
        assert "jingdong" in error_msg
        assert "Connection Error" in error_msg

    @patch('spider.downloader.normal_downloader.requests.get')
    @patch('spider.downloader.normal_downloader.Encoding.set_utf8_html')
    @patch('spider.downloader.normal_downloader.Utils.valid_html')
    def test_invalid_html_handling(self, mock_valid_html, mock_encoding, mock_get):
        """Test invalid HTML is detected and logged"""
        # Setup
        mock_response = Mock()
        mock_response.content = b"invalid"
        mock_get.return_value = mock_response
        mock_valid_html.return_value = False  # Invalid HTML

        mock_item = Mock(url="http://test.com", kind="tmall", html="invalid")
        mock_item.__class__.__name__ = "Page"

        downloader = NormalDownloader([mock_item])
        mock_logger = Mock()
        downloader._logger = mock_logger
        callback = Mock()

        # Execute
        downloader.run(callback)

        # Verify
        callback.assert_not_called()
        mock_logger.error.assert_called_once()
        error_msg = mock_logger.error.call_args[0][0]
        assert "Page" in error_msg
        assert "tmall" in error_msg
        assert "Bad HTML" in error_msg

    @patch('spider.downloader.normal_downloader.requests.get')
    def test_general_exception_handling(self, mock_get):
        """Test general exception is handled and logged"""
        # Setup
        mock_get.side_effect = ValueError("Unexpected error")
        mock_item = Mock(url="http://test.com", kind="newegg")
        mock_item.__class__.__name__ = "Product"

        downloader = NormalDownloader([mock_item])
        mock_logger = Mock()
        downloader._logger = mock_logger
        callback = Mock()

        # Execute
        downloader.run(callback)

        # Verify
        callback.assert_not_called()
        mock_logger.error.assert_called_once()
        error_msg = mock_logger.error.call_args[0][0]
        assert "Product" in error_msg
        assert "newegg" in error_msg
        assert "Error:" in error_msg

    @patch('spider.downloader.normal_downloader.requests.get')
    @patch('spider.downloader.normal_downloader.Encoding.set_utf8_html')
    @patch('spider.downloader.normal_downloader.Utils.valid_html')
    def test_encoding_conversion_called(self, mock_valid_html, mock_encoding, mock_get):
        """Test encoding conversion is called for each download"""
        # Setup
        mock_response = Mock()
        mock_response.content = b"\xe4\xb8\xad\xe6\x96\x87"  # UTF-8 Chinese
        mock_get.return_value = mock_response
        mock_valid_html.return_value = True

        mock_item = Mock(url="http://test.com", kind="dangdang")
        downloader = NormalDownloader([mock_item])
        callback = Mock()

        # Execute
        downloader.run(callback)

        # Verify
        mock_encoding.assert_called_once_with(mock_item, b"\xe4\xb8\xad\xe6\x96\x87")

    @patch('spider.downloader.normal_downloader.requests.get')
    @patch('spider.downloader.normal_downloader.Encoding.set_utf8_html')
    @patch('spider.downloader.normal_downloader.Utils.valid_html')
    def test_one_failure_does_not_stop_others(self, mock_valid_html, mock_encoding, mock_get):
        """Test one item failure doesn't stop processing other items"""
        # Setup - first fails, second succeeds
        mock_get.side_effect = [
            requests.Timeout("Timeout"),
            Mock(content=b"<html>Success</html>")
        ]
        mock_valid_html.return_value = True

        item1 = Mock(url="http://fail.com", kind="dangdang")
        item1.__class__.__name__ = "Page"
        item2 = Mock(url="http://success.com", kind="dangdang", html="<html>Success</html>")

        downloader = NormalDownloader([item1, item2])
        mock_logger = Mock()
        downloader._logger = mock_logger
        callback = Mock()

        # Execute
        downloader.run(callback)

        # Verify
        assert mock_get.call_count == 2
        callback.assert_called_once_with(item2)
        mock_logger.error.assert_called_once()

    @patch('spider.downloader.normal_downloader.requests.get')
    @patch('spider.downloader.normal_downloader.Encoding.set_utf8_html')
    @patch('spider.downloader.normal_downloader.Utils.valid_html')
    def test_request_timeout_parameter(self, mock_valid_html, mock_encoding, mock_get):
        """Test requests are made with 30 second timeout"""
        # Setup
        mock_response = Mock()
        mock_response.content = b"<html>Test</html>"
        mock_get.return_value = mock_response
        mock_valid_html.return_value = True

        mock_item = Mock(url="http://test.com", kind="dangdang", html="<html>Test</html>")
        downloader = NormalDownloader([mock_item])
        callback = Mock()

        # Execute
        downloader.run(callback)

        # Verify timeout parameter
        mock_get.assert_called_once_with("http://test.com", timeout=30)
