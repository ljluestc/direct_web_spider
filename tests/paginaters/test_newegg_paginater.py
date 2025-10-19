"""
Comprehensive unit tests for spider.paginater.newegg_paginater
"""
import pytest
from unittest.mock import Mock
from spider.paginater.newegg_paginater import NeweggPaginater
from spider.paginater import Paginater


@pytest.mark.unit
@pytest.mark.paginater
@pytest.mark.unit
class TestNeweggPaginaterBase:
    """Test cases for NeweggPaginater base functionality"""

    def test_newegg_paginater_exists(self):
        """Test NeweggPaginater exists"""
        assert NeweggPaginater is not None

    def test_newegg_paginater_is_class(self):
        """Test NeweggPaginater is a class"""
        assert isinstance(NeweggPaginater, type)

    def test_newegg_paginater_inherits_paginater(self):
        """Test NeweggPaginater inherits from Paginater"""
        assert issubclass(NeweggPaginater, Paginater)

    def test_newegg_paginater_initialization(self):
        """Test NeweggPaginater initialization"""
        html = "<html><body>Test</body></html>"
        item = Mock(url="http://www.newegg.com/Product/ProductList.htm", html=html)
        paginater = NeweggPaginater(item)
        assert paginater is not None
        assert paginater.url == "http://www.newegg.com/Product/ProductList.htm"
        assert paginater.doc is not None


@pytest.mark.unit
@pytest.mark.paginater
@pytest.mark.unit
class TestNeweggPaginaterPaginationList:
    """Test cases for pagination_list() method"""

    def test_pagination_list_single_page(self):
        """Test pagination with single page"""
        html = """
        <html>
            <div class="pageNav">
                <a><span>1</span></a>
            </div>
        </html>
        """
        item = Mock(url="http://www.newegg.com/Product/ProductList.htm", html=html)
        paginater = NeweggPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 1
        assert urls[0] == "http://www.newegg.com/Product/ProductList-1.htm"

    def test_pagination_list_multiple_pages(self):
        """Test pagination with multiple pages"""
        html = """
        <html>
            <div class="pageNav">
                <a><span>1</span></a>
                <a><span>2</span></a>
                <a><span>3</span></a>
            </div>
        </html>
        """
        item = Mock(url="http://www.newegg.com/Product/ProductList.htm", html=html)
        paginater = NeweggPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 3
        assert urls[0] == "http://www.newegg.com/Product/ProductList-1.htm"
        assert urls[1] == "http://www.newegg.com/Product/ProductList-2.htm"
        assert urls[2] == "http://www.newegg.com/Product/ProductList-3.htm"

    def test_pagination_list_with_text_descendants(self):
        """Test pagination extracting numbers from descendants"""
        html = """
        <html>
            <div class="pageNav">
                <a>1</a>
                <a>2</a>
            </div>
        </html>
        """
        item = Mock(url="http://www.newegg.com/Product/ProductList.htm", html=html)
        paginater = NeweggPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 2
        assert urls[0].endswith("-1.htm")
        assert urls[1].endswith("-2.htm")

    def test_pagination_list_missing_pagenav(self):
        """Test pagination when .pageNav is missing"""
        html = "<html><body>No pagination</body></html>"
        item = Mock(url="http://www.newegg.com/Product/ProductList.htm", html=html)
        paginater = NeweggPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 1
        assert urls[0] == "http://www.newegg.com/Product/ProductList-1.htm"

    def test_pagination_list_url_replacement(self):
        """Test that .htm is correctly replaced"""
        html = """
        <html>
            <div class="pageNav">
                <a>1</a>
                <a>2</a>
            </div>
        </html>
        """
        item = Mock(url="http://www.newegg.com/laptops.htm", html=html)
        paginater = NeweggPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 2
        assert all(".htm" in url for url in urls)
        assert all("-" in url for url in urls)
        assert "laptops-1.htm" in urls[0]
        assert "laptops-2.htm" in urls[1]

    def test_pagination_list_large_page_count(self):
        """Test pagination with many pages"""
        html_links = "".join([f"<a>{i}</a>" for i in range(1, 51)])
        html = f"""
        <html>
            <div class="pageNav">
                {html_links}
            </div>
        </html>
        """
        item = Mock(url="http://www.newegg.com/Product/ProductList.htm", html=html)
        paginater = NeweggPaginater(item)

        urls = paginater.pagination_list()
        assert len(urls) == 50
        assert urls[0].endswith("-1.htm")
        assert urls[49].endswith("-50.htm")

    def test_pagination_list_ignores_non_numeric_text(self):
        """Test pagination ignores non-numeric text (triggers ValueError exception)"""
        html = """
        <html>
            <div class="pageNav">
                <a><span>Next</span></a>
                <a><span>Previous</span></a>
                <a><span>1</span></a>
                <a><span>2</span></a>
                <a><span>Last</span></a>
            </div>
        </html>
        """
        item = Mock(url="http://www.newegg.com/Product/ProductList.htm", html=html)
        paginater = NeweggPaginater(item)

        urls = paginater.pagination_list()
        # Should only count numeric values
        assert len(urls) == 2
        assert urls[0].endswith("-1.htm")
        assert urls[1].endswith("-2.htm")
