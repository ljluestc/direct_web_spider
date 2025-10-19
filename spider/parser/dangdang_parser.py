# encoding: utf-8
from spider.parser import Parser
from bs4 import BeautifulSoup
from datetime import datetime
import re


class DangdangParser(Parser):
    """Parser for Dangdang product pages"""

    def title(self):
        """Extract product title"""
        elem = self.doc.select_one("div.dp_wrap h1")
        return elem.get_text(strip=True) if elem else None

    def price(self):
        """Extract product price"""
        elem = self.doc.select_one("#salePriceTag")
        if elem:
            price_text = elem.get_text(strip=True)
            # Remove currency symbol and convert to int
            price_text = price_text.replace("￥", "")
            try:
                return int(float(price_text))
            except (ValueError, TypeError):
                return None
        return None

    def stock(self):
        """Extract stock quantity"""
        # TODO: Stock information is loaded via AJAX
        # http://205.186.156.35:8080/issues/24
        # Stock URL: http://product.dangdang.com/callback.php?type=stock&product_id=1033397102&page_type=mall
        return 1

    def image_url(self):
        """Extract main product image URL"""
        img = self.doc.select_one("#largePic")
        if img:
            return img.get("src")
        # Default fallback image
        return "http://img32.ddimg.cn/7/35/60129142-1_h.jpg"

    def desc(self):
        """Extract product description"""
        return None

    def price_url(self):
        """Extract price URL (for ajax-loaded prices)"""
        return None

    def score(self):
        """Extract product score/rating"""
        # Count red star images
        imgs = self.doc.select("p.fraction img")
        red_stars = [img for img in imgs if img.get("src") and re.search(r'red', img.get("src", ""))]
        return len(red_stars)

    def product_code(self):
        """Extract product code/SKU"""
        return None

    def standard(self):
        """Extract product standard/specification"""
        return None

    def comments(self):
        """
        Extract product comments/reviews.

        Returns:
            list: List of comment dicts with keys:
                - title: Comment title
                - content: Comment content
                - publish_at: Publication datetime
                - star: Star rating (integer)
        """
        title_elems = self.doc.select("#comm_all h5 a")
        content_elems = self.doc.select("#comm_all div.text")
        publish_at_elems = self.doc.select("#comm_all .title .time")
        star_elems = self.doc.select("#comm_all .title .star")

        comments_list = []
        for i in range(len(title_elems)):
            # Extract title
            title = title_elems[i].get_text(strip=True) if i < len(title_elems) else ""

            # Extract content and remove date/time prefix
            content = ""
            if i < len(content_elems):
                content = content_elems[i].get_text(strip=True)
                # Remove leading date/time pattern like "2013-08-15 12:30:45"
                content = re.sub(r'^[\s\d:-]+', '', content)

            # Extract publish date
            publish_at = datetime.now()
            if i < len(publish_at_elems):
                publish_at_text = publish_at_elems[i].get_text(strip=True)
                if publish_at_text:
                    try:
                        # Try to parse various date formats
                        publish_at = datetime.strptime(publish_at_text, "%Y-%m-%d")
                    except (ValueError, TypeError):
                        try:
                            publish_at = datetime.strptime(publish_at_text, "%Y-%m-%d %H:%M:%S")
                        except (ValueError, TypeError):
                            publish_at = datetime.now()

            # Extract star rating by counting red star images
            star = 0
            if i < len(star_elems):
                star_imgs = star_elems[i].select("img")
                red_imgs = [img for img in star_imgs if img.get("src") and re.search(r'red', img.get("src", ""))]
                star = len(red_imgs)

            comments_list.append({
                "title": title,
                "content": content,
                "publish_at": publish_at,
                "star": star
            })

        return comments_list

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
        crumb_links = self.doc.select(".crumb a")
        categories = []
        for elem in crumb_links:
            href = elem.get("href", "")
            if href and re.search(r'list', href):
                categories.append({
                    "name": elem.get_text(strip=True),
                    "url": href
                })
        return categories
