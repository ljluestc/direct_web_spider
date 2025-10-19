#!/usr/bin/env python3
# encoding: utf-8
"""
Spider Digger Runner
Extracts product URLs from page listings and saves to database.
"""

import sys
import os
from pathlib import Path

# Add parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from spider.utils.utils import Utils
from spider.utils.optparse import SpiderOptions
from spider.logger import get_logger
from spider.models.page import Page
from spider.models.product_url import ProductUrl

# Load environment
Utils.load_mongo(SpiderOptions['environment'])
Utils.load_models()
Utils.load_digger()
Utils.load_downloader()

# Get logger
logger = get_logger(__name__)

# Dynamically load the digger class
spider_name = SpiderOptions['name']
digger_module_name = f"{spider_name}_digger"
digger_class_name = f"{spider_name.capitalize()}Digger"

try:
    digger_module = __import__(f'spider.digger.{digger_module_name}', fromlist=[digger_class_name])
    CurrentDigger = getattr(digger_module, digger_class_name)
except (ImportError, AttributeError) as e:
    logger.error(f"Failed to load digger for '{spider_name}': {e}")
    print(f"Error: Could not find {digger_class_name} in spider.digger.{digger_module_name}")
    sys.exit(1)

# Dynamically load the downloader class
downloader_name = SpiderOptions['downloader']
downloader_module_name = f"{downloader_name}_downloader"
downloader_class_name = f"{downloader_name.capitalize()}Downloader"

try:
    downloader_module = __import__(f'spider.downloader.{downloader_module_name}', fromlist=[downloader_class_name])
    CurrentDownloader = getattr(downloader_module, downloader_class_name)
except (ImportError, AttributeError) as e:
    logger.error(f"Failed to load downloader '{downloader_name}': {e}")
    print(f"Error: Could not find {downloader_class_name} in spider.downloader.{downloader_module_name}")
    sys.exit(1)


def start_digg(page):
    """
    Dig product URLs from a page and save them.

    Args:
        page: Page model instance
    """
    digger = CurrentDigger(page)
    for url in digger.product_list():
        product_url = ProductUrl(
            url=url,
            kind=SpiderOptions['name'],
            page_id=page.id
        )
        product_url.save()

        # Check if saved successfully
        if product_url.id is not None:
            logger.info(f"Saved Product URL: {url}")

    # Mark page as completed
    page.completed = True
    page.save()

    # Check if page is still persisted
    if page.id is not None:
        logger.info(f"Completed Page URL: {page.url}")


# Get pages to process
# Page.from_kind(kind).where(completed=false).limit(number)
try:
    pages = Page.from_kind(SpiderOptions['name']).filter(
        completed=False
    ).limit(SpiderOptions['number'])

    # Convert QuerySet to list for downloader
    pages_list = list(pages)

    # Run downloader with pages
    downloader = CurrentDownloader(pages_list)
    downloader.run(start_digg)

    print(f"Digging completed for {spider_name}")

except Exception as e:
    logger.error(f"Error during digging: {e}")
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
