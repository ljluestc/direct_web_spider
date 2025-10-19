# encoding: utf-8
"""
Encoding conversion module for handling different character encodings
from e-commerce sites.
"""


class Encoding:
    """
    Handles character encoding conversion for different e-commerce sites.
    Mimics Ruby's Spider::Encoding module.
    """

    # Encoding map for different sites
    Map = {
        "dangdang": "GB18030",
        "jingdong": "GB18030",
        "newegg": "GB18030",
        "tmall": "GB18030",
        "suning": "UTF-8",
        "gome": "UTF-8"
    }

    @staticmethod
    def set_utf8_html(item, html):
        """
        Convert HTML from origin encoding to UTF-8 and set it on the item.

        Args:
            item: Object with 'kind' attribute and 'html' attribute to set
            html: Raw HTML bytes or string

        Returns:
            The item with html attribute set to UTF-8 string
        """
        origin_encoding = Encoding.Map.get(item.kind, "UTF-8")

        # Handle both bytes and string input
        if isinstance(html, bytes):
            # Decode bytes to UTF-8 string, replacing invalid characters
            try:
                item.html = html.decode(origin_encoding, errors='replace')
            except (LookupError, UnicodeDecodeError):
                # Fallback to UTF-8 if origin encoding fails
                item.html = html.decode('utf-8', errors='replace')
        else:
            # Already a string
            item.html = html

        # Replace undefined characters with "?"
        item.html = item.html.replace('\ufffd', '?')

        return item
