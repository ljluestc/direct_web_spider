# encoding: utf-8
from spider.paginater import Paginater
from bs4 import BeautifulSoup
import re


class NeweggPaginater(Paginater):
    """
    Newegg pagination handler.
    Extracts max page number from .pageNav links and generates paginated URLs.
    """

    def pagination_list(self):
        """
        Generate list of pagination URLs for Newegg category pages.

        Returns:
            list: List of paginated URLs with -{page_number}.htm suffix
        """
        # Extract max page number from .pageNav a/* elements (all children)
        page_numbers = []
        nav_links = self.doc.select(".pageNav a")
        for link in nav_links:
            # Get all text from children
            for child in link.descendants:
                if isinstance(child, str):
                    text = child.strip()
                    # Try to convert to integer
                    try:
                        page_num = int(text)
                        page_numbers.append(page_num)
                    except ValueError:
                        continue

        max_page = max(page_numbers) if page_numbers else 1

        # Generate URLs by replacing .htm with -{page}.htm
        urls = []
        for i in range(1, max_page + 1):
            url = self.url.replace(".htm", f"-{i}.htm")
            urls.append(url)

        return urls
