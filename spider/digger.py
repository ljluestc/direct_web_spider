# encoding: utf-8
from bs4 import BeautifulSoup
from spider.logger import LoggerMixin


class Digger(LoggerMixin):
    """
    Base Digger class for extracting product URLs from listing pages.
    Subclasses must implement product_list() method.
    """

    def __init__(self, page):
        """
        Initialize digger with a page object.

        Args:
            page: Page object with 'url' and 'html' attributes
        """
        self.url = page.url
        self.doc = BeautifulSoup(page.html, 'lxml')

    def product_list(self):
        """
        Extract list of product URLs from the page.

        Returns:
            list: List of product URL strings
        """
        raise NotImplementedError("Subclass must implement product_list() method")
