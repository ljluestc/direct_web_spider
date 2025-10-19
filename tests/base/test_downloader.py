"""
Comprehensive unit tests for spider.downloader
"""
import pytest
from unittest.mock import Mock
from spider.downloader import Downloader
from spider.logger import LoggerMixin


@pytest.mark.unit
class TestDownloaderBase:
    """Test cases for Downloader base class"""

    def test_downloader_exists(self):
        """Test Downloader exists"""
        assert Downloader is not None

    def test_downloader_is_class(self):
        """Test Downloader is a class"""
        assert isinstance(Downloader, type)

    def test_downloader_inherits_logger_mixin(self):
        """Test Downloader inherits LoggerMixin"""
        assert issubclass(Downloader, LoggerMixin)

    def test_downloader_can_be_instantiated(self):
        """Test Downloader can be instantiated"""
        downloader = Downloader()
        assert downloader is not None

    def test_downloader_has_max_concurrency_method(self):
        """Test Downloader has max_concurrency method"""
        assert hasattr(Downloader, 'max_concurrency')
        assert callable(Downloader.max_concurrency)

    def test_downloader_max_concurrency_default(self):
        """Test max_concurrency returns default 10"""
        downloader = Downloader()
        assert downloader.max_concurrency() == 10

    def test_downloader_has_run_method(self):
        """Test Downloader has run method"""
        assert hasattr(Downloader, 'run')
        assert callable(Downloader.run)

    def test_downloader_run_raises_not_implemented(self):
        """Test run raises NotImplementedError"""
        downloader = Downloader()
        with pytest.raises(NotImplementedError):
            downloader.run(lambda x: None)

    def test_subclass_can_override_max_concurrency(self):
        """Test subclass can override max_concurrency"""
        class TestDownloader(Downloader):
            def max_concurrency(self):
                return 20
            def run(self, callback):
                pass

        downloader = TestDownloader()
        assert downloader.max_concurrency() == 20

    def test_subclass_can_override_run(self):
        """Test subclass can override run method"""
        class TestDownloader(Downloader):
            def run(self, callback):
                callback(Mock(html="<html>test</html>"))

        downloader = TestDownloader()
        called = []
        downloader.run(lambda x: called.append(x))
        assert len(called) == 1
