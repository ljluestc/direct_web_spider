# encoding: utf-8
from spider.parser import Parser
from bs4 import BeautifulSoup
from datetime import datetime
import re


class SuningParser(Parser):
    """Parser for Suning product pages"""

    def title(self):
        """Extract product title"""
        elem = self.doc.select_one(".product_title_name")
        return elem.get_text(strip=True) if elem else None

    def price(self):
        """Extract product price"""
        return None

    def stock(self):
        """Extract stock quantity"""
        elem = self.doc.select_one("#deleverStatus")
        if elem:
            text = elem.get_text(strip=True)
            return 1 if re.search(r'现货', text) else 0
        return 0

    def image_url(self):
        """Extract main product image URL"""
        img = self.doc.select_one(".product_b_image img")
        return img.get("src") if img else None

    def desc(self):
        """Extract product description"""
        return None

    def price_url(self):
        """Extract price URL (for ajax-loaded prices)"""
        return None

    def score(self):
        """Extract product score/rating"""
        # Count stars by subtracting empty stars from 5
        noscore_elems = self.doc.select(".sn_stars em.noscore")
        return 5 - len(noscore_elems)

    def product_code(self):
        """Extract product code/SKU"""
        elem = self.doc.select_one(".product_title_cout")
        if elem:
            text = elem.get_text(strip=True)
            # Extract first sequence of digits
            match = re.search(r'\d+', text)
            if match:
                try:
                    return int(match.group(0))
                except ValueError:
                    return None
        return None

    def standard(self):
        """Extract product standard/specification"""
        return ""

    def comments(self):
        """
        Extract product comments/reviews.

        Returns:
            list: List of comment dicts
        """
        return []

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

    def belongs_to_categories(self):
        """
        Extract category breadcrumb/hierarchy.

        Returns:
            list: List of dicts with 'name' and 'url' keys
        """
        path_links = self.doc.select(".path a")
        categories = []
        for elem in path_links:
            href = elem.get("href", "")
            # Match URLs containing "html"
            if href and re.search(r'html', href):
                categories.append({
                    "name": elem.get_text(strip=True),
                    "url": href
                })
        return categories
