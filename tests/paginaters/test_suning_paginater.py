"""
Comprehensive unit tests for spider.paginater.suning_paginater
"""
import pytest
from unittest.mock import Mock, patch
from spider.paginater.suning_paginater import SuningPaginater
from spider.paginater import Paginater


@pytest.mark.unit
@pytest.mark.paginater
@pytest.mark.unit
class TestSuningPaginaterBase:
    """Test cases for SuningPaginater base functionality"""

    def test_suning_paginater_exists(self):
        """Test SuningPaginater exists"""
        assert SuningPaginater is not None

    def test_suning_paginater_inherits_paginater(self):
        """Test SuningPaginater inherits from Paginater"""
        assert issubclass(SuningPaginater, Paginater)


@pytest.mark.unit
@pytest.mark.paginater
@pytest.mark.unit
class TestSuningPaginaterParseUrlInfo:
    """Test cases for SuningPaginater _parse_url_info method"""

    def test_parse_url_info_complete_url(self):
        """Test URL parsing with complete parameters"""
        url = "http://www.suning.com/test_10051_20002_Y_30003_40004.html"
        item = Mock(url=url, html="<html></html>")
        paginater = SuningPaginater(item)

        info = paginater._parse_url_info()
        assert info['store_id'] == '10051'
        assert info['catalog_id'] == '20002'
        assert info['is_catalog_search'] == 'Y'
        assert info['category_id'] == '30003'

    def test_parse_url_info_minimal_url(self):
        """Test URL parsing with minimal parameters"""
        url = "http://www.suning.com/test.html"
        item = Mock(url=url, html="<html></html>")
        paginater = SuningPaginater(item)

        info = paginater._parse_url_info()
        assert info['store_id'] == ''
        assert info['catalog_id'] == ''

    def test_parse_url_info_returns_dict(self):
        """Test that _parse_url_info returns a dictionary"""
        url = "http://www.suning.com/test_123_456.html"
        item = Mock(url=url, html="<html></html>")
        paginater = SuningPaginater(item)

        info = paginater._parse_url_info()
        assert isinstance(info, dict)
        assert 'store_id' in info
        assert 'catalog_id' in info
        assert 'category_id' in info


@pytest.mark.unit
@pytest.mark.paginater
@pytest.mark.unit
class TestSuningPaginaterPaginationList:
    """Test cases for SuningPaginater pagination_list method"""

    def test_pagination_list_single_page(self):
        """Test pagination with single page"""
        html = """
        <html>
            <div id="pagetop">
                <span>1/1</span>
            </div>
        </html>
        """
        url = "http://www.suning.com/test_10051_20002_Y_30003_40004.html"
        item = Mock(url=url, html=html)
        paginater = SuningPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 1
        assert "currentPage=0" in urls[0]

    def test_pagination_list_multiple_pages(self):
        """Test pagination with multiple pages"""
        html = """
        <html>
            <div id="pagetop">
                <span>1/5</span>
            </div>
        </html>
        """
        url = "http://www.suning.com/test_10051_20002_Y_30003_40004.html"
        item = Mock(url=url, html=html)
        paginater = SuningPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 5

    def test_pagination_list_current_page_zero_indexed(self):
        """Test that currentPage parameter is 0-indexed"""
        html = """
        <html>
            <div id="pagetop">
                <span>1/3</span>
            </div>
        </html>
        """
        url = "http://www.suning.com/test_10051_20002_Y_30003_40004.html"
        item = Mock(url=url, html=html)
        paginater = SuningPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 3
        # Page 1: currentPage=0
        assert "currentPage=0" in urls[0]
        # Page 2: currentPage=1
        assert "currentPage=1" in urls[1]
        # Page 3: currentPage=2
        assert "currentPage=2" in urls[2]

    def test_pagination_list_no_pagetop(self):
        """Test pagination when pagetop element is missing"""
        html = """
        <html>
            <div>No pagination</div>
        </html>
        """
        url = "http://www.suning.com/test_10051_20002_Y_30003_40004.html"
        item = Mock(url=url, html=html)
        paginater = SuningPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 1

    def test_pagination_list_url_structure(self):
        """Test that URLs have correct structure"""
        html = """
        <html>
            <div id="pagetop">
                <span>1/2</span>
            </div>
        </html>
        """
        url = "http://www.suning.com/test_10051_20002_Y_30003_40004.html"
        item = Mock(url=url, html=html)
        paginater = SuningPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 2
        for url in urls:
            assert url.startswith("http://www.suning.com/webapp/wcs/stores/servlet/odeSearch?")
            assert "storeId=10051" in url
            assert "catalogId=20002" in url
            assert "categoryId=30003" in url
            assert "isCatalogSearch=Y" in url

    def test_pagination_list_returns_list(self):
        """Test pagination_list returns a list"""
        html = """
        <html>
            <div id="pagetop">
                <span>1/1</span>
            </div>
        </html>
        """
        url = "http://www.suning.com/test_10051_20002_Y_30003.html"
        item = Mock(url=url, html=html)
        paginater = SuningPaginater(item)

        result = paginater.pagination_list()
        assert isinstance(result, list)
