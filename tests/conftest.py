"""
Pytest Configuration and Shared Fixtures
"""
import os
import sys
from unittest.mock import Mock, MagicMock, patch

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from bs4 import BeautifulSoup


@pytest.fixture(scope='session')
def mongodb_connection():
    """Create MongoDB test connection"""
    import mongomock
    # Connect to test database using mongomock
    return mongomock.MongoClient().test_db


@pytest.fixture(scope='function')
def clean_db(mongodb_connection):
    """Clean database before each test"""
    from spider.models.category import Category
    from spider.models.page import Page
    from spider.models.product_url import ProductUrl
    from spider.models.product import Product
    from spider.models.brand import Brand
    from spider.models.merchant import Merchant
    from spider.models.comment import Comment
    from spider.models.body import Body
    from spider.models.top_product import TopProduct
    from spider.models.middle_product import MiddleProduct
    from spider.models.end_product import EndProduct
    from spider.models.brand_type import BrandType

    # Clear all collections
    Category.drop_collection()
    Page.drop_collection()
    ProductUrl.drop_collection()
    Product.drop_collection()
    Brand.drop_collection()
    Merchant.drop_collection()
    Comment.drop_collection()
    Body.drop_collection()
    TopProduct.drop_collection()
    MiddleProduct.drop_collection()
    EndProduct.drop_collection()
    BrandType.drop_collection()


@pytest.fixture
def mock_category():
    """Mock Category object"""
    mock = Mock()
    mock.url = "http://example.com/category"
    mock.name = "Test Category"
    return mock


@pytest.fixture
def mock_page():
    """Mock Page object"""
    mock = Mock()
    mock.url = "http://example.com/page"
    mock.html = "<html><body>Test</body></html>"
    return mock


@pytest.fixture
def mock_product_url():
    """Mock ProductUrl object"""
    mock = Mock()
    mock.url = "http://example.com/product/12345"
    mock.title = "Test Product"
    return mock


@pytest.fixture
def mock_product():
    """Mock Product object"""
    mock = Mock()
    mock.title = "Test Product"
    mock.price = 99.99
    mock.stock = 10
    mock.score = 4.5
    mock.url = "http://example.com/product/12345"
    return mock


@pytest.fixture
def sample_html():
    """Sample HTML for testing parsers"""
    return """
    <html>
    <head><title>Test Page</title></head>
    <body>
        <div class="dp_wrap">
            <h1>Test Product Title</h1>
        </div>
        <div id="salePriceTag">$99</div>
        <img id="largePic" src="http://example.com/image.jpg" />
        <p class="fraction">
            <img src="star_red.png" />
            <img src="star_red.png" />
            <img src="star_red.png" />
            <img src="star_red.png" />
            <img src="star_red.png" />
        </p>
    </body>
    </html>
    """


@pytest.fixture
def sample_soup(sample_html):
    """BeautifulSoup object from sample HTML"""
    return BeautifulSoup(sample_html, 'lxml')


@pytest.fixture
def mock_requests_response():
    """Mock requests.Response object"""
    mock = Mock()
    mock.status_code = 200
    mock.text = "<html><body>Test</body></html>"
    mock.encoding = 'utf-8'
    return mock


@pytest.fixture
def mock_aiohttp_response():
    """Mock aiohttp response"""
    mock = MagicMock()
    mock.status = 200
    mock.text.return_value = "<html><body>Test</body></html>"
    return mock


@pytest.fixture
def spider_options():
    """Default SpiderOptions for testing"""
    return {
        'name': 'dangdang',
        'url': 'http://example.com',
        'max_pages': 10
    }


@pytest.fixture
def mock_logger():
    """Mock logger object"""
    logger = Mock()
    logger.info = Mock()
    logger.error = Mock()
    logger.warning = Mock()
    logger.debug = Mock()
    return logger


@pytest.fixture(autouse=True)
def reset_spider_options():
    """Reset SpiderOptions before each test"""
    from spider.utils.optparse import SpiderOptions
    SpiderOptions['name'] = 'dangdang'
    SpiderOptions['url'] = 'http://example.com'
    SpiderOptions['max_pages'] = 10
    yield
    # Reset after test
    SpiderOptions['name'] = 'dangdang'
    SpiderOptions['url'] = 'http://example.com'
    SpiderOptions['max_pages'] = 10


@pytest.fixture
def temp_log_dir(tmp_path):
    """Create temporary log directory"""
    log_dir = tmp_path / "log"
    log_dir.mkdir()
    return log_dir


@pytest.fixture
def mock_mongodb_models():
    """Mock all MongoDB models"""
    with patch('spider.models.category.Category') as mock_category, \
         patch('spider.models.page.Page') as mock_page, \
         patch('spider.models.product_url.ProductUrl') as mock_product_url, \
         patch('spider.models.product.Product') as mock_product, \
         patch('spider.models.brand.Brand') as mock_brand, \
         patch('spider.models.merchant.Merchant') as mock_merchant, \
         patch('spider.models.comment.Comment') as mock_comment, \
         patch('spider.models.body.Body') as mock_body, \
         patch('spider.models.top_product.TopProduct') as mock_top_product, \
         patch('spider.models.middle_product.MiddleProduct') as mock_middle_product, \
         patch('spider.models.end_product.EndProduct') as mock_end_product, \
         patch('spider.models.brand_type.BrandType') as mock_brand_type:
        yield {
            'category': mock_category,
            'page': mock_page,
            'product_url': mock_product_url,
            'product': mock_product,
            'brand': mock_brand,
            'merchant': mock_merchant,
            'comment': mock_comment,
            'body': mock_body,
            'top_product': mock_top_product,
            'middle_product': mock_middle_product,
            'end_product': mock_end_product,
            'brand_type': mock_brand_type
        }


@pytest.fixture
def sample_categories():
    """Sample category list"""
    return [
        {'name': 'Books', 'url': 'http://example.com/books'},
        {'name': 'Electronics', 'url': 'http://example.com/electronics'}
    ]


@pytest.fixture
def sample_product_urls():
    """Sample product URL list"""
    return [
        'http://example.com/product/1',
        'http://example.com/product/2',
        'http://example.com/product/3'
    ]


@pytest.fixture
def sample_pagination_urls():
    """Sample pagination URL list"""
    return [
        'http://example.com/list?p=1',
        'http://example.com/list?p=2',
        'http://example.com/list?p=3'
    ]


@pytest.fixture
def sample_comments():
    """Sample comment list"""
    return [
        {
            'content': 'Great product!',
            'rating': 5,
            'author': 'User1'
        },
        {
            'content': 'Not bad',
            'rating': 3,
            'author': 'User2'
        }
    ]


# Performance fixtures
@pytest.fixture
def performance_timer():
    """Timer for performance testing"""
    import time

    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None

        def start(self):
            self.start_time = time.time()

        def stop(self):
            self.end_time = time.time()

        def elapsed(self):
            if self.start_time and self.end_time:
                return self.end_time - self.start_time
            return None

    return Timer()