# encoding: utf-8
from spider.digger import Digger
from bs4 import BeautifulSoup


class NeweggDigger(Digger):
    def product_list(self):
        """
        Extract product URLs from Newegg listing page.

        Returns:
            list: List of product URL strings
        """
        elements = self.doc.select("#itemGrid1 div.itemCell dt a")
        return [elem.get("href") for elem in elements if elem.get("href")]
