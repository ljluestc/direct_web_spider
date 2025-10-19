"""
Error handling tests for downloader components
"""

import pytest
from unittest.mock import Mock, patch


class TestDownloaderErrorHandling:
    """Test downloader error handling"""

    @pytest.mark.error_handling
    def test_downloader_handles_connection_error(self):
        """Test downloader handles connection error"""
        from spider.downloader import NormalDownloader
        downloader = NormalDownloader([])
        mock_callback = Mock()
        
        with patch('requests.get') as mock_get:
            mock_get.side_effect = ConnectionError("Connection failed")
            downloader.run(mock_callback)
            # Should not call callback on error
            mock_callback.assert_not_called()

    @pytest.mark.error_handling
    def test_downloader_handles_timeout_error(self):
        """Test downloader handles timeout error"""
        from spider.downloader import NormalDownloader
        downloader = NormalDownloader([])
        mock_callback = Mock()
        
        with patch('requests.get') as mock_get:
            mock_get.side_effect = TimeoutError("Request timeout")
            downloader.run(mock_callback)
            mock_callback.assert_not_called()

    @pytest.mark.error_handling
    def test_downloader_handles_http_error(self):
        """Test downloader handles HTTP error"""
        from spider.downloader import NormalDownloader
        downloader = NormalDownloader([])
        mock_callback = Mock()
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.raise_for_status.side_effect = Exception("HTTP 500")
            mock_get.return_value = mock_response
            
            downloader.run(mock_callback)
            mock_callback.assert_not_called()

    @pytest.mark.error_handling
    def test_downloader_handles_general_exception(self):
        """Test downloader handles general exception"""
        from spider.downloader import NormalDownloader
        downloader = NormalDownloader([])
        mock_callback = Mock()
        
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("General error")
            downloader.run(mock_callback)
            mock_callback.assert_not_called()

    @pytest.mark.error_handling
    def test_downloader_handles_system_exit(self):
        """Test downloader handles system exit"""
        from spider.downloader import NormalDownloader
        downloader = NormalDownloader([])
        mock_callback = Mock()
        
        with patch('requests.get') as mock_get:
            mock_get.side_effect = SystemExit("System exit")
            # SystemExit should be caught by the general exception handler
            downloader.run(mock_callback)
            mock_callback.assert_not_called()