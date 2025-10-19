# encoding: utf-8
from spider.logger import LoggerMixin


class Fetcher(LoggerMixin):
    """
    Base Fetcher class for fetching initial category lists from e-commerce sites.
    Subclasses must implement category_list() class method.
    """

    @classmethod
    def category_list(cls):
        """
        Fetch and return list of categories for the site.

        Returns:
            list: List of dicts with 'name' and 'url' keys
                Example: [{'name': 'Electronics', 'url': 'http://...'}]
        """
        raise NotImplementedError("Subclass must implement category_list() method")
