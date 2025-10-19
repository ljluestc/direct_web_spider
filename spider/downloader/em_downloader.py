# encoding: utf-8
import asyncio
import aiohttp
from spider.downloader import Downloader
from spider.encoding import Encoding
from spider.utils.utils import Utils


class EmDownloader(Downloader):
    """
    Asynchronous event-driven downloader using asyncio and aiohttp.
    Downloads all items concurrently using async/await.
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
        Download all items asynchronously and call callback for each successful download.

        Args:
            callback: Function to call for each successfully downloaded item
        """
        # Run the async event loop
        asyncio.run(self._run_async(callback))

    async def _run_async(self, callback):
        """
        Async implementation of the download loop.

        Args:
            callback: Function to call for each successfully downloaded item
        """
        async with aiohttp.ClientSession() as session:
            # Create all download tasks
            tasks = [self._fetch(session, item, callback) for item in self.items]
            # Wait for all to complete
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _fetch(self, session, item, callback):
        """
        Fetch a single item asynchronously.

        Args:
            session: aiohttp ClientSession
            item: Object with 'url' attribute
            callback: Function to call on success
        """
        try:
            async with session.get(item.url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status == 200:
                    html = await response.read()

                    # Convert encoding to UTF-8
                    Encoding.set_utf8_html(item, html)

                    # Validate HTML
                    if not Utils.valid_html(item.html):
                        self.logger.error(f"{item.__class__.__name__} {item.kind} {item.url} Bad HTML.")
                    else:
                        # Call callback with successfully downloaded item
                        callback(item)
                else:
                    self.logger.error(f"{item.__class__.__name__} {item.kind} {item.url} HTTP {response.status}.")

        except asyncio.TimeoutError:
            self.logger.error(f"{item.__class__.__name__} {item.kind} {item.url} HTTP Connection Timeout.")
        except aiohttp.ClientError as e:
            self.logger.error(f"{item.__class__.__name__} {item.kind} {item.url} HTTP Connection Error: {e}")
        except Exception as e:
            self.logger.error(f"{item.__class__.__name__} {item.kind} {item.url} Error: {e}")
