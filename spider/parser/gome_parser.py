# encoding: utf-8
from spider.parser import Parser
from bs4 import BeautifulSoup
from datetime import datetime
import re


class GomeParser(Parser):
    """Parser for Gome product pages"""

    def title(self):
        """Extract product title"""
        elem = self.doc.select_one("#name")
        if elem:
            # Strip whitespace like Ruby's .strip
            return elem.get_text(strip=True)
        return None

    def price(self):
        """Extract product price"""
        return None

    def stock(self):
        """Extract stock quantity"""
        return 1

    def image_url(self):
        """Extract main product image URL"""
        img = self.doc.select_one(".p_img_bar img")
        return img.get("src") if img else None

    def desc(self):
        """Extract product description"""
        elem = self.doc.select_one(".description")
        # Return HTML content (inner_html equivalent)
        return elem.decode_contents() if elem else None

    def price_url(self):
        """Extract price URL (for ajax-loaded prices)"""
        img = self.doc.select_one("#gomeprice img")
        return img.get("src") if img else None

    def score(self):
        """Extract product score/rating"""
        elem = self.doc.select_one("#positive div.star")
        if elem:
            class_attr = elem.get("class", [])
            # class can be a list in BeautifulSoup
            if isinstance(class_attr, list):
                class_str = " ".join(class_attr)
            else:
                class_str = class_attr
            # Extract first sequence of digits
            match = re.search(r'\d+', class_str)
            if match:
                try:
                    return int(match.group(0))
                except ValueError:
                    return 0
        return 0

    def product_code(self):
        """Extract product code/SKU"""
        elem = self.doc.select_one("#sku")
        return elem.get_text(strip=True) if elem else None

    def standard(self):
        """Extract product standard/specification"""
        elem = self.doc.select_one(".Ptable")
        # Return HTML content (inner_html equivalent)
        return elem.decode_contents() if elem else None

    def comments(self):
        """
        Extract product comments/reviews.

        Returns:
            list: List of comment dicts
        """
        # Comments URL: http://www.gome.com.cn/appraise/getAppraise.do
        # Requires separate AJAX request
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
        nav_links = self.doc.select("#navigation a")
        categories = []
        for elem in nav_links:
            href = elem.get("href")
            # Filter out links containing "index" or "brand"
            if href and not re.search(r'index|brand', href):
                # Replace ".." with full domain path
                url = href.replace("..", "http://www.gome.com.cn")
                categories.append({
                    "name": elem.get_text(strip=True),
                    "url": url
                })
        return categories
