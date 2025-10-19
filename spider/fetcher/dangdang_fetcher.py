# encoding: utf-8
import requests
import json
import re
from spider.fetcher import Fetcher


class DangdangFetcher(Fetcher):
    """
    Fetcher for Dangdang (dangdang.com) e-commerce site
    """
    URL = "http://www.dangdang.com/Found/category.js"

    @classmethod
    def category_list(cls):
        """
        Fetch category list from Dangdang

        Returns:
            list: List of category dicts with 'name' and 'url' keys
        """
        response = requests.get(cls.URL)
        html = response.content.decode('utf-8', errors='replace')

        # Extract JSON data from JavaScript
        match = re.search(r'json_category=(.*?)menudataloaded', html, re.DOTALL)
        if not match:
            raise Exception("当当网页面结构改变了！")

        json_data = match.group(1)
        data = json.loads(json_data)

        categories = []
        for item in data.values():
            url = "http://" + item["u"].replace("#dd#", ".dangdang.com/")
            if "list?cat" in url:
                categories.append({
                    'name': item["n"],
                    'url': url
                })

        return categories
