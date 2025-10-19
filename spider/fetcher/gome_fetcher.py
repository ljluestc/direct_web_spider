# encoding: utf-8
import requests
from bs4 import BeautifulSoup
from spider.fetcher import Fetcher


class GomeFetcher(Fetcher):
    """
    Fetcher for Gome (gome.com.cn) e-commerce site
    """
    URL = "http://www.gome.com.cn/allSort.html"

    @classmethod
    def category_list(cls):
        """
        Fetch category list from Gome

        Returns:
            list: List of category dicts with 'name' and 'url' keys
        """
        response = requests.get(cls.URL)
        html = response.content.decode('utf-8', errors='replace')

        doc = BeautifulSoup(html, 'lxml')

        categories = []
        for elem in doc.select('#allsort a'):
            href = elem.get('href', '').strip()
            if 'product' in href:
                categories.append({
                    'name': elem.get_text(strip=True),
                    'url': href
                })

        return categories
