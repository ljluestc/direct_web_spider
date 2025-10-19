# encoding: utf-8
from bs4 import BeautifulSoup
from spider.logger import LoggerMixin


class Paginater(LoggerMixin):
    """
    Base Paginater class for generating pagination URLs from category pages.
    Subclasses must implement pagination_list() method.
    """

    def __init__(self, item):
        """
        Initialize paginater with a category item.

        Args:
            item: Category object with 'url' and 'html' attributes
        """
        self.url = item.url
        self.doc = BeautifulSoup(item.html, 'lxml')

    def pagination_list(self):
        """
        Generate list of pagination URLs for the category.

        Returns:
            list: List of paginated URL strings
        """
        raise NotImplementedError("Subclass must implement pagination_list() method")
