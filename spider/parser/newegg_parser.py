# encoding: utf-8
from spider.parser import Parser
from bs4 import BeautifulSoup
from datetime import datetime
import re


class NeweggParser(Parser):
    """Parser for Newegg product pages"""

    def title(self):
        """Extract product title"""
        elem = self.doc.select_one(".proHeader h1")
        return elem.get_text(strip=True) if elem else None

    def price(self):
        """Extract product price"""
        return None

    def stock(self):
        """Extract stock quantity"""
        elem = self.doc.select_one(".detailList span.lightly")
        if elem:
            text = elem.get_text(strip=True)
            return 1 if text == "有货" else 0
        return 0

    def image_url(self):
        """Extract main product image URL"""
        link = self.doc.select_one("a#bigImg")
        return link.get("href") if link else None

    def price_url(self):
        """Extract price URL (for ajax-loaded prices)"""
        img = self.doc.select_one(".neweggPrice img")
        return img.get("src") if img else None

    def score(self):
        """Extract product score/rating"""
        score_elems = self.doc.select(".score span")
        if score_elems:
            score_text = score_elems[0].get_text(strip=True)
            try:
                return float(score_text)
            except (ValueError, TypeError):
                return 0.0
        return 0.0

    def desc(self):
        """Extract product description"""
        return None

    def standard(self):
        """Extract product standard/specification"""
        elem = self.doc.select_one(".proDescTab table")
        return str(elem) if elem else None

    def product_code(self):
        """Extract product code/SKU (商品代码)"""
        return None

    def comments(self):
        """
        Extract product comments/reviews.

        Returns:
            list: List of comment dicts with keys:
                - title: Comment title
                - content: Comment content
                - publish_at: Publication datetime
                - star: Star rating (float)
        """
        comment_cells = self.doc.select("#comment_1 .listCell")
        comments_list = []

        for elem in comment_cells:
            # Extract title
            title_elem = elem.select_one(".title h2")
            title = title_elem.get_text(strip=True) if title_elem else ""

            # Extract publish date
            publish_at = datetime.now()
            pub_date_elem = elem.select_one(".pubDate")
            if pub_date_elem:
                pub_date_text = pub_date_elem.get_text(strip=True)
                try:
                    # Try to parse date - format may vary
                    publish_at = datetime.strptime(pub_date_text, "%Y-%m-%d")
                except (ValueError, TypeError):
                    try:
                        publish_at = datetime.strptime(pub_date_text, "%Y-%m-%d %H:%M:%S")
                    except (ValueError, TypeError):
                        publish_at = datetime.now()

            # Extract star rating
            star = 0.0
            star_elem = elem.select_one(".rankIcon strong")
            if star_elem:
                star_text = star_elem.get_text(strip=True)
                try:
                    star = float(star_text)
                except (ValueError, TypeError):
                    star = 0.0

            # Extract content from multiple text blocks
            content_blocks = elem.select(".content .textBlock")
            content_parts = [block.get_text(strip=True) for block in content_blocks]
            content = "\n".join(content_parts)

            comments_list.append({
                "title": title,
                "publish_at": publish_at,
                "star": star,
                "content": content
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
        return []
