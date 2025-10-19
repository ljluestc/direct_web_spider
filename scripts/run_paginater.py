#!/usr/bin/env python3
# encoding: utf-8
"""
Spider Paginater Runner
Paginates through category pages and saves individual page URLs to database.
"""

import sys
import os
from pathlib import Path

# Add parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from spider.utils.utils import Utils
from spider.utils.optparse import SpiderOptions
from spider.logger import get_logger
from spider.models.category import Category
from spider.models.page import Page

# Load environment
Utils.load_mongo(SpiderOptions['environment'])
Utils.load_models()
Utils.load_paginater()
Utils.load_downloader()

# Get logger
logger = get_logger(__name__)

# Dynamically load the paginater class
spider_name = SpiderOptions['name']
paginater_module_name = f"{spider_name}_paginater"
paginater_class_name = f"{spider_name.capitalize()}Paginater"

try:
    paginater_module = __import__(f'spider.paginater.{paginater_module_name}', fromlist=[paginater_class_name])
    CurrentPaginater = getattr(paginater_module, paginater_class_name)
except (ImportError, AttributeError) as e:
    logger.error(f"Failed to load paginater for '{spider_name}': {e}")
    print(f"Error: Could not find {paginater_class_name} in spider.paginater.{paginater_module_name}")
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


def start_paginate(category):
    """
    Paginate through a category and save page URLs.

    Args:
        category: Category model instance
    """
    paginater = CurrentPaginater(category)
    for url in paginater.pagination_list():
        page = Page(
            url=url,
            kind=SpiderOptions['name'],
            category_id=category.id
        )
        page.save()

        # Check if saved successfully
        if page.id is not None:
            logger.info(f"Saved Page URL: {url}")

    # Mark category as completed
    category.completed = True
    category.save()

    # Check if category is still persisted
    if category.id is not None:
        logger.info(f"Completed Category URL: {category.url}")


# Get categories to process
# Category.from_kind(kind).leaves.where(completed=false).limit(number)
# In MongoEngine: Category.from_kind(kind) returns a queryset, then we need leaves
# Note: Category.from_kind returns a QuerySet, leaves is a class method that needs to be chained
try:
    # Get all leaf categories (no children) of this kind that are not completed
    all_categories = Category.from_kind(SpiderOptions['name'])

    # Filter for leaf nodes (categories with no children)
    # We need to get leaf categories that are not completed
    categories = []
    for cat in all_categories:
        if cat.is_leaf and not cat.completed:
            categories.append(cat)
            if len(categories) >= SpiderOptions['number']:
                break

    # Run downloader with categories
    downloader = CurrentDownloader(categories)
    downloader.run(start_paginate)

    print(f"Pagination completed for {spider_name}")

except Exception as e:
    logger.error(f"Error during pagination: {e}")
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
