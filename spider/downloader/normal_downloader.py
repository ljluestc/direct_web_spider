# encoding: utf-8
import requests
from spider.downloader import Downloader
from spider.encoding import Encoding
from spider.utils.utils import Utils


class NormalDownloader(Downloader):
    """
    Single-threaded downloader using requests library.
    Downloads items sequentially one at a time.
    """

    def __init__(self, items):
        """
        Initialize downloader with list of items to download.

        Args:
            items: List of objects with 'url' attribute
        """
        self.items = items

    def run(self, callback):
        """
        Download all items sequentially and call callback for each successful download.

        Args:
            callback: Function to call for each successfully downloaded item
        """
        for item in self.items:
            try:
                response = requests.get(item.url, timeout=30)
                html = response.content

                # Convert encoding to UTF-8
                Encoding.set_utf8_html(item, html)

                # Validate HTML
                if not Utils.valid_html(item.html):
                    self.logger.error(f"{item.__class__.__name__} {item.kind} {item.url} Bad HTML.")
                else:
                    # Call callback with successfully downloaded item
                    callback(item)

            except (requests.Timeout, requests.ConnectionError) as e:
                self.logger.error(f"{item.__class__.__name__} {item.kind} {item.url} HTTP Connection Error: {e}")
            except Exception as e:
                self.logger.error(f"{item.__class__.__name__} {item.kind} {item.url} Error: {e}")
