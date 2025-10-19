#!/usr/bin/env python3
# encoding: utf-8
"""
Spider Parser Runner
Parses product pages and extracts product information, saving to database.
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
from spider.models.product_url import ProductUrl
from spider.models.product import Product

# Load environment
Utils.load_mongo(SpiderOptions['environment'])
Utils.load_models()
Utils.load_redis(SpiderOptions['environment'])
Utils.load_parser()
Utils.load_downloader()

# Get logger
logger = get_logger(__name__)

# Dynamically load the parser class
spider_name = SpiderOptions['name']
parser_module_name = f"{spider_name}_parser"
parser_class_name = f"{spider_name.capitalize()}Parser"

try:
    parser_module = __import__(f'spider.parser.{parser_module_name}', fromlist=[parser_class_name])
    CurrentParser = getattr(parser_module, parser_class_name)
except (ImportError, AttributeError) as e:
    logger.error(f"Failed to load parser for '{spider_name}': {e}")
    print(f"Error: Could not find {parser_class_name} in spider.parser.{parser_module_name}")
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


def assoc_category(category_list, kind):
    """
    Associate categories with parent-child relationships.

    Args:
        category_list: List of dicts with 'name' and 'url' keys
        kind: Spider kind/name

    Returns:
        list: List of Category model instances
    """
    cate_list = []
    for name_and_url in category_list:
        # Merge the dict with kind
        category_data = {**name_and_url, 'kind': kind}

        # Find or create category
        # In Ruby: Category.find_or_create_by(name_and_url.merge(:kind => kind))
        # In Python/MongoEngine: Use get_or_create or similar pattern
        existing = Category.objects(
            url=category_data['url'],
            kind=kind
        ).first()

        if existing:
            cat = existing
        else:
            cat = Category(**category_data)
            cat.save()

        cate_list.append(cat)

    set_assoc(cate_list)
    return cate_list


def set_assoc(cate_list):
    """
    Set parent-child associations for a list of categories.
    Each category's parent is the previous one in the list.

    Args:
        cate_list: List of Category model instances
    """
    # Ruby's each_cons(2) creates pairs: [a,b,c,d] -> [[a,b], [b,c], [c,d]]
    for i in range(len(cate_list) - 1):
        parent = cate_list[i]
        child = cate_list[i + 1]

        child.parent = parent
        child.save()


def start_parse(product_url):
    """
    Parse a product URL and save product information.

    Args:
        product_url: ProductUrl model instance
    """
    try:
        parser = CurrentParser(product_url)

        # Associate categories from parser
        assoc_category(parser.belongs_to_categories(), SpiderOptions['name'])

        # Get product attributes from parser
        product_attrs = parser.attributes()

        # Create product
        product = Product(**product_attrs)
        product.save()

        # Check if saved successfully (product.persisted? in Ruby)
        if product.id is not None:
            logger.info(f"Parsed Product URL: {product_url.url}")
            # Mark product_url as completed
            product_url.completed = True
            product_url.save()

    except Exception as e:
        logger.error(f"Error parsing {product_url.url}: {e}")
        # Don't mark as completed if parsing failed


# Get product URLs to process
# ProductUrl.from_kind(kind).where(completed=false).limit(number)
try:
    product_urls = ProductUrl.from_kind(SpiderOptions['name']).filter(
        completed=False
    ).limit(SpiderOptions['number'])

    # Convert QuerySet to list for downloader
    product_urls_list = list(product_urls)

    # Run downloader with product URLs
    downloader = CurrentDownloader(product_urls_list)
    downloader.run(start_parse)

    print(f"Parsing completed for {spider_name}")

except Exception as e:
    logger.error(f"Error during parsing: {e}")
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
