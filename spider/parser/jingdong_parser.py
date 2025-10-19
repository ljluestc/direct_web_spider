# encoding: utf-8
from spider.parser import Parser
from bs4 import BeautifulSoup
from datetime import datetime
import re


class JingdongParser(Parser):
    """Parser for Jingdong (JD.com) product pages"""

    def end_product(self):
        """Extract or find end product reference"""
        return None

    def merchant(self):
        """Extract or find merchant reference"""
        return None

    def brand(self):
        """Extract or find brand reference"""
        return None

    def brand_type(self):
        """Extract or find brand type reference"""
        return None

    def product_code(self):
        """Extract product code/SKU"""
        elem = self.doc.select_one("#summary li:first-child span")
        if elem:
            text = elem.get_text(strip=True)
            # Remove "商品编号：" prefix
            return re.sub(r'商品编号：', '', text)
        return None

    def title(self):
        """Extract product title"""
        elem = self.doc.select_one("div#name h1")
        return elem.get_text(strip=True) if elem else None

    def price(self):
        """Extract product price"""
        return None

    def price_url(self):
        """Extract price URL (for ajax-loaded prices)"""
        img = self.doc.select_one("strong.price img")
        return img.get("src") if img else None

    def stock(self):
        """Extract stock quantity"""
        elem = self.doc.select_one("#stocktext")
        if elem:
            text = elem.get_text(strip=True)
            if re.search(r'发货', text):
                return 1
            if re.search(r'售完', text):
                return 0
        self.logger.info("stock issue!")
        return 0

    def image_url(self):
        """Extract main product image URL"""
        img = self.doc.select_one("#preview img")
        return img.get("src") if img else None

    def score(self):
        """Extract product score/rating"""
        # Find div with id starting with "star"
        star_divs = self.doc.select("div[id^=star]")
        if star_divs:
            first_child = star_divs[0].select_one("div:first-child")
            if first_child:
                class_attr = first_child.get("class", [])
                # class can be a list in BeautifulSoup
                if isinstance(class_attr, list):
                    class_str = " ".join(class_attr)
                else:
                    class_str = class_attr
                # Extract digits from class string
                match = re.search(r'\d+', class_str)
                if match:
                    try:
                        return int(match.group(0))
                    except ValueError:
                        return 0
        return 0

    def standard(self):
        """Extract product standard/specification"""
        elem = self.doc.select_one(".Ptable")
        return str(elem) if elem else None

    def desc(self):
        """Extract product description"""
        elem = self.doc.select_one(".mc.fore.tabcon")
        return str(elem) if elem else None

    def comments(self):
        """
        Extract product comments/reviews.

        Returns:
            list: List of comment dicts
        """
        # Comments URL: http://club.360buy.com/clubservice/productcomment-495087-5-0.html
        # Not implemented - requires separate AJAX request
        return []

    def belongs_to_categories(self):
        """
        Extract category breadcrumb/hierarchy.

        Returns:
            list: List of dicts with 'name' and 'url' keys
        """
        crumb_links = self.doc.select(".crumb a")
        categories = []
        for elem in crumb_links:
            href = elem.get("href", "")
            # Match URLs containing "products" or ending with "com/xxx.html"
            if href and (re.search(r'products', href) or re.search(r'com/\w+\.html$', href)):
                categories.append({
                    "name": elem.get_text(strip=True),
                    "url": href
                })
        return categories
