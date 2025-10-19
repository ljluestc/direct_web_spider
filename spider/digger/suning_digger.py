# encoding: utf-8
from spider.digger import Digger
from bs4 import BeautifulSoup


class SuningDigger(Digger):
    def product_list(self):
        """
        Extract product URLs from Suning listing page.

        Returns:
            list: List of product URL strings
        """
        base_url = "http://www.suning.com"
        elements = self.doc.select("#product_container li .pro_img a")
        return [base_url + elem.get("href") for elem in elements if elem.get("href")]
