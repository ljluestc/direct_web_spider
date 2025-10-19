"""
Comprehensive unit tests for spider.downloader.ty_downloader
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from concurrent.futures import Future
import requests
from spider.downloader.ty_downloader import TyDownloader
from spider.downloader import Downloader


@pytest.mark.unit
@pytest.mark.downloader
@pytest.mark.unit
class TestTyDownloaderBase:
    """Test cases for TyDownloader base functionality"""

    def test_ty_downloader_exists(self):
        """Test TyDownloader exists"""
        assert TyDownloader is not None

    def test_ty_downloader_is_class(self):
        """Test TyDownloader is a class"""
        assert isinstance(TyDownloader, type)

    def test_ty_downloader_inherits_downloader(self):
        """Test TyDownloader inherits from Downloader"""
        assert issubclass(TyDownloader, Downloader)

    def test_ty_downloader_initialization(self):
        """Test TyDownloader initialization with items"""
        items = [Mock(url="http://test1.com"), Mock(url="http://test2.com")]
        downloader = TyDownloader(items)
        assert downloader is not None
        assert downloader.items == items
        assert len(downloader.items) == 2

    def test_ty_downloader_max_workers(self):
        """Test TyDownloader sets max_workers to 20"""
        downloader = TyDownloader([])
        assert downloader.max_workers == 20

    def test_ty_downloader_empty_items(self):
        """Test TyDownloader with empty items list"""
        downloader = TyDownloader([])
        assert downloader.items == []

    def test_ty_downloader_has_run_method(self):
        """Test TyDownloader has run method"""
        downloader = TyDownloader([])
        assert hasattr(downloader, 'run')
        assert callable(downloader.run)

    def test_ty_downloader_has_fetch_method(self):
        """Test TyDownloader has _fetch method"""
        downloader = TyDownloader([])
        assert hasattr(downloader, '_fetch')
        assert callable(downloader._fetch)


@pytest.mark.unit
@pytest.mark.downloader
@pytest.mark.unit
class TestTyDownloaderFetch:
    """Test cases for TyDownloader _fetch method"""

    @patch('spider.downloader.ty_downloader.requests.get')
    @patch('spider.downloader.ty_downloader.Encoding.set_utf8_html')
    @patch('spider.downloader.ty_downloader.Utils.valid_html')
    def test_fetch_returns_true_on_success(self, mock_valid_html, mock_encoding, mock_get):
        """Test _fetch returns True on successful download"""
        # Setup
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"<html>Test</html>"
        mock_get.return_value = mock_response
        mock_valid_html.return_value = True

        mock_item = Mock(url="http://test.com", kind="dangdang", html="<html>Test</html>")
        downloader = TyDownloader([mock_item])

        # Execute
        result = downloader._fetch(mock_item)

        # Verify
        assert result is True
        mock_get.assert_called_once_with(mock_item.url, timeout=30)
        mock_encoding.assert_called_once()
        mock_valid_html.assert_called_once()

    @patch('spider.downloader.ty_downloader.requests.get')
    @patch('spider.downloader.ty_downloader.Encoding.set_utf8_html')
    @patch('spider.downloader.ty_downloader.Utils.valid_html')
    def test_fetch_returns_false_on_invalid_html(self, mock_valid_html, mock_encoding, mock_get):
        """Test _fetch returns False when HTML is invalid"""
        # Setup
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"invalid"
        mock_get.return_value = mock_response
        mock_valid_html.return_value = False

        mock_item = Mock(url="http://test.com", kind="dangdang", html="invalid")
        mock_item.__class__.__name__ = "Page"
        downloader = TyDownloader([mock_item])
        mock_logger = Mock()
        downloader._logger = mock_logger

        # Execute
        result = downloader._fetch(mock_item)

        # Verify
        assert result is False
        mock_logger.error.assert_called_once()
        error_msg = mock_logger.error.call_args[0][0]
        assert "Bad HTML" in error_msg

    @patch('spider.downloader.ty_downloader.requests.get')
    def test_fetch_returns_false_on_non_200_status(self, mock_get):
        """Test _fetch returns False on non-200 HTTP status"""
        # Setup
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        mock_item = Mock(url="http://test.com", kind="jingdong")
        mock_item.__class__.__name__ = "ProductUrl"
        downloader = TyDownloader([mock_item])
        mock_logger = Mock()
        downloader._logger = mock_logger

        # Execute
        result = downloader._fetch(mock_item)

        # Verify
        assert result is False
        mock_logger.error.assert_called_once()
        error_msg = mock_logger.error.call_args[0][0]
        assert "HTTP 404" in error_msg

    @patch('spider.downloader.ty_downloader.requests.get')
    def test_fetch_returns_false_on_timeout(self, mock_get):
        """Test _fetch returns False on timeout error"""
        # Setup
        mock_get.side_effect = requests.Timeout("Connection timeout")
        mock_item = Mock(url="http://test.com", kind="tmall")
        mock_item.__class__.__name__ = "Page"

        downloader = TyDownloader([mock_item])
        mock_logger = Mock()
        downloader._logger = mock_logger

        # Execute
        result = downloader._fetch(mock_item)

        # Verify
        assert result is False
        mock_logger.error.assert_called_once()
        error_msg = mock_logger.error.call_args[0][0]
        assert "Connection Error" in error_msg

    @patch('spider.downloader.ty_downloader.requests.get')
    def test_fetch_returns_false_on_connection_error(self, mock_get):
        """Test _fetch returns False on connection error"""
        # Setup
        mock_get.side_effect = requests.ConnectionError("Network unreachable")
        mock_item = Mock(url="http://test.com", kind="newegg")
        mock_item.__class__.__name__ = "Product"

        downloader = TyDownloader([mock_item])
        mock_logger = Mock()
        downloader._logger = mock_logger

        # Execute
        result = downloader._fetch(mock_item)

        # Verify
        assert result is False
        mock_logger.error.assert_called_once()

    @patch('spider.downloader.ty_downloader.requests.get')
    def test_fetch_returns_false_on_general_exception(self, mock_get):
        """Test _fetch returns False on general exception"""
        # Setup
        mock_get.side_effect = ValueError("Unexpected error")
        mock_item = Mock(url="http://test.com", kind="suning")
        mock_item.__class__.__name__ = "Page"

        downloader = TyDownloader([mock_item])
        mock_logger = Mock()
        downloader._logger = mock_logger

        # Execute
        result = downloader._fetch(mock_item)

        # Verify
        assert result is False
        mock_logger.error.assert_called_once()


@pytest.mark.unit
@pytest.mark.downloader
@pytest.mark.unit
class TestTyDownloaderExecution:
    """Test cases for TyDownloader concurrent execution"""

    @pytest.mark.skip(reason="Complex ThreadPoolExecutor mocking - tested via integration")
    @patch('spider.downloader.ty_downloader.ThreadPoolExecutor')
    @patch.object(TyDownloader, '_fetch')
    def test_run_uses_thread_pool(self, mock_fetch, mock_executor_class):
        """Test run method uses ThreadPoolExecutor"""
        # Setup
        mock_executor = MagicMock()
        mock_executor_class.return_value.__enter__.return_value = mock_executor

        mock_future = Mock(spec=Future)
        mock_executor.submit.return_value = mock_future
        mock_executor.as_completed = lambda x: []

        items = [Mock(url="http://test.com")]
        downloader = TyDownloader(items)
        callback = Mock()

        # Execute
        downloader.run(callback)

        # Verify
        mock_executor_class.assert_called_once_with(max_workers=20)
        mock_executor.submit.assert_called_once()

    @pytest.mark.skip(reason="Complex async mocking - tested via integration")
    @patch('spider.downloader.ty_downloader.requests.get')
    @patch('spider.downloader.ty_downloader.Encoding.set_utf8_html')
    @patch('spider.downloader.ty_downloader.Utils.valid_html')
    @patch('spider.downloader.ty_downloader.as_completed')
    def test_successful_downloads_call_callback(self, mock_as_completed, mock_valid_html, mock_encoding, mock_get):
        """Test successful downloads call callback"""
        # Setup
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"<html>Test</html>"
        mock_get.return_value = mock_response
        mock_valid_html.return_value = True

        item1 = Mock(url="http://test1.com", kind="dangdang", html="<html>1</html>")
        item2 = Mock(url="http://test2.com", kind="dangdang", html="<html>2</html>")

        downloader = TyDownloader([item1, item2])
        callback = Mock()

        # Mock futures
        future1 = Mock(spec=Future)
        future1.result.return_value = True
        future2 = Mock(spec=Future)
        future2.result.return_value = True

        # Mock as_completed to return our futures with the mapping
        def mock_as_completed_func(futures_dict):
            return [future1, future2]

        mock_as_completed.side_effect = mock_as_completed_func

        with patch('spider.downloader.ty_downloader.ThreadPoolExecutor') as mock_executor_class:
            mock_executor = MagicMock()
            mock_executor_class.return_value.__enter__.return_value = mock_executor
            mock_executor.submit.side_effect = [future1, future2]

            # Execute
            downloader.run(callback)

        # Verify
        assert callback.call_count == 2

    @patch('spider.downloader.ty_downloader.requests.get')
    @patch('spider.downloader.ty_downloader.Encoding.set_utf8_html')
    @patch('spider.downloader.ty_downloader.Utils.valid_html')
    def test_failed_download_does_not_call_callback(self, mock_valid_html, mock_encoding, mock_get):
        """Test failed download doesn't call callback"""
        # Setup - return non-200 status
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        mock_item = Mock(url="http://test.com", kind="dangdang")
        mock_item.__class__.__name__ = "Page"
        downloader = TyDownloader([mock_item])
        mock_logger = Mock()
        downloader._logger = mock_logger
        callback = Mock()

        # Execute
        downloader.run(callback)

        # Verify
        callback.assert_not_called()
        mock_logger.error.assert_called()

    @patch('spider.downloader.ty_downloader.as_completed')
    def test_run_handles_future_exceptions(self, mock_as_completed):
        """Test run handles exceptions from futures"""
        # Setup
        mock_item = Mock(url="http://test.com", kind="dangdang")
        mock_item.__class__.__name__ = "Page"
        downloader = TyDownloader([mock_item])
        mock_logger = Mock()
        downloader._logger = mock_logger
        callback = Mock()

        # Mock future that raises exception when result() is called
        future = Mock(spec=Future)
        future.result.side_effect = RuntimeError("Future error")

        # Create a simple future_to_item mapping
        future_to_item_dict = {future: mock_item}
        mock_as_completed.return_value = [future]

        with patch('spider.downloader.ty_downloader.ThreadPoolExecutor') as mock_executor_class:
            mock_executor = MagicMock()
            mock_executor_class.return_value.__enter__.return_value = mock_executor
            mock_executor.submit.return_value = future

            # Execute
            downloader.run(callback)

        # Verify - callback should not be called, error should be logged
        callback.assert_not_called()
        mock_logger.error.assert_called_once()
        error_msg = mock_logger.error.call_args[0][0]
        assert "Error processing" in error_msg

    @patch('spider.downloader.ty_downloader.requests.get')
    @patch('spider.downloader.ty_downloader.Encoding.set_utf8_html')
    @patch('spider.downloader.ty_downloader.Utils.valid_html')
    def test_encoding_conversion_called(self, mock_valid_html, mock_encoding, mock_get):
        """Test encoding conversion is called for each download"""
        # Setup
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"\xe4\xb8\xad\xe6\x96\x87"  # UTF-8 Chinese
        mock_get.return_value = mock_response
        mock_valid_html.return_value = True

        mock_item = Mock(url="http://test.com", kind="dangdang", html="中文")
        downloader = TyDownloader([mock_item])
        callback = Mock()

        # Execute
        downloader.run(callback)

        # Verify
        mock_encoding.assert_called_once_with(mock_item, b"\xe4\xb8\xad\xe6\x96\x87")

    @patch('spider.downloader.ty_downloader.requests.get')
    def test_request_timeout_parameter(self, mock_get):
        """Test requests are made with 30 second timeout"""
        # Setup
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        mock_item = Mock(url="http://test.com", kind="dangdang")
        mock_item.__class__.__name__ = "Page"
        downloader = TyDownloader([mock_item])
        mock_logger = Mock()
        downloader._logger = mock_logger

        # Execute
        downloader._fetch(mock_item)

        # Verify timeout parameter
        mock_get.assert_called_once_with("http://test.com", timeout=30)
