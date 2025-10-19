# encoding: utf-8
from spider.digger import Digger
from bs4 import BeautifulSoup


class JingdongDigger(Digger):
    def product_list(self):
        """
        Extract product URLs from Jingdong listing page.

        Returns:
            list: List of product URL strings
        """
        elements = self.doc.select("#plist ul.list-h div.p-img a")
        return [elem.get("href") for elem in elements if elem.get("href")]
