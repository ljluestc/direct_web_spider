# encoding: utf-8
import requests
from bs4 import BeautifulSoup
from spider.fetcher import Fetcher


class NeweggFetcher(Fetcher):
    """
    Fetcher for Newegg China (newegg.com.cn) e-commerce site
    """
    URL = "http://www.newegg.com.cn/CategoryList.htm"

    @classmethod
    def category_list(cls):
        """
        Fetch category list from Newegg

        Returns:
            list: List of category dicts with 'name' and 'url' keys
        """
        response = requests.get(cls.URL)
        html = response.content.decode('utf-8', errors='replace')

        doc = BeautifulSoup(html, 'lxml')

        categories = []
        for elem in doc.select('.allCateList dd a'):
            categories.append({
                'url': elem.get('href', ''),
                'name': elem.get_text(strip=True)
            })

        return categories
