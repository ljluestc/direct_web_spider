# encoding: utf-8
from spider.paginater import Paginater
from bs4 import BeautifulSoup
import re


class JingdongPaginater(Paginater):
    """
    Jingdong (JD.com) pagination handler.
    Extracts max page number from pagination div and generates paginated URLs.
    """

    def pagination_list(self):
        """
        Generate list of pagination URLs for Jingdong category pages.

        Returns:
            list: List of paginated URLs with modified .html suffix
        """
        # Extract max page number from div.pagin a elements
        page_numbers = []
        pagin_links = self.doc.select("div.pagin a")
        for elem in pagin_links:
            text = elem.get_text().strip()
            # Try to convert to integer
            try:
                page_num = int(text)
                page_numbers.append(page_num)
            except ValueError:
                continue

        max_page = max(page_numbers) if page_numbers else 1

        # Generate URLs by replacing .html with modified suffix
        # Format: -0-0-0-0-0-0-0-1-1-{page}.html
        urls = []
        for i in range(1, max_page + 1):
            url = self.url.replace(".html", f"-0-0-0-0-0-0-0-1-1-{i}.html")
            urls.append(url)

        return urls
