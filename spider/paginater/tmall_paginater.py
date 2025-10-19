# encoding: utf-8
from spider.paginater import Paginater
from spider.utils.utils import Utils
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, urlunparse


class TmallPaginater(Paginater):
    """
    Tmall pagination handler.
    Extracts max page number and form action URL, then generates paginated URLs
    by modifying the 's' query parameter.
    """

    def pagination_list(self):
        """
        Generate list of pagination URLs for Tmall category pages.

        Returns:
            list: List of paginated URLs with modified 's' parameter
        """
        # Extract max page from #totalPage input element
        total_page_elem = self.doc.select_one("#totalPage")
        if total_page_elem:
            max_page = int(total_page_elem.get('value', 1))
        else:
            max_page = 1

        # Extract form action URL
        filter_form = self.doc.select_one("#filterPageForm")
        if filter_form:
            first_url = filter_form.get('action', '')
        else:
            first_url = ''

        # Parse URL
        parsed = urlparse(first_url)
        query_hash = Utils.query2hash(parsed.query) if parsed.query else {}

        # Get the 'n' parameter (items per page)
        n_value = int(query_hash.get('n', 0))

        # Generate URLs for each page
        urls = []
        for i in range(1, max_page + 1):
            # Update 's' parameter: s = n * (page - 1)
            updated_hash = query_hash.copy()
            updated_hash['s'] = n_value * (i - 1)

            # Reconstruct URL
            new_query = Utils.hash2query(updated_hash)
            new_parsed = parsed._replace(query=new_query)
            url = urlunparse(new_parsed)
            urls.append(url)

        return urls
