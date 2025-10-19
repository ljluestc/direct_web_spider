# encoding: utf-8
from spider.paginater import Paginater
from bs4 import BeautifulSoup
import re


class SuningPaginater(Paginater):
    """
    Suning pagination handler.
    Extracts parameters from URL and generates paginated search URLs.
    """

    def pagination_list(self):
        """
        Generate list of pagination URLs for Suning category pages.

        Returns:
            list: List of paginated search URLs with currentPage parameter
        """
        # Parse URL info
        info = self._parse_url_info()

        # Build base URL
        base_url = (
            f"http://www.suning.com/webapp/wcs/stores/servlet/odeSearch?"
            f"storeId={info['store_id']}&"
            f"catalogId={info['catalog_id']}&"
            f"categoryId={info['category_id']}&"
            f"suggestionWordList={info['suggestion_list']}&"
            f"isCatalogSearch={info['is_catalog_search']}"
        )

        # Extract max page from #pagetop span element
        pagetop_span = self.doc.select_one("#pagetop span")
        if pagetop_span:
            text = pagetop_span.get_text()
            # Split by '/' and get last part
            parts = text.split('/')
            max_page = int(parts[-1]) if parts else 1
        else:
            max_page = 1

        # Generate URLs with currentPage parameter (0-indexed)
        urls = []
        for i in range(1, max_page + 1):
            url = f"{base_url}&currentPage={i - 1}"
            urls.append(url)

        return urls

    def _parse_url_info(self):
        """
        Parse URL to extract Suning-specific parameters.

        Returns:
            dict: Dictionary of URL parameters
        """
        # Remove .html suffix and split by underscore (not followed by word boundary)
        url_cleaned = re.sub(r'\.html$', '', self.url)
        # Split by underscore that's not at word boundaries
        url_info = re.split(r'_(?!\b)', url_cleaned)

        # Extract parameters based on position
        return {
            'store_id': url_info[1] if len(url_info) > 1 else '',
            'catalog_id': url_info[2] if len(url_info) > 2 else '',
            'category_id': url_info[4] if len(url_info) > 4 else '',
            'suggestion_list': '',
            'lang_id': -7,
            'is_catalog_search': url_info[3] if len(url_info) > 3 else ''
        }
