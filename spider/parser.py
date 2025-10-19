# encoding: utf-8
from bs4 import BeautifulSoup
from spider.logger import LoggerMixin


class Parser(LoggerMixin):
    """
    Base Parser class for parsing product details from product pages.
    Subclasses must implement all abstract methods.
    """

    def __init__(self, product):
        """
        Initialize parser with a product URL object.

        Args:
            product: ProductUrl object with 'html' attribute containing page HTML
        """
        self.product = product
        self.doc = BeautifulSoup(product.html, 'lxml')

    def attributes(self):
        """
        Return dictionary of all product attributes.

        Returns:
            dict: Product attributes for database storage
        """
        return {
            'kind': self.product.kind,
            'title': self.title(),
            'product_code': self.product_code(),
            'price': self.price(),
            'price_url': self.price_url(),
            'stock': self.stock(),
            'image_url': self.image_url(),
            'score': self.score(),
            'desc': self.desc(),
            'standard': self.standard(),
            'comments': self.comments(),
            'end_product': self.end_product(),
            'merchant': self.merchant(),
            'brand': self.brand(),
            'brand_type': self.brand_type(),
            'product_url_id': self.product.id
        }

    # Abstract methods - subclasses must implement these
    def title(self):
        """Extract product title"""
        raise NotImplementedError()

    def price(self):
        """Extract product price"""
        raise NotImplementedError()

    def price_url(self):
        """Extract price URL (for ajax-loaded prices)"""
        raise NotImplementedError()

    def stock(self):
        """Extract stock quantity"""
        raise NotImplementedError()

    def image_url(self):
        """Extract main product image URL"""
        raise NotImplementedError()

    def desc(self):
        """Extract product description"""
        raise NotImplementedError()

    def score(self):
        """Extract product score/rating"""
        raise NotImplementedError()

    def standard(self):
        """Extract product standard/specification"""
        raise NotImplementedError()

    def product_code(self):
        """Extract product code/SKU"""
        raise NotImplementedError()

    def comments(self):
        """
        Extract product comments/reviews.

        Returns:
            list: List of comment dicts with keys:
                - title: Comment title
                - content: Comment content
                - publish_at: Publication datetime
                - star: Star rating (integer)
        """
        raise NotImplementedError()

    def end_product(self):
        """Extract or find end product reference"""
        raise NotImplementedError()

    def merchant(self):
        """Extract or find merchant reference"""
        raise NotImplementedError()

    def brand(self):
        """Extract or find brand reference"""
        raise NotImplementedError()

    def brand_type(self):
        """Extract or find brand type reference"""
        raise NotImplementedError()

    def belongs_to_categories(self):
        """
        Extract category breadcrumb/hierarchy.

        Returns:
            list: List of dicts with 'name' and 'url' keys
                Example: [{'name': 'Electronics', 'url': 'http://...'}, ...]
        """
        raise NotImplementedError()
