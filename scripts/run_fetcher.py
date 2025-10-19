#!/usr/bin/env python3
# encoding: utf-8
"""
Spider Fetcher Runner
Fetches initial category list from e-commerce sites and saves to database.
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

# Load environment
Utils.load_mongo(SpiderOptions['environment'])
Utils.load_models()
Utils.load_fetcher()

# Get logger
logger = get_logger(__name__)

# Dynamically load the fetcher class based on spider name
# "Spider::#{name}Fetcher".constantize -> dynamic import
spider_name = SpiderOptions['name']
fetcher_module_name = f"{spider_name}_fetcher"
fetcher_class_name = f"{spider_name.capitalize()}Fetcher"

try:
    # Import the specific fetcher module
    fetcher_module = __import__(f'spider.fetcher.{fetcher_module_name}', fromlist=[fetcher_class_name])
    ThisFetcher = getattr(fetcher_module, fetcher_class_name)
except (ImportError, AttributeError) as e:
    logger.error(f"Failed to load fetcher for '{spider_name}': {e}")
    print(f"Error: Could not find {fetcher_class_name} in spider.fetcher.{fetcher_module_name}")
    sys.exit(1)

# Fetch and save categories
try:
    for category in ThisFetcher.category_list():
        # Create category with url, kind, and name
        cat = Category(
            url=category['url'],
            kind=SpiderOptions['name'],
            name=category['name']
        )
        cat.save()

        # Check if saved successfully (id is not None after save)
        if cat.id is not None:
            logger.info(f"Saved URL: {cat.url}")

except Exception as e:
    logger.error(f"Error during fetching: {e}")
    print(f"Error: {e}")
    sys.exit(1)

print(f"Fetching completed for {spider_name}")
