# encoding: utf-8
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from spider.downloader import Downloader
from spider.encoding import Encoding
from spider.utils.utils import Utils


class TyDownloader(Downloader):
    """
    Multi-threaded downloader using ThreadPoolExecutor.
    Downloads multiple items concurrently.
    """

    def __init__(self, items):
        """
        Initialize downloader with list of items to download.

        Args:
            items: List of objects with 'url' attribute
        """
        self.items = items
        self.max_workers = 20  # Matches Ruby's max_concurrency

    def run(self, callback):
        """
        Download all items concurrently using thread pool and call callback for each.

        Args:
            callback: Function to call for each successfully downloaded item
        """
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all download tasks
            future_to_item = {executor.submit(self._fetch, item): item for item in self.items}

            # Process completed downloads
            for future in as_completed(future_to_item):
                item = future_to_item[future]
                try:
                    success = future.result()
                    if success:
                        callback(item)
                except Exception as e:
                    self.logger.error(f"Error processing {item.url}: {e}")

    def _fetch(self, item):
        """
        Fetch a single item (executed in thread pool).

        Args:
            item: Object with 'url' attribute

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            response = requests.get(item.url, timeout=30)

            if response.status_code == 200:
                html = response.content

                # Convert encoding to UTF-8
                Encoding.set_utf8_html(item, html)

                # Validate HTML
                if not Utils.valid_html(item.html):
                    self.logger.error(f"{item.__class__.__name__} {item.kind} {item.url} Bad HTML.")
                    return False
                else:
                    return True
            else:
                self.logger.error(f"{item.__class__.__name__} {item.kind} {item.url} HTTP {response.status_code}.")
                return False

        except (requests.Timeout, requests.ConnectionError) as e:
            self.logger.error(f"{item.__class__.__name__} {item.kind} {item.url} HTTP Connection Error: {e}")
            return False
        except Exception as e:
            self.logger.error(f"{item.__class__.__name__} {item.kind} {item.url} Error: {e}")
            return False
