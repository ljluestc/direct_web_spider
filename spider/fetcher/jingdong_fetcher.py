# encoding: utf-8
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from spider.fetcher import Fetcher


class JingdongFetcher(Fetcher):
    """
    Fetcher for JingDong/360buy (jd.com) e-commerce site
    """
    URL = "http://www.360buy.com/allSort.aspx"
    BASE_URL = "http://www.360buy.com"

    @classmethod
    def category_list(cls):
        """
        Fetch category list from JingDong

        Returns:
            list: List of category dicts with 'name' and 'url' keys
        """
        response = requests.get(cls.URL)
        html = response.content.decode('GB18030', errors='replace')

        doc = BeautifulSoup(html, 'lxml')

        categories = []
        for elem in doc.select('div.mc em a[href^="products"]'):
            categories.append({
                'name': elem.get_text(strip=True),
                'url': urljoin(cls.BASE_URL, elem['href'])
            })

        return categories
