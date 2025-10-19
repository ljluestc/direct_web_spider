# encoding: utf-8
from spider.digger import Digger
from bs4 import BeautifulSoup


class DangdangDigger(Digger):
    def product_list(self):
        """
        Extract product URLs from Dangdang listing page.

        Returns:
            list: List of product URL strings
        """
        elements = self.doc.select(".mode_goods div.name a")
        return [elem.get("href") for elem in elements if elem.get("href")]
