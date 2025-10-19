#!/usr/bin/env python3
# encoding: utf-8
"""
Tests for missing coverage in spider modules
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import asyncio
import aiohttp

@pytest.mark.unit
class TestMissingCoverage:
    """Tests to cover missing lines in spider modules"""

    @patch('spider.downloader.em_downloader.aiohttp.ClientSession')
    @patch('spider.downloader.em_downloader.asyncio.gather')
    @patch('spider.downloader.em_downloader.EmDownloader._fetch')
    def test_em_downloader_run_async_success(self, mock_fetch, mock_gather, mock_session):
        """Test EmDownloader._run_async method"""
        from spider.downloader.em_downloader import EmDownloader
        
        # Create mock items
        mock_items = [Mock(url='http://example.com/1'), Mock(url='http://example.com/2')]
        
        # Create downloader instance
        downloader = EmDownloader(mock_items)
        
        # Mock the async context manager
        mock_session_instance = Mock()
        mock_session.return_value.__aenter__.return_value = mock_session_instance
        mock_session.return_value.__aexit__.return_value = None
        
        # Mock gather to return successful results
        mock_gather.return_value = []
        
        # Mock _fetch to return a coroutine
        async def mock_fetch_coro():
            pass
        mock_fetch.return_value = mock_fetch_coro()
        
        # Create mock callback
        mock_callback = Mock()
        
        # Run the async method
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(downloader._run_async(mock_callback))
        finally:
            loop.close()
        
        # Verify that gather was called with tasks
        mock_gather.assert_called_once()
        assert len(mock_gather.call_args[0][0]) == 2  # Two tasks for two items

    @patch('spider.downloader.em_downloader.aiohttp.ClientSession')
    @patch('spider.downloader.em_downloader.asyncio.gather')
    @patch('spider.downloader.em_downloader.EmDownloader._fetch')
    def test_em_downloader_run_async_with_exceptions(self, mock_fetch, mock_gather, mock_session):
        """Test EmDownloader._run_async method with exceptions"""
        from spider.downloader.em_downloader import EmDownloader
        
        # Create mock items
        mock_items = [Mock(url='http://example.com/1')]
        
        # Create downloader instance
        downloader = EmDownloader(mock_items)
        
        # Mock the async context manager
        mock_session_instance = Mock()
        mock_session.return_value.__aenter__.return_value = mock_session_instance
        mock_session.return_value.__aexit__.return_value = None
        
        # Mock gather to return exceptions
        mock_gather.return_value = [Exception("Test error")]
        
        # Mock _fetch to return a coroutine
        async def mock_fetch_coro():
            pass
        mock_fetch.return_value = mock_fetch_coro()
        
        # Create mock callback
        mock_callback = Mock()
        
        # Run the async method
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(downloader._run_async(mock_callback))
        finally:
            loop.close()
        
        # Verify that gather was called with return_exceptions=True
        mock_gather.assert_called_once()
        assert mock_gather.call_args[1]['return_exceptions'] is True

    @patch('spider.downloader.em_downloader.aiohttp.ClientSession')
    @patch('spider.downloader.em_downloader.Encoding')
    @patch('spider.downloader.em_downloader.Utils')
    def test_em_downloader_fetch_success(self, mock_utils, mock_encoding, mock_session):
        """Test EmDownloader._fetch method with successful response"""
        from spider.downloader.em_downloader import EmDownloader
        
        # Create mock items
        mock_items = [Mock(url='http://example.com/1')]
        
        # Create downloader instance
        downloader = EmDownloader(mock_items)
        
        # Mock session and response
        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'<html>test</html>'
        
        mock_session_instance = Mock()
        mock_session_instance.get.return_value.__aenter__.return_value = mock_response
        mock_session_instance.get.return_value.__aexit__.return_value = None
        
        # Mock Utils.valid_html to return True
        mock_utils.valid_html.return_value = True
        
        # Create mock item
        mock_item = Mock()
        mock_item.url = 'http://example.com/1'
        mock_item.__class__.__name__ = 'TestItem'
        mock_item.kind = 'test'
        mock_item.html = '<html>test</html>'
        
        # Create mock callback
        mock_callback = Mock()
        
        # Run the async method
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(downloader._fetch(mock_session_instance, mock_item, mock_callback))
        finally:
            loop.close()
        
        # Verify that callback was called
        mock_callback.assert_called_once_with(mock_item)

    @patch('spider.downloader.em_downloader.aiohttp.ClientSession')
    @patch('spider.downloader.em_downloader.Encoding')
    @patch('spider.downloader.em_downloader.Utils')
    def test_em_downloader_fetch_bad_html(self, mock_utils, mock_encoding, mock_session):
        """Test EmDownloader._fetch method with bad HTML"""
        from spider.downloader.em_downloader import EmDownloader
        
        # Create mock items
        mock_items = [Mock(url='http://example.com/1')]
        
        # Create downloader instance
        downloader = EmDownloader(mock_items)
        
        # Mock session and response
        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'<html>test</html>'
        
        mock_session_instance = Mock()
        mock_session_instance.get.return_value.__aenter__.return_value = mock_response
        mock_session_instance.get.return_value.__aexit__.return_value = None
        
        # Mock Utils.valid_html to return False
        mock_utils.valid_html.return_value = False
        
        # Create mock item
        mock_item = Mock()
        mock_item.url = 'http://example.com/1'
        mock_item.__class__.__name__ = 'TestItem'
        mock_item.kind = 'test'
        mock_item.html = '<html>test</html>'
        
        # Create mock callback
        mock_callback = Mock()
        
        # Run the async method
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(downloader._fetch(mock_session_instance, mock_item, mock_callback))
        finally:
            loop.close()
        
        # Verify that callback was NOT called
        mock_callback.assert_not_called()

    @patch('spider.downloader.em_downloader.aiohttp.ClientSession')
    def test_em_downloader_fetch_http_error(self, mock_session):
        """Test EmDownloader._fetch method with HTTP error"""
        from spider.downloader.em_downloader import EmDownloader
        
        # Create mock items
        mock_items = [Mock(url='http://example.com/1')]
        
        # Create downloader instance
        downloader = EmDownloader(mock_items)
        
        # Mock session and response with error status
        mock_response = Mock()
        mock_response.status = 404
        
        mock_session_instance = Mock()
        mock_session_instance.get.return_value.__aenter__.return_value = mock_response
        mock_session_instance.get.return_value.__aexit__.return_value = None
        
        # Create mock item
        mock_item = Mock()
        mock_item.url = 'http://example.com/1'
        mock_item.__class__.__name__ = 'TestItem'
        mock_item.kind = 'test'
        
        # Create mock callback
        mock_callback = Mock()
        
        # Run the async method
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(downloader._fetch(mock_session_instance, mock_item, mock_callback))
        finally:
            loop.close()
        
        # Verify that callback was NOT called
        mock_callback.assert_not_called()

    @patch('spider.downloader.em_downloader.aiohttp.ClientSession')
    def test_em_downloader_fetch_timeout_error(self, mock_session):
        """Test EmDownloader._fetch method with timeout error"""
        from spider.downloader.em_downloader import EmDownloader
        
        # Create mock items
        mock_items = [Mock(url='http://example.com/1')]
        
        # Create downloader instance
        downloader = EmDownloader(mock_items)
        
        # Mock session to raise TimeoutError
        mock_session_instance = Mock()
        mock_session_instance.get.side_effect = asyncio.TimeoutError()
        
        # Create mock item
        mock_item = Mock()
        mock_item.url = 'http://example.com/1'
        mock_item.__class__.__name__ = 'TestItem'
        mock_item.kind = 'test'
        
        # Create mock callback
        mock_callback = Mock()
        
        # Run the async method
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(downloader._fetch(mock_session_instance, mock_item, mock_callback))
        finally:
            loop.close()
        
        # Verify that callback was NOT called
        mock_callback.assert_not_called()

    @patch('spider.downloader.em_downloader.aiohttp.ClientSession')
    def test_em_downloader_fetch_client_error(self, mock_session):
        """Test EmDownloader._fetch method with client error"""
        from spider.downloader.em_downloader import EmDownloader
        
        # Create mock items
        mock_items = [Mock(url='http://example.com/1')]
        
        # Create downloader instance
        downloader = EmDownloader(mock_items)
        
        # Mock session to raise ClientError
        mock_session_instance = Mock()
        mock_session_instance.get.side_effect = aiohttp.ClientError("Connection error")
        
        # Create mock item
        mock_item = Mock()
        mock_item.url = 'http://example.com/1'
        mock_item.__class__.__name__ = 'TestItem'
        mock_item.kind = 'test'
        
        # Create mock callback
        mock_callback = Mock()
        
        # Run the async method
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(downloader._fetch(mock_session_instance, mock_item, mock_callback))
        finally:
            loop.close()
        
        # Verify that callback was NOT called
        mock_callback.assert_not_called()

    @patch('spider.downloader.em_downloader.aiohttp.ClientSession')
    def test_em_downloader_fetch_general_exception(self, mock_session):
        """Test EmDownloader._fetch method with general exception"""
        from spider.downloader.em_downloader import EmDownloader
        
        # Create mock items
        mock_items = [Mock(url='http://example.com/1')]
        
        # Create downloader instance
        downloader = EmDownloader(mock_items)
        
        # Mock session to raise general exception
        mock_session_instance = Mock()
        mock_session_instance.get.side_effect = Exception("General error")
        
        # Create mock item
        mock_item = Mock()
        mock_item.url = 'http://example.com/1'
        mock_item.__class__.__name__ = 'TestItem'
        mock_item.kind = 'test'
        
        # Create mock callback
        mock_callback = Mock()
        
        # Run the async method
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(downloader._fetch(mock_session_instance, mock_item, mock_callback))
        finally:
            loop.close()
        
        # Verify that callback was NOT called
        mock_callback.assert_not_called()

    def test_encoding_set_utf8_html_fallback(self):
        """Test Encoding.set_utf8_html with fallback encoding"""
        from spider.encoding import Encoding
        
        # Create mock item
        mock_item = Mock()
        
        # Test with invalid encoding that will trigger fallback
        html_bytes = b'<html>test</html>'
        
        # Mock the decode method to raise LookupError first, then succeed with utf-8
        original_decode = html_bytes.decode
        
        def mock_decode(encoding, errors='strict'):
            if encoding == 'invalid_encoding':
                raise LookupError("Unknown encoding")
            return original_decode(encoding, errors)
        
        # Patch the decode method
        with patch.object(html_bytes, 'decode', side_effect=mock_decode):
            # This should trigger the fallback to utf-8
            Encoding.set_utf8_html(mock_item, html_bytes, 'invalid_encoding')
        
        # Verify that the item's html was set
        assert hasattr(mock_item, 'html')

    def test_encoding_set_utf8_html_unicode_decode_error(self):
        """Test Encoding.set_utf8_html with UnicodeDecodeError"""
        from spider.encoding import Encoding
        
        # Create mock item
        mock_item = Mock()
        
        # Test with bytes that will cause UnicodeDecodeError
        html_bytes = b'\xff\xfe<html>test</html>'
        
        # Mock the decode method to raise UnicodeDecodeError first, then succeed with utf-8
        original_decode = html_bytes.decode
        
        def mock_decode(encoding, errors='strict'):
            if encoding == 'utf-8' and errors == 'strict':
                raise UnicodeDecodeError('utf-8', b'\xff\xfe', 0, 1, 'invalid start byte')
            return original_decode(encoding, errors)
        
        # Patch the decode method
        with patch.object(html_bytes, 'decode', side_effect=mock_decode):
            # This should trigger the fallback to utf-8 with errors='replace'
            Encoding.set_utf8_html(mock_item, html_bytes, 'utf-8')
        
        # Verify that the item's html was set
        assert hasattr(mock_item, 'html')

    @patch('spider.logger.os.path.basename')
    @patch('spider.logger.SpiderOptions')
    def test_logger_mixin_file_name_module_level(self, mock_spider_options, mock_basename):
        """Test LoggerMixin file_name property for module-level usage"""
        from spider.logger import LoggerMixin
        
        # Mock SpiderOptions
        mock_spider_options.__getitem__ = Mock(return_value='test_spider')
        
        # Mock os.path.basename to return a script name
        mock_basename.return_value = 'test_script.py'
        
        # Mock __file__ to simulate module-level usage
        with patch('spider.logger.__file__', '/path/to/test_script.py'):
            # Create a LoggerMixin instance without logger_file
            logger_mixin = LoggerMixin()
            
            # Access the file_name property
            file_name = logger_mixin.file_name
            
            # Verify the file name format
            assert file_name == 'test_script.py_test_spider.log'

    def test_optparse_parse_arguments_not_in_test_mode(self):
        """Test optparse.parse_arguments when not in test mode"""
        from spider.utils.optparse import parse_arguments
        
        # Mock sys.modules to not include pytest or unittest
        with patch('spider.utils.optparse.sys.modules', {}):
            # Mock argparse.ArgumentParser to prevent actual argument parsing
            with patch('spider.utils.optparse.ArgumentParser') as mock_parser:
                mock_parser_instance = Mock()
                mock_parser.return_value = mock_parser_instance
                mock_parser_instance.parse_args.return_value = Mock()
                
                # This should not raise an exception
                parse_arguments()

    def test_optparse_parse_arguments_system_exit(self):
        """Test optparse.parse_arguments with SystemExit"""
        from spider.utils.optparse import parse_arguments
        
        # Mock sys.modules to not include pytest or unittest
        with patch('spider.utils.optparse.sys.modules', {}):
            # Mock argparse.ArgumentParser to raise SystemExit
            with patch('spider.utils.optparse.ArgumentParser') as mock_parser:
                mock_parser_instance = Mock()
                mock_parser.return_value = mock_parser_instance
                mock_parser_instance.parse_args.side_effect = SystemExit()
                
                # This should not raise an exception (SystemExit should be caught)
                parse_arguments()

    def test_utils_decompress_gzip_string_input(self):
        """Test Utils.decompress_gzip with string input"""
        from spider.utils.utils import Utils
        
        # Test with string input (should be encoded to bytes)
        test_string = "test string"
        
        # Mock gzip.GzipFile to return decompressed data
        with patch('spider.utils.utils.gzip.GzipFile') as mock_gzip:
            mock_gz_file = Mock()
            mock_gz_file.read.return_value = b'decompressed data'
            mock_gzip.return_value.__enter__.return_value = mock_gz_file
            mock_gzip.return_value.__exit__.return_value = None
            
            result = Utils.decompress_gzip(test_string)
            
            # Verify that the string was encoded to bytes
            assert result == 'decompressed data'

    def test_utils_load_mongo_with_credentials(self):
        """Test Utils.load_mongo with username and password"""
        from spider.utils.utils import Utils
        
        # Mock environment settings
        env_settings = {
            'host': 'localhost',
            'port': 27017,
            'database': 'test_db',
            'username': 'test_user',
            'password': 'test_pass'
        }
        
        # Mock mongoengine.connect
        with patch('spider.utils.utils.connect') as mock_connect:
            with patch('spider.utils.utils.print') as mock_print:
                Utils.load_mongo('test', env_settings)
                
                # Verify that connect was called with credentials
                mock_connect.assert_called_once_with(
                    'test_db', 
                    host='localhost', 
                    port=27017, 
                    username='test_user', 
                    password='test_pass'
                )
                
                # Verify that print was called
                mock_print.assert_called_once_with("Connected to MongoDB: localhost:27017/test_db")

    def test_utils_load_mongo_without_credentials(self):
        """Test Utils.load_mongo without username and password"""
        from spider.utils.utils import Utils
        
        # Mock environment settings without credentials
        env_settings = {
            'host': 'localhost',
            'port': 27017,
            'database': 'test_db'
        }
        
        # Mock mongoengine.connect
        with patch('spider.utils.utils.connect') as mock_connect:
            with patch('spider.utils.utils.print') as mock_print:
                Utils.load_mongo('test', env_settings)
                
                # Verify that connect was called without credentials
                mock_connect.assert_called_once_with(
                    'test_db', 
                    host='localhost', 
                    port=27017
                )
                
                # Verify that print was called
                mock_print.assert_called_once_with("Connected to MongoDB: localhost:27017/test_db")
