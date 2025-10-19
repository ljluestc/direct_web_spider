# encoding: utf-8
from spider.paginater import Paginater
from bs4 import BeautifulSoup
import re


class DangdangPaginater(Paginater):
    """
    Dangdang pagination handler.
    Extracts max page number from #all_num element and generates paginated URLs.
    """

    def pagination_list(self):
        """
        Generate list of pagination URLs for Dangdang category pages.

        Returns:
            list: List of paginated URLs with &p={page_number} parameter
        """
        # Extract max page number from #all_num element text
        all_num_elem = self.doc.select_one("#all_num")
        if all_num_elem:
            text = all_num_elem.get_text()
            # Extract first number from text
            match = re.search(r'\d+', text)
            max_page = int(match.group(0)) if match else 1
        else:
            max_page = 1

        # Generate URLs with &p={page_number} parameter
        return [f"{self.url}&p={i}" for i in range(1, max_page + 1)]
