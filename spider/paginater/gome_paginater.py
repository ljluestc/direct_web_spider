# encoding: utf-8
from spider.paginater import Paginater
from bs4 import BeautifulSoup
import re


class GomePaginater(Paginater):
    """
    Gome pagination handler.
    Extracts parameters from URL and generates paginated search URLs.
    """

    def pagination_list(self):
        """
        Generate list of pagination URLs for Gome category pages.

        Returns:
            list: List of paginated search URLs with p parameter
        """
        # Parse URL info
        info = self._parse_url_info()

        # Extract max page from .thispage element
        thispage_elem = self.doc.select_one(".thispage")
        if thispage_elem:
            text = thispage_elem.get_text()
            # Split by '/' and get last part
            parts = text.split('/')
            max_page = int(parts[-1]) if parts else 1
        else:
            max_page = 1

        # Generate URLs
        urls = []
        for i in range(1, max_page + 1):
            # Update info dict with page number
            params = info.copy()
            params['p'] = i

            # Build query string
            query_parts = [f"{key}={value}" for key, value in params.items()]
            query_string = "&".join(query_parts)

            url = f"http://search.gome.com.cn/product.do?{query_string}"
            urls.append(url)

        return urls

    def _parse_url_info(self):
        """
        Parse URL to extract Gome-specific parameters.

        Returns:
            dict: Dictionary of URL parameters
        """
        # Extract all numbers from URL using regex
        numbers = re.findall(r'\d+', self.url)

        return {
            'topCtgyId': numbers[0] if len(numbers) > 0 else '',
            'ctgyId': numbers[1] if len(numbers) > 1 else '',
            'order': 3,
            'ctgLevel': numbers[2] if len(numbers) > 2 else '',
            'scopes': ''
        }
