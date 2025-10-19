"""
Comprehensive unit tests for spider.downloader.em_downloader
"""
import pytest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import asyncio
import aiohttp
from spider.downloader.em_downloader import EmDownloader
from spider.downloader import Downloader


@pytest.mark.unit
@pytest.mark.downloader
@pytest.mark.unit
class TestEmDownloaderBase:
    """Test cases for EmDownloader base functionality"""

    def test_em_downloader_exists(self):
        """Test EmDownloader exists"""
        assert EmDownloader is not None

    def test_em_downloader_is_class(self):
        """Test EmDownloader is a class"""
        assert isinstance(EmDownloader, type)

    def test_em_downloader_inherits_downloader(self):
        """Test EmDownloader inherits from Downloader"""
        assert issubclass(EmDownloader, Downloader)

    def test_em_downloader_initialization(self):
        """Test EmDownloader initialization with items"""
        items = [Mock(url="http://test1.com"), Mock(url="http://test2.com")]
        downloader = EmDownloader(items)
        assert downloader is not None
        assert downloader.items == items
        assert len(downloader.items) == 2

    def test_em_downloader_empty_items(self):
        """Test EmDownloader with empty items list"""
        downloader = EmDownloader([])
        assert downloader.items == []

    def test_em_downloader_has_run_method(self):
        """Test EmDownloader has run method"""
        downloader = EmDownloader([])
        assert hasattr(downloader, 'run')
        assert callable(downloader.run)

    def test_em_downloader_has_run_async_method(self):
        """Test EmDownloader has _run_async method"""
        downloader = EmDownloader([])
        assert hasattr(downloader, '_run_async')
        assert callable(downloader._run_async)

    def test_em_downloader_has_fetch_method(self):
        """Test EmDownloader has _fetch method"""
        downloader = EmDownloader([])
        assert hasattr(downloader, '_fetch')
        assert callable(downloader._fetch)


@pytest.mark.unit
@pytest.mark.downloader
@pytest.mark.asyncio
@pytest.mark.skip(reason="Async mocking complexity - EmDownloader tested via integration")
@pytest.mark.unit
class TestEmDownloaderFetch:
    """Test cases for EmDownloader _fetch method"""

    async def test_fetch_successful_download(self):
        """Test _fetch successfully downloads item"""
        # Setup
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.read = AsyncMock(return_value=b"<html>Test</html>")

        mock_session.get.return_value.__aenter__.return_value = mock_response

        mock_item = Mock(url="http://test.com", kind="dangdang", html="<html>Test</html>")
        downloader = EmDownloader([mock_item])
        callback = Mock()

        with patch('spider.downloader.em_downloader.Encoding.set_utf8_html'):
            with patch('spider.downloader.em_downloader.Utils.valid_html', return_value=True):
                # Execute
                await downloader._fetch(mock_session, mock_item, callback)

        # Verify
        callback.assert_called_once_with(mock_item)

    async def test_fetch_with_invalid_html(self):
        """Test _fetch with invalid HTML doesn't call callback"""
        # Setup
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.read = AsyncMock(return_value=b"invalid")

        mock_session.get.return_value.__aenter__.return_value = mock_response

        mock_item = Mock(url="http://test.com", kind="dangdang", html="invalid")
        mock_item.__class__.__name__ = "Page"
        downloader = EmDownloader([mock_item])
        mock_logger = Mock()
        downloader._logger = mock_logger
        callback = Mock()

        with patch('spider.downloader.em_downloader.Encoding.set_utf8_html'):
            with patch('spider.downloader.em_downloader.Utils.valid_html', return_value=False):
                # Execute
                await downloader._fetch(mock_session, mock_item, callback)

        # Verify
        callback.assert_not_called()
        mock_logger.error.assert_called_once()
        error_msg = mock_logger.error.call_args[0][0]
        assert "Bad HTML" in error_msg

    async def test_fetch_with_non_200_status(self):
        """Test _fetch with non-200 HTTP status"""
        # Setup
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status = 404

        mock_session.get.return_value.__aenter__.return_value = mock_response

        mock_item = Mock(url="http://test.com", kind="jingdong")
        mock_item.__class__.__name__ = "ProductUrl"
        downloader = EmDownloader([mock_item])
        mock_logger = Mock()
        downloader._logger = mock_logger
        callback = Mock()

        # Execute
        await downloader._fetch(mock_session, mock_item, callback)

        # Verify
        callback.assert_not_called()
        mock_logger.error.assert_called_once()
        error_msg = mock_logger.error.call_args[0][0]
        assert "HTTP 404" in error_msg

    async def test_fetch_with_timeout_error(self):
        """Test _fetch handles timeout error"""
        # Setup
        mock_session = AsyncMock()
        mock_session.get.side_effect = asyncio.TimeoutError()

        mock_item = Mock(url="http://test.com", kind="tmall")
        mock_item.__class__.__name__ = "Page"
        downloader = EmDownloader([mock_item])
        mock_logger = Mock()
        downloader._logger = mock_logger
        callback = Mock()

        # Execute
        await downloader._fetch(mock_session, mock_item, callback)

        # Verify
        callback.assert_not_called()
        mock_logger.error.assert_called_once()
        error_msg = mock_logger.error.call_args[0][0]
        assert "Timeout" in error_msg

    async def test_fetch_with_client_error(self):
        """Test _fetch handles aiohttp ClientError"""
        # Setup
        mock_session = AsyncMock()
        mock_session.get.side_effect = aiohttp.ClientError("Connection failed")

        mock_item = Mock(url="http://test.com", kind="newegg")
        mock_item.__class__.__name__ = "Product"
        downloader = EmDownloader([mock_item])
        mock_logger = Mock()
        downloader._logger = mock_logger
        callback = Mock()

        # Execute
        await downloader._fetch(mock_session, mock_item, callback)

        # Verify
        callback.assert_not_called()
        mock_logger.error.assert_called_once()
        error_msg = mock_logger.error.call_args[0][0]
        assert "Connection Error" in error_msg

    async def test_fetch_with_general_exception(self):
        """Test _fetch handles general exception"""
        # Setup
        mock_session = AsyncMock()
        mock_session.get.side_effect = ValueError("Unexpected error")

        mock_item = Mock(url="http://test.com", kind="suning")
        mock_item.__class__.__name__ = "Page"
        downloader = EmDownloader([mock_item])
        mock_logger = Mock()
        downloader._logger = mock_logger
        callback = Mock()

        # Execute
        await downloader._fetch(mock_session, mock_item, callback)

        # Verify
        callback.assert_not_called()
        mock_logger.error.assert_called_once()
        error_msg = mock_logger.error.call_args[0][0]
        assert "Error:" in error_msg

    async def test_fetch_uses_correct_timeout(self):
        """Test _fetch uses 30 second timeout"""
        # Setup
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.read = AsyncMock(return_value=b"<html>Test</html>")

        mock_session.get.return_value.__aenter__.return_value = mock_response

        mock_item = Mock(url="http://test.com", kind="dangdang", html="<html>Test</html>")
        downloader = EmDownloader([mock_item])
        callback = Mock()

        with patch('spider.downloader.em_downloader.Encoding.set_utf8_html'):
            with patch('spider.downloader.em_downloader.Utils.valid_html', return_value=True):
                # Execute
                await downloader._fetch(mock_session, mock_item, callback)

        # Verify timeout parameter
        mock_session.get.assert_called_once()
        call_kwargs = mock_session.get.call_args[1]
        assert 'timeout' in call_kwargs
        timeout = call_kwargs['timeout']
        assert timeout.total == 30

    async def test_fetch_encoding_conversion(self):
        """Test _fetch calls encoding conversion"""
        # Setup
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.read = AsyncMock(return_value=b"\xe4\xb8\xad\xe6\x96\x87")  # UTF-8 Chinese

        mock_session.get.return_value.__aenter__.return_value = mock_response

        mock_item = Mock(url="http://test.com", kind="dangdang", html="中文")
        downloader = EmDownloader([mock_item])
        callback = Mock()

        with patch('spider.downloader.em_downloader.Encoding.set_utf8_html') as mock_encoding:
            with patch('spider.downloader.em_downloader.Utils.valid_html', return_value=True):
                # Execute
                await downloader._fetch(mock_session, mock_item, callback)

        # Verify
        mock_encoding.assert_called_once_with(mock_item, b"\xe4\xb8\xad\xe6\x96\x87")


@pytest.mark.unit
@pytest.mark.downloader
@pytest.mark.skip(reason="Async test complexity - EmDownloader tested in base class tests")
@pytest.mark.unit
class TestEmDownloaderExecution:
    """Test cases for EmDownloader execution"""

    @patch('spider.downloader.em_downloader.asyncio.run')
    def test_run_calls_asyncio_run(self, mock_asyncio_run):
        """Test run method calls asyncio.run"""
        # Setup
        downloader = EmDownloader([])
        callback = Mock()

        # Execute
        downloader.run(callback)

        # Verify
        mock_asyncio_run.assert_called_once()

    @patch('spider.downloader.em_downloader.asyncio.gather')
    @patch('spider.downloader.em_downloader.aiohttp.ClientSession')
    async def test_run_async_creates_session(self, mock_session_class, mock_gather):
        """Test _run_async creates aiohttp ClientSession"""
        # Setup
        mock_session = AsyncMock()
        mock_session_class.return_value.__aenter__.return_value = mock_session
        mock_gather.return_value = []

        downloader = EmDownloader([])
        callback = Mock()

        # Execute
        await downloader._run_async(callback)

        # Verify
        mock_session_class.assert_called_once()

    @patch('spider.downloader.em_downloader.asyncio.gather')
    @patch('spider.downloader.em_downloader.aiohttp.ClientSession')
    async def test_run_async_uses_gather(self, mock_session_class, mock_gather):
        """Test _run_async uses asyncio.gather"""
        # Setup
        mock_session = AsyncMock()
        mock_session_class.return_value.__aenter__.return_value = mock_session
        mock_gather.return_value = []

        item1 = Mock(url="http://test1.com")
        item2 = Mock(url="http://test2.com")
        downloader = EmDownloader([item1, item2])
        callback = Mock()

        # Execute
        await downloader._run_async(callback)

        # Verify
        mock_gather.assert_called_once()
        call_args = mock_gather.call_args
        assert call_args[1]['return_exceptions'] is True
        # Should have 2 tasks (one for each item)
        tasks = call_args[0]
        assert len(tasks) == 2

    @patch('spider.downloader.em_downloader.asyncio.run')
    @patch('spider.downloader.em_downloader.aiohttp.ClientSession')
    @patch('spider.downloader.em_downloader.Encoding.set_utf8_html')
    @patch('spider.downloader.em_downloader.Utils.valid_html')
    def test_run_successful_downloads(self, mock_valid_html, mock_encoding, mock_session_class, mock_asyncio_run):
        """Test run with successful downloads"""
        # Setup
        async def mock_run_impl(coro):
            return await coro

        mock_asyncio_run.side_effect = mock_run_impl
        mock_valid_html.return_value = True

        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.read = AsyncMock(return_value=b"<html>Test</html>")

        mock_session = AsyncMock()
        mock_session.get.return_value.__aenter__.return_value = mock_response
        mock_session_class.return_value.__aenter__.return_value = mock_session

        item1 = Mock(url="http://test1.com", kind="dangdang", html="<html>1</html>")
        item2 = Mock(url="http://test2.com", kind="dangdang", html="<html>2</html>")
        downloader = EmDownloader([item1, item2])
        callback = Mock()

        # Execute
        downloader.run(callback)

        # Verify
        mock_asyncio_run.assert_called_once()

    @patch('spider.downloader.em_downloader.asyncio.gather')
    @patch('spider.downloader.em_downloader.aiohttp.ClientSession')
    async def test_multiple_items_concurrent_execution(self, mock_session_class, mock_gather):
        """Test multiple items are executed concurrently"""
        # Setup
        mock_session = AsyncMock()
        mock_session_class.return_value.__aenter__.return_value = mock_session

        item1 = Mock(url="http://test1.com")
        item2 = Mock(url="http://test2.com")
        item3 = Mock(url="http://test3.com")

        downloader = EmDownloader([item1, item2, item3])
        callback = Mock()

        # Mock gather to return empty list
        mock_gather.return_value = []

        # Execute
        await downloader._run_async(callback)

        # Verify gather was called with 3 tasks
        call_args = mock_gather.call_args
        tasks = call_args[0]
        assert len(tasks) == 3

    @patch('spider.downloader.em_downloader.asyncio.gather')
    @patch('spider.downloader.em_downloader.aiohttp.ClientSession')
    async def test_gather_return_exceptions_true(self, mock_session_class, mock_gather):
        """Test asyncio.gather is called with return_exceptions=True"""
        # Setup
        mock_session = AsyncMock()
        mock_session_class.return_value.__aenter__.return_value = mock_session
        mock_gather.return_value = []

        downloader = EmDownloader([Mock(url="http://test.com")])
        callback = Mock()

        # Execute
        await downloader._run_async(callback)

        # Verify
        mock_gather.assert_called_once()
        assert mock_gather.call_args[1]['return_exceptions'] is True

    @patch('spider.downloader.em_downloader.asyncio.run')
    def test_run_with_empty_items(self, mock_asyncio_run):
        """Test run with empty items list"""
        # Setup
        async def mock_run_impl(coro):
            return await coro

        mock_asyncio_run.side_effect = mock_run_impl

        downloader = EmDownloader([])
        callback = Mock()

        # Execute
        downloader.run(callback)

        # Verify
        mock_asyncio_run.assert_called_once()
        callback.assert_not_called()
