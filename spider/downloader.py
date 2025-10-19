# encoding: utf-8
from spider.encoding import Encoding
from spider.logger import LoggerMixin


class Downloader(LoggerMixin):
    """
    Base Downloader class for downloading web pages.
    Subclasses must implement run() method.
    """

    def max_concurrency(self):
        """
        Maximum number of concurrent downloads.

        Returns:
            int: Maximum concurrency level (default: 10)
        """
        return 10

    def run(self, callback):
        """
        Run the downloader and execute callback for each successfully downloaded item.

        Args:
            callback: Function to call for each downloaded item
                Signature: callback(item) where item has html attribute set
        """
        raise NotImplementedError("Subclass must implement run() method")
