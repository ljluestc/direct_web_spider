"""
Comprehensive unit tests for spider.fetcher
"""
import pytest
import logging
from unittest.mock import Mock, patch
from spider.fetcher import Fetcher
from spider.logger import LoggerMixin


@pytest.mark.unit
class TestFetcherBase:
    """Test cases for Fetcher base class"""

    def test_fetcher_exists(self):
        """Test Fetcher class exists"""
        assert Fetcher is not None

    def test_fetcher_is_class(self):
        """Test Fetcher is a class"""
        assert isinstance(Fetcher, type)

    def test_fetcher_inherits_logger_mixin(self):
        """Test Fetcher inherits from LoggerMixin"""
        assert issubclass(Fetcher, LoggerMixin)

    def test_fetcher_has_category_list_method(self):
        """Test Fetcher has category_list classmethod"""
        assert hasattr(Fetcher, 'category_list')
        assert callable(Fetcher.category_list)

    def test_fetcher_category_list_is_classmethod(self):
        """Test category_list is a classmethod"""
        import inspect
        assert isinstance(inspect.getattr_static(Fetcher, 'category_list'), classmethod)

    def test_fetcher_category_list_raises_not_implemented(self):
        """Test category_list raises NotImplementedError"""
        with pytest.raises(NotImplementedError) as exc_info:
            Fetcher.category_list()

        assert "Subclass must implement category_list() method" in str(exc_info.value)

    def test_fetcher_can_be_instantiated(self):
        """Test Fetcher can be instantiated"""
        fetcher = Fetcher()
        assert fetcher is not None
        assert isinstance(fetcher, Fetcher)

    def test_fetcher_instance_has_logger(self):
        """Test Fetcher instance has logger from LoggerMixin"""
        fetcher = Fetcher()
        # Just check the attribute exists; actual logger functionality
        # is tested in LoggerMixin tests
        assert hasattr(fetcher, 'logger')

    def test_fetcher_instance_has_logger_file(self):
        """Test Fetcher instance has logger_file from LoggerMixin"""
        fetcher = Fetcher()
        assert hasattr(fetcher, 'logger_file')


@pytest.mark.unit
class TestFetcherSubclass:
    """Test cases for Fetcher subclassing behavior"""

    def test_subclass_can_override_category_list(self):
        """Test subclass can override category_list"""
        class TestFetcher(Fetcher):
            @classmethod
            def category_list(cls):
                return [{'name': 'Test', 'url': 'http://test.com'}]

        result = TestFetcher.category_list()
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]['name'] == 'Test'
        assert result[0]['url'] == 'http://test.com'

    def test_subclass_category_list_return_structure(self):
        """Test subclass category_list returns correct structure"""
        class TestFetcher(Fetcher):
            @classmethod
            def category_list(cls):
                return [
                    {'name': 'Electronics', 'url': 'http://test.com/electronics'},
                    {'name': 'Books', 'url': 'http://test.com/books'}
                ]

        categories = TestFetcher.category_list()
        assert len(categories) == 2
        for cat in categories:
            assert 'name' in cat
            assert 'url' in cat
            assert isinstance(cat['name'], str)
            assert isinstance(cat['url'], str)

    def test_subclass_can_be_instantiated(self):
        """Test Fetcher subclass can be instantiated"""
        class TestFetcher(Fetcher):
            @classmethod
            def category_list(cls):
                return []

        fetcher = TestFetcher()
        assert fetcher is not None
        assert isinstance(fetcher, TestFetcher)
        assert isinstance(fetcher, Fetcher)

    def test_multiple_subclasses_independent(self):
        """Test multiple Fetcher subclasses are independent"""
        class Fetcher1(Fetcher):
            @classmethod
            def category_list(cls):
                return [{'name': 'Cat1', 'url': 'http://1.com'}]

        class Fetcher2(Fetcher):
            @classmethod
            def category_list(cls):
                return [{'name': 'Cat2', 'url': 'http://2.com'}]

        result1 = Fetcher1.category_list()
        result2 = Fetcher2.category_list()

        assert result1[0]['name'] == 'Cat1'
        assert result2[0]['name'] == 'Cat2'

    def test_subclass_inherits_logger_mixin(self):
        """Test Fetcher subclass inherits LoggerMixin"""
        class TestFetcher(Fetcher):
            @classmethod
            def category_list(cls):
                return []

        assert issubclass(TestFetcher, LoggerMixin)
        fetcher = TestFetcher()
        assert hasattr(fetcher, 'logger')
        assert hasattr(fetcher, 'logger_file')


@pytest.mark.unit
class TestFetcherDocumentation:
    """Test cases for Fetcher documentation and interface"""

    def test_fetcher_has_docstring(self):
        """Test Fetcher class has docstring"""
        assert Fetcher.__doc__ is not None
        assert len(Fetcher.__doc__) > 0

    def test_category_list_has_docstring(self):
        """Test category_list method has docstring"""
        # Access the actual method, not the classmethod descriptor
        method = Fetcher.category_list.__func__
        assert method.__doc__ is not None
        assert 'category' in method.__doc__.lower() or 'fetch' in method.__doc__.lower()

    def test_fetcher_interface_contract(self):
        """Test Fetcher defines clear interface contract"""
        # Fetcher should define category_list as the contract
        assert hasattr(Fetcher, 'category_list')

        # Calling without implementation should raise NotImplementedError
        with pytest.raises(NotImplementedError):
            Fetcher.category_list()
