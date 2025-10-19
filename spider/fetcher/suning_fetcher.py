# encoding: utf-8
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from spider.fetcher import Fetcher


class SuningFetcher(Fetcher):
    """
    Fetcher for Suning (suning.com) e-commerce site
    """
    URL = "http://www.suning.com/webapp/wcs/stores/servlet/SNProductCatgroupView?storeId=10052&catalogId=10051&flag=1"
    BASE_URL = "http://www.suning.com"

    @classmethod
    def category_list(cls):
        """
        Fetch category list from Suning

        Returns:
            list: List of category dicts with 'name' and 'url' keys
        """
        response = requests.get(cls.URL)
        html = response.content.decode('utf-8', errors='replace')

        doc = BeautifulSoup(html, 'lxml')

        categories = []
        for elem in doc.select('.contentmain .allProContent .cont-left a'):
            categories.append({
                'name': elem.get_text(strip=True),
                'url': urljoin(cls.BASE_URL, elem.get('href', ''))
            })

        return categories
