# Product Requirements Document: Ruby to Python Conversion
## Direct Web Spider Framework

**Version:** 1.0
**Date:** 2025-10-16
**Status:** Implementation Ready

---

## Executive Summary

This PRD outlines the complete conversion of the Direct Web Spider framework from Ruby to Python. The framework is a directed web scraping system designed to extract product information from major Chinese e-commerce platforms (Dangdang, JingDong, Tmall, Newegg, Suning, and Gome).

---

## Project Overview

### Current State (Ruby Implementation)
- **Language:** Ruby 1.9.2+
- **Total Files:** 45 Ruby files
- **Dependencies:** Mongoid, Nokogiri, Typhoeus, EventMachine, Tesseract
- **Database:** MongoDB
- **Architecture:** 4-stage pipeline (Fetcher → Paginater → Digger → Parser)

### Target State (Python Implementation)
- **Language:** Python 3.8+
- **Dependencies:** PyMongo/MongoEngine, lxml/BeautifulSoup4, requests/httpx, asyncio, pytesseract
- **Database:** MongoDB (unchanged)
- **Architecture:** Maintain identical 4-stage pipeline with same logic flow

---

## Architecture Overview

### Core Components

#### 1. **Fetcher Stage**
- **Purpose:** Fetch initial category list from e-commerce sites
- **Input:** Website URL
- **Output:** Category records in MongoDB with URLs
- **Implementation:** 6 site-specific fetchers + 1 base class

#### 2. **Paginater Stage**
- **Purpose:** Generate pagination URLs for each category
- **Input:** Category records
- **Output:** Page records with pagination URLs
- **Implementation:** 6 site-specific paginaters + 1 base class

#### 3. **Digger Stage**
- **Purpose:** Extract product URLs from listing pages
- **Input:** Page records
- **Output:** ProductUrl records
- **Implementation:** 6 site-specific diggers + 1 base class

#### 4. **Parser Stage**
- **Purpose:** Parse product details from product pages
- **Input:** ProductUrl records
- **Output:** Product records with full details
- **Implementation:** 6 site-specific parsers + 1 base class

### Supporting Components

#### 5. **Downloader System**
- **Types:**
  - **NormalDownloader:** Single-threaded HTTP requests
  - **TyDownloader:** Multi-threaded concurrent requests (Typhoeus)
  - **EmDownloader:** Event-driven async requests (EventMachine)
- **Python Equivalent:**
  - **NormalDownloader:** `urllib` or `requests`
  - **TyDownloader:** `concurrent.futures.ThreadPoolExecutor` + `requests`
  - **EmDownloader:** `asyncio` + `aiohttp`

#### 6. **Models (MongoDB Documents)**
- Category (with tree structure)
- Page
- ProductUrl
- Product
- Brand
- BrandType
- Merchant
- EndProduct
- MiddleProduct
- TopProduct
- Comment (embedded in Product)
- Body

#### 7. **Utilities**
- **Logger:** Custom logging per module
- **Encoding:** Character encoding conversion (GB18030/UTF-8)
- **Utils:** Helper functions, module loading
- **Optparse:** Command-line argument parsing

---

## Detailed Component Specifications

### 1. Core Module: Logger (`logger.py`)

**Ruby Implementation:**
```ruby
module Spider::Logger
  def logger_file
    # Dynamic log file based on class name
  end

  def logger
    @logger ||= ::Logger.new(self.logger_file)
  end
end
```

**Python Requirements:**
- Create `spider/logger.py` module
- Implement as mixin class or decorator
- Use Python's `logging` module
- Dynamic log file naming based on class name
- Log format: `[YYYY-MM-DD HH:MM:SS] LEVEL: message`
- Log directory: `log/`

### 2. Core Module: Encoding (`encoding.py`)

**Ruby Implementation:**
```ruby
module Spider::Encoding
  Map = {
    "dangdang" => "GB18030",
    "jingdong" => "GB18030",
    # ...
  }

  def self.set_utf8_html(item, html)
    origin_encoding = Map[item.kind]
    item.html = html.force_encoding(origin_encoding).encode("UTF-8")
  end
end
```

**Python Requirements:**
- Encoding map dictionary
- Method to convert bytes to UTF-8 with proper error handling
- Handle `undef` and `invalid` characters (replace with "?")
- Set HTML attribute on item object

### 3. Core Module: Utils (`utils/utils.py`)

**Functions Required:**
- `valid_html(html)`: Validate HTML completeness (regex check)
- `query2hash(query_str)`: Parse query string to dict
- `hash2query(hash)`: Convert dict to query string
- `decompress_gzip(string)`: Decompress gzip data
- `load_models()`: Load all model classes
- `load_mongo(environment)`: Initialize MongoDB connection
- `load_fetcher()`: Import fetcher module
- `load_parser()`: Import parser module
- `load_digger()`: Import digger module
- `load_paginater()`: Import paginater module
- `load_downloader()`: Import downloader module

### 4. Command-Line Parser (`utils/optparse.py`)

**Ruby Implementation:**
```ruby
SpiderOptions = {
  :name => "dangdang",
  :environment => "development",
  :downloader => "normal",
  :number => 1000
}
```

**Python Requirements:**
- Use `argparse` module
- Arguments:
  - `-s/--name`: Spider name (default: dangdang)
  - `-e/--environment`: Environment (default: development)
  - `-d/--downloader`: Downloader type (default: normal)
  - `-n/--number`: Records to process (default: 1000)
  - `-h/--help`: Help message
- Create `SpiderOptions` global dict

### 5. MongoDB Models

#### Base Model Pattern
All models use MongoEngine ODM with:
- `id` field (auto ObjectId)
- `created_at` timestamp
- `updated_at` timestamp
- Scopes/class methods
- Relationships

#### Category Model (`models/category.py`)
```python
class Category(Document):
    url = StringField(required=True, unique=True)
    completed = BooleanField(default=False)
    name = StringField()
    kind = StringField()
    retry_time = IntField(default=0)
    parent_id = ObjectIdField()

    # Tree structure (Mongoid::Tree equivalent)
    # Use custom tree implementation or library

    # Relationships
    pages = ListField(ReferenceField('Page'))

    @classmethod
    def from_kind(cls, kind):
        return cls.objects(kind=kind)
```

#### Page Model (`models/page.py`)
```python
class Page(Document):
    url = StringField(required=True, unique=True)
    completed = BooleanField(default=False)
    kind = StringField()
    retry_time = IntField(default=0)
    category_id = ObjectIdField()

    # Virtual attribute (not stored)
    html = None

    # Relationships
    category = ReferenceField('Category')
    product_urls = ListField(ReferenceField('ProductUrl'))

    @classmethod
    def from_kind(cls, kind):
        return cls.objects(kind=kind)
```

#### ProductUrl Model (`models/product_url.py`)
Similar structure to Page

#### Product Model (`models/product.py`)
```python
class Product(Document):
    price = DecimalField(precision=2)
    price_url = StringField()
    title = StringField()
    stock = IntField()
    kind = StringField()
    image_url = StringField()
    desc = StringField()
    image_info = ListField()
    score = IntField()
    standard = StringField()
    product_code = StringField()
    product_url_id = ObjectIdField()

    # Relationships
    product_url = ReferenceField('ProductUrl')
    merchant = ReferenceField('Merchant')
    brand = ReferenceField('Brand')
    end_product = ReferenceField('EndProduct')
    brand_type = ReferenceField('BrandType')

    # Embedded documents
    comments = EmbeddedDocumentListField('Comment')
```

#### Comment Model (`models/comment.py`)
```python
class Comment(EmbeddedDocument):
    title = StringField()
    content = StringField()
    publish_at = DateTimeField()
    star = IntField()
```

#### Other Models
- Brand, BrandType, Merchant, EndProduct, MiddleProduct, TopProduct, Body

### 6. Base Classes

#### Fetcher Base (`fetcher.py`)
```python
from spider.logger import LoggerMixin

class Fetcher(LoggerMixin):
    @classmethod
    def category_list(cls):
        """Return list of category dicts with 'name' and 'url' keys"""
        raise NotImplementedError("Subclass must implement category_list")
```

#### Parser Base (`parser.py`)
```python
class Parser(LoggerMixin):
    def __init__(self, product):
        self.product = product
        self.doc = BeautifulSoup(product.html, 'lxml')

    def attributes(self):
        """Return dict of product attributes"""
        return {
            'kind': self.product.kind,
            'title': self.title(),
            'product_code': self.product_code(),
            'price': self.price(),
            'price_url': self.price_url(),
            'stock': self.stock(),
            'image_url': self.image_url(),
            'score': self.score(),
            'desc': self.desc(),
            'standard': self.standard(),
            'comments': self.comments(),
            'end_product': self.end_product(),
            'merchant': self.merchant(),
            'brand': self.brand(),
            'brand_type': self.brand_type(),
            'product_url_id': self.product.id
        }

    # Abstract methods
    def title(self): raise NotImplementedError()
    def price(self): raise NotImplementedError()
    # ... etc
```

#### Digger Base (`digger.py`)
```python
class Digger(LoggerMixin):
    def __init__(self, page):
        self.url = page.url
        self.doc = BeautifulSoup(page.html, 'lxml')

    def product_list(self):
        """Return list of product URLs"""
        raise NotImplementedError()
```

#### Paginater Base (`paginater.py`)
```python
class Paginater(LoggerMixin):
    def __init__(self, item):
        self.url = item.url
        self.doc = BeautifulSoup(item.html, 'lxml')

    def pagination_list(self):
        """Return list of pagination URLs"""
        raise NotImplementedError()
```

#### Downloader Base (`downloader.py`)
```python
class Downloader(LoggerMixin):
    def max_concurrency(self):
        return 10

    def run(self, callback):
        """Run downloader with callback for each item"""
        raise NotImplementedError()
```

### 7. Downloader Implementations

#### NormalDownloader (`downloader/normal_downloader.py`)
```python
import requests
from spider.encoding import Encoding
from spider.utils import Utils

class NormalDownloader(Downloader):
    def __init__(self, items):
        self.items = items

    def run(self, callback):
        for item in self.items:
            try:
                response = requests.get(item.url, timeout=30)
                html = response.content
                Encoding.set_utf8_html(item, html)
                if Utils.valid_html(item.html):
                    callback(item)
                else:
                    self.logger.error(f"{item.__class__} {item.kind} {item.url} Bad HTML.")
            except (requests.Timeout, requests.ConnectionError) as e:
                self.logger.error(f"{item.__class__} {item.kind} {item.url} HTTP Connection Error.")
```

#### TyDownloader (`downloader/ty_downloader.py`)
```python
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

class TyDownloader(Downloader):
    def __init__(self, items):
        self.items = items
        self.max_workers = 20

    def run(self, callback):
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self._fetch, item): item for item in self.items}
            for future in as_completed(futures):
                item = futures[future]
                try:
                    result = future.result()
                    if result:
                        callback(item)
                except Exception as e:
                    self.logger.error(f"Error processing {item.url}: {e}")

    def _fetch(self, item):
        try:
            response = requests.get(item.url, timeout=30)
            Encoding.set_utf8_html(item, response.content)
            if Utils.valid_html(item.html):
                return True
            else:
                self.logger.error(f"{item.__class__} {item.kind} {item.url} Bad HTML.")
                return False
        except Exception as e:
            self.logger.error(f"{item.__class__} {item.kind} {item.url} HTTP Connection Error.")
            return False
```

#### EmDownloader (`downloader/em_downloader.py`)
```python
import asyncio
import aiohttp

class EmDownloader(Downloader):
    def __init__(self, items):
        self.items = items

    def run(self, callback):
        asyncio.run(self._run_async(callback))

    async def _run_async(self, callback):
        async with aiohttp.ClientSession() as session:
            tasks = [self._fetch(session, item, callback) for item in self.items]
            await asyncio.gather(*tasks)

    async def _fetch(self, session, item, callback):
        try:
            async with session.get(item.url, timeout=30) as response:
                html = await response.read()
                Encoding.set_utf8_html(item, html)
                if Utils.valid_html(item.html):
                    callback(item)
                else:
                    self.logger.error(f"{item.__class__} {item.kind} {item.url} Bad HTML.")
        except Exception as e:
            self.logger.error(f"{item.__class__} {item.kind} {item.url} HTTP Connection Error.")
```

### 8. Site-Specific Implementations

#### Dangdang Fetcher Example (`fetcher/dangdang_fetcher.py`)
```python
import requests
import json

class DangdangFetcher(Fetcher):
    URL = "http://www.dangdang.com/Found/category.js"

    @classmethod
    def category_list(cls):
        response = requests.get(cls.URL)
        html = response.content.decode('utf-8', errors='replace')

        # Extract JSON
        import re
        match = re.search(r'json_category=(.*?)menudataloaded', html, re.DOTALL)
        if not match:
            raise Exception("当当网页面结构改变了！")

        json_data = match.group(1)
        data = json.loads(json_data)

        categories = []
        for item in data.values():
            url = "http://" + item["u"].replace("#dd#", ".dangdang.com/")
            if "list?cat" in url:
                categories.append({
                    'name': item["n"],
                    'url': url
                })

        return categories
```

#### Dangdang Parser Example (`parser/dangdang_parser.py`)
```python
from bs4 import BeautifulSoup
from datetime import datetime

class DangdangParser(Parser):
    def title(self):
        elem = self.doc.select_one("div.dp_wrap h1")
        return elem.get_text(strip=True) if elem else ""

    def price(self):
        elem = self.doc.select_one("#salePriceTag")
        if elem:
            price_text = elem.get_text(strip=True).replace("￥", "")
            return int(price_text)
        return 0

    def stock(self):
        # TODO: Ajax loaded data
        return 1

    def image_url(self):
        img = self.doc.select_one("#largePic")
        if img and img.get('src'):
            return img['src']
        return "http://img32.ddimg.cn/7/35/60129142-1_h.jpg"

    def score(self):
        imgs = self.doc.select("p.fraction img")
        return len([img for img in imgs if 'red' in img.get('src', '')])

    def comments(self):
        title_elems = self.doc.select("#comm_all h5 a")
        content_elems = self.doc.select("#comm_all div.text")
        publish_at_elems = self.doc.select("#comm_all .title .time")
        star_elems = self.doc.select("#comm_all .title .star")

        comments = []
        for i in range(len(title_elems)):
            pub_at_text = publish_at_elems[i].get_text(strip=True) if i < len(publish_at_elems) else ""
            pub_at = datetime.strptime(pub_at_text, "%Y-%m-%d %H:%M:%S") if pub_at_text else datetime.now()

            star = 0
            if i < len(star_elems):
                red_imgs = star_elems[i].select("img")
                star = len([img for img in red_imgs if 'red' in img.get('src', '')])

            comments.append({
                'title': title_elems[i].get_text(strip=True),
                'content': content_elems[i].get_text(strip=True) if i < len(content_elems) else "",
                'publish_at': pub_at,
                'star': star
            })

        return comments

    def belongs_to_categories(self):
        links = self.doc.select(".crumb a")
        categories = []
        for link in links:
            href = link.get('href', '')
            if 'list' in href:
                categories.append({
                    'name': link.get_text(strip=True),
                    'url': href
                })
        return categories

    # Stub methods
    def desc(self): return None
    def price_url(self): return None
    def product_code(self): return None
    def standard(self): return None
    def end_product(self): return None
    def merchant(self): return None
    def brand(self): return None
    def brand_type(self): return None
```

#### Dangdang Digger Example (`digger/dangdang_digger.py`)
```python
class DangdangDigger(Digger):
    def product_list(self):
        links = self.doc.select(".mode_goods div.name a")
        return [link.get('href') for link in links if link.get('href')]
```

#### Dangdang Paginater Example (`paginater/dangdang_paginater.py`)
```python
import re

class DangdangPaginater(Paginater):
    def pagination_list(self):
        elem = self.doc.select_one("#all_num")
        if elem:
            text = elem.get_text(strip=True)
            match = re.search(r'\d+', text)
            max_page = int(match.group(0)) if match else 1
        else:
            max_page = 1

        return [f"{self.url}&p={i}" for i in range(1, max_page + 1)]
```

### 9. Script Runners

#### run_fetcher (`scripts/run_fetcher.py`)
```python
#!/usr/bin/env python
# encoding: utf-8

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spider.utils.utils import Utils
from spider.utils.optparse import SpiderOptions
from spider.logger import get_logger

# Load dependencies
Utils.load_mongo(SpiderOptions['environment'])
Utils.load_models()
Utils.load_fetcher()

from spider.models.category import Category

logger = get_logger(__name__)

# Dynamically get the fetcher class
fetcher_class_name = f"{SpiderOptions['name'].capitalize()}Fetcher"
fetcher_module = __import__(f"spider.fetcher.{SpiderOptions['name']}_fetcher", fromlist=[fetcher_class_name])
ThisFetcher = getattr(fetcher_module, fetcher_class_name)

# Fetch and save categories
for category in ThisFetcher.category_list():
    cat = Category(
        url=category['url'],
        kind=SpiderOptions['name'],
        name=category['name']
    )
    cat.save()
    logger.info(f"Saved URL: {cat.url}")
```

#### run_paginater (`scripts/run_paginater.py`)
```python
#!/usr/bin/env python
# encoding: utf-8

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spider.utils.utils import Utils
from spider.utils.optparse import SpiderOptions
from spider.logger import get_logger

Utils.load_mongo(SpiderOptions['environment'])
Utils.load_models()
Utils.load_paginater()
Utils.load_downloader()

from spider.models.category import Category
from spider.models.page import Page

logger = get_logger(__name__)

# Dynamic class loading
paginater_class_name = f"{SpiderOptions['name'].capitalize()}Paginater"
downloader_class_name = f"{SpiderOptions['downloader'].capitalize()}Downloader"

paginater_module = __import__(f"spider.paginater.{SpiderOptions['name']}_paginater", fromlist=[paginater_class_name])
downloader_module = __import__(f"spider.downloader.{SpiderOptions['downloader']}_downloader", fromlist=[downloader_class_name])

CurrentPaginater = getattr(paginater_module, paginater_class_name)
CurrentDownloader = getattr(downloader_module, downloader_class_name)

def start_paginate(category):
    paginater = CurrentPaginater(category)
    for url in paginater.pagination_list():
        page = Page(
            url=url,
            kind=SpiderOptions['name'],
            category_id=category.id
        )
        page.save()
        logger.info(f"Saved Page URL: {url}")

    category.completed = True
    category.save()
    logger.info(f"Completed Category URL: {category.url}")

# Get leaf categories (tree structure)
categories = Category.from_kind(SpiderOptions['name']).filter(completed=False).limit(SpiderOptions['number'])
downloader = CurrentDownloader(list(categories))
downloader.run(start_paginate)
```

#### run_digger (`scripts/run_digger.py`)
```python
#!/usr/bin/env python
# encoding: utf-8

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spider.utils.utils import Utils
from spider.utils.optparse import SpiderOptions
from spider.logger import get_logger

Utils.load_mongo(SpiderOptions['environment'])
Utils.load_models()
Utils.load_digger()
Utils.load_downloader()

from spider.models.page import Page
from spider.models.product_url import ProductUrl

logger = get_logger(__name__)

# Dynamic class loading
digger_class_name = f"{SpiderOptions['name'].capitalize()}Digger"
downloader_class_name = f"{SpiderOptions['downloader'].capitalize()}Downloader"

digger_module = __import__(f"spider.digger.{SpiderOptions['name']}_digger", fromlist=[digger_class_name])
downloader_module = __import__(f"spider.downloader.{SpiderOptions['downloader']}_downloader", fromlist=[downloader_class_name])

CurrentDigger = getattr(digger_module, digger_class_name)
CurrentDownloader = getattr(downloader_module, downloader_class_name)

def start_digg(page):
    digger = CurrentDigger(page)
    for url in digger.product_list():
        product_url = ProductUrl(
            url=url,
            kind=SpiderOptions['name'],
            page_id=page.id
        )
        product_url.save()
        logger.info(f"Saved Product URL: {url}")

    page.completed = True
    page.save()
    logger.info(f"Completed Page URL: {page.url}")

pages = Page.from_kind(SpiderOptions['name']).filter(completed=False).limit(SpiderOptions['number'])
downloader = CurrentDownloader(list(pages))
downloader.run(start_digg)
```

#### run_parser (`scripts/run_parser.py`)
```python
#!/usr/bin/env python
# encoding: utf-8

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spider.utils.utils import Utils
from spider.utils.optparse import SpiderOptions
from spider.logger import get_logger

Utils.load_mongo(SpiderOptions['environment'])
Utils.load_models()
Utils.load_parser()
Utils.load_downloader()

from spider.models.product_url import ProductUrl
from spider.models.product import Product
from spider.models.category import Category

logger = get_logger(__name__)

# Dynamic class loading
parser_class_name = f"{SpiderOptions['name'].capitalize()}Parser"
downloader_class_name = f"{SpiderOptions['downloader'].capitalize()}Downloader"

parser_module = __import__(f"spider.parser.{SpiderOptions['name']}_parser", fromlist=[parser_class_name])
downloader_module = __import__(f"spider.downloader.{SpiderOptions['downloader']}_downloader", fromlist=[downloader_class_name])

CurrentParser = getattr(parser_module, parser_class_name)
CurrentDownloader = getattr(downloader_module, downloader_class_name)

def assoc_category(category_list, kind):
    """Associate category hierarchy"""
    cate_list = []
    for name_and_url in category_list:
        cat = Category.objects(name=name_and_url['name'], url=name_and_url['url'], kind=kind).first()
        if not cat:
            cat = Category(name=name_and_url['name'], url=name_and_url['url'], kind=kind)
            cat.save()
        cate_list.append(cat)
    set_assoc(cate_list)

def set_assoc(cate_list):
    """Set parent-child relationships"""
    for i in range(len(cate_list) - 1):
        parent = cate_list[i]
        child = cate_list[i + 1]
        child.parent = parent
        child.save()

def start_parse(product_url):
    parser = CurrentParser(product_url)
    assoc_category(parser.belongs_to_categories(), SpiderOptions['name'])

    product = Product(**parser.attributes())
    product.save()

    logger.info(f"Parsed Product URL: {product_url.url}")
    product_url.completed = True
    product_url.save()

product_urls = ProductUrl.from_kind(SpiderOptions['name']).filter(completed=False).limit(SpiderOptions['number'])
downloader = CurrentDownloader(list(product_urls))
downloader.run(start_parse)
```

---

## Dependencies Mapping

### Ruby → Python

| Ruby Gem | Python Package | Purpose |
|----------|---------------|---------|
| mongoid | mongoengine | MongoDB ODM |
| bson_ext | pymongo | BSON support |
| mongoid-tree | Custom implementation | Tree structure for categories |
| nokogiri | beautifulsoup4 + lxml | HTML parsing |
| typhoeus | requests + ThreadPoolExecutor | Multi-threaded HTTP |
| eventmachine | asyncio + aiohttp | Async HTTP |
| em-http-request | aiohttp | Async HTTP client |
| mini_tesseract | pytesseract | OCR for price images |

### requirements.txt
```
mongoengine>=0.24.0
pymongo>=4.0.0
beautifulsoup4>=4.11.0
lxml>=4.9.0
requests>=2.28.0
aiohttp>=3.8.0
pytesseract>=0.3.10
pyyaml>=6.0
```

---

## Configuration Files

### config/mongoid.yml
```yaml
development:
  host: localhost
  database: testapp_development

production:
  host: localhost
  database: testapp_production
```

### config/redis.yml (if needed)
```yaml
development:
  host: localhost
  port: 6379
  db: 0

production:
  host: localhost
  port: 6379
  db: 1
```

---

## Directory Structure

```
direct_web_spider/
├── spider/
│   ├── __init__.py
│   ├── logger.py
│   ├── encoding.py
│   ├── fetcher.py
│   ├── parser.py
│   ├── digger.py
│   ├── paginater.py
│   ├── downloader.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── category.py
│   │   ├── page.py
│   │   ├── product_url.py
│   │   ├── product.py
│   │   ├── brand.py
│   │   ├── brand_type.py
│   │   ├── merchant.py
│   │   ├── end_product.py
│   │   ├── middle_product.py
│   │   ├── top_product.py
│   │   ├── comment.py
│   │   └── body.py
│   ├── fetcher/
│   │   ├── __init__.py
│   │   ├── dangdang_fetcher.py
│   │   ├── jingdong_fetcher.py
│   │   ├── tmall_fetcher.py
│   │   ├── newegg_fetcher.py
│   │   ├── suning_fetcher.py
│   │   └── gome_fetcher.py
│   ├── parser/
│   │   ├── __init__.py
│   │   ├── dangdang_parser.py
│   │   ├── jingdong_parser.py
│   │   ├── tmall_parser.py
│   │   ├── newegg_parser.py
│   │   ├── suning_parser.py
│   │   └── gome_parser.py
│   ├── digger/
│   │   ├── __init__.py
│   │   ├── dangdang_digger.py
│   │   ├── jingdong_digger.py
│   │   ├── tmall_digger.py
│   │   ├── newegg_digger.py
│   │   ├── suning_digger.py
│   │   └── gome_digger.py
│   ├── paginater/
│   │   ├── __init__.py
│   │   ├── dangdang_paginater.py
│   │   ├── jingdong_paginater.py
│   │   ├── tmall_paginater.py
│   │   ├── newegg_paginater.py
│   │   ├── suning_paginater.py
│   │   └── gome_paginater.py
│   ├── downloader/
│   │   ├── __init__.py
│   │   ├── normal_downloader.py
│   │   ├── ty_downloader.py
│   │   └── em_downloader.py
│   └── utils/
│       ├── __init__.py
│       ├── utils.py
│       └── optparse.py
├── scripts/
│   ├── run_fetcher.py
│   ├── run_paginater.py
│   ├── run_digger.py
│   ├── run_parser.py
│   └── console.py
├── config/
│   ├── mongoid.yml
│   └── redis.yml
├── log/
├── requirements.txt
├── README.md
└── PRD_RUBY_TO_PYTHON_CONVERSION.md
```

---

## Testing Strategy

### Unit Tests
- Test each model's CRUD operations
- Test encoding conversions
- Test utility functions
- Test each parser, digger, paginater implementation

### Integration Tests
- Test complete pipeline: Fetcher → Paginater → Digger → Parser
- Test with mock data
- Test downloader implementations

### Manual Testing
1. Start MongoDB
2. Run fetcher for one site (e.g., dangdang)
3. Verify categories saved
4. Run paginater
5. Verify pages saved
6. Run digger
7. Verify product URLs saved
8. Run parser
9. Verify products saved with all fields

---

## Implementation Plan

### Phase 1: Core Infrastructure (Week 1)
- [x] Set up Python project structure
- [ ] Convert Logger module
- [ ] Convert Encoding module
- [ ] Convert Utils module
- [ ] Convert Optparse module
- [ ] Set up MongoDB connection

### Phase 2: Models (Week 1)
- [ ] Convert all 11 models
- [ ] Implement tree structure for Category
- [ ] Test model CRUD operations

### Phase 3: Base Classes (Week 2)
- [ ] Convert Fetcher base
- [ ] Convert Parser base
- [ ] Convert Digger base
- [ ] Convert Paginater base
- [ ] Convert Downloader base

### Phase 4: Downloader Implementations (Week 2)
- [ ] Convert NormalDownloader
- [ ] Convert TyDownloader
- [ ] Convert EmDownloader
- [ ] Test all downloaders

### Phase 5: Site Implementations - Dangdang (Week 3)
- [ ] Convert DangdangFetcher
- [ ] Convert DangdangPaginater
- [ ] Convert DangdangDigger
- [ ] Convert DangdangParser
- [ ] Test complete Dangdang pipeline

### Phase 6: Site Implementations - Others (Week 3-4)
- [ ] Convert Jingdong implementations
- [ ] Convert Tmall implementations
- [ ] Convert Newegg implementations
- [ ] Convert Suning implementations
- [ ] Convert Gome implementations

### Phase 7: Script Runners (Week 4)
- [ ] Convert run_fetcher
- [ ] Convert run_paginater
- [ ] Convert run_digger
- [ ] Convert run_parser
- [ ] Create console script

### Phase 8: Testing & Documentation (Week 5)
- [ ] Integration testing
- [ ] Performance testing
- [ ] Update README with Python instructions
- [ ] Create usage examples

---

## Success Criteria

1. **Functionality:** All 4 pipeline stages work identically to Ruby version
2. **Data:** MongoDB schema remains unchanged
3. **Performance:** Python version matches or exceeds Ruby performance
4. **Compatibility:** Can process data from Ruby version
5. **Maintainability:** Clean, documented Python code following PEP 8
6. **Testing:** >80% code coverage with unit and integration tests

---

## Risk Mitigation

### Risk 1: Encoding Issues
**Mitigation:** Thoroughly test GB18030 → UTF-8 conversion with real data

### Risk 2: HTML Parsing Differences
**Mitigation:** Compare Nokogiri vs BeautifulSoup outputs; adjust selectors

### Risk 3: MongoDB Tree Structure
**Mitigation:** Implement custom tree or use django-mptt patterns

### Risk 4: Website Structure Changes
**Mitigation:** Focus on framework conversion; parsers may need updates

### Risk 5: Async/Threading Complexity
**Mitigation:** Start with NormalDownloader; add concurrency incrementally

---

## Maintenance & Support

### Code Standards
- Follow PEP 8
- Type hints where appropriate
- Docstrings for all public methods
- Comprehensive logging

### Version Control
- Git branches for each phase
- Pull requests for review
- Tag releases (v1.0-python, etc.)

### Documentation
- Code comments in English
- README with usage examples
- API documentation
- Migration guide from Ruby

---

## Appendix

### A. Complete File Conversion Matrix

| Ruby File | Python File | Status |
|-----------|-------------|--------|
| fetcher.rb | spider/fetcher.py | Pending |
| parser.rb | spider/parser.py | Pending |
| digger.rb | spider/digger.py | Pending |
| paginater.rb | spider/paginater.py | Pending |
| downloader.rb | spider/downloader.py | Pending |
| logger.rb | spider/logger.py | Pending |
| encoding.rb | spider/encoding.py | Pending |
| utils/utils.rb | spider/utils/utils.py | Pending |
| utils/optparse.rb | spider/utils/optparse.py | Pending |
| models/category.rb | spider/models/category.py | Pending |
| models/page.rb | spider/models/page.py | Pending |
| models/product_url.rb | spider/models/product_url.py | Pending |
| models/product.rb | spider/models/product.py | Pending |
| models/brand.rb | spider/models/brand.py | Pending |
| models/brand_type.rb | spider/models/brand_type.py | Pending |
| models/merchant.rb | spider/models/merchant.py | Pending |
| models/end_product.rb | spider/models/end_product.py | Pending |
| models/middle_product.rb | spider/models/middle_product.py | Pending |
| models/top_product.rb | spider/models/top_product.py | Pending |
| models/comment.rb | spider/models/comment.py | Pending |
| models/body.rb | spider/models/body.py | Pending |
| fetcher/dangdang_fetcher.rb | spider/fetcher/dangdang_fetcher.py | Pending |
| fetcher/jingdong_fetcher.rb | spider/fetcher/jingdong_fetcher.py | Pending |
| fetcher/tmall_fetcher.rb | spider/fetcher/tmall_fetcher.py | Pending |
| fetcher/newegg_fetcher.rb | spider/fetcher/newegg_fetcher.py | Pending |
| fetcher/suning_fetcher.rb | spider/fetcher/suning_fetcher.py | Pending |
| fetcher/gome_fetcher.rb | spider/fetcher/gome_fetcher.py | Pending |
| parser/dangdang_parser.rb | spider/parser/dangdang_parser.py | Pending |
| parser/jingdong_parser.rb | spider/parser/jingdong_parser.py | Pending |
| parser/tmall_parser.rb | spider/parser/tmall_parser.py | Pending |
| parser/newegg_parser.rb | spider/parser/newegg_parser.py | Pending |
| parser/suning_parser.rb | spider/parser/suning_parser.py | Pending |
| parser/gome_parser.rb | spider/parser/gome_parser.py | Pending |
| digger/dangdang_digger.rb | spider/digger/dangdang_digger.py | Pending |
| digger/jingdong_digger.rb | spider/digger/jingdong_digger.py | Pending |
| digger/tmall_digger.rb | spider/digger/tmall_digger.py | Pending |
| digger/newegg_digger.rb | spider/digger/newegg_digger.py | Pending |
| digger/suning_digger.rb | spider/digger/suning_digger.py | Pending |
| digger/gome_digger.rb | spider/digger/gome_digger.py | Pending |
| paginater/dangdang_paginater.rb | spider/paginater/dangdang_paginater.py | Pending |
| paginater/jingdong_paginater.rb | spider/paginater/jingdong_paginater.py | Pending |
| paginater/tmall_paginater.rb | spider/paginater/tmall_paginater.py | Pending |
| paginater/newegg_paginater.rb | spider/paginater/newegg_paginater.py | Pending |
| paginater/suning_paginater.rb | spider/paginater/suning_paginater.py | Pending |
| paginater/gome_paginater.rb | spider/paginater/gome_paginater.py | Pending |
| downloader/normal_downloader.rb | spider/downloader/normal_downloader.py | Pending |
| downloader/ty_downloader.rb | spider/downloader/ty_downloader.py | Pending |
| downloader/em_downloader.rb | spider/downloader/em_downloader.py | Pending |
| script/run_fetcher | scripts/run_fetcher.py | Pending |
| script/run_paginater | scripts/run_paginater.py | Pending |
| script/run_digger | scripts/run_digger.py | Pending |
| script/run_parser | scripts/run_parser.py | Pending |

**Total Files:** 51 files to convert

---

## Notes

- All Chinese comments and error messages preserved
- Redis integration mentioned in utils but not fully implemented in Ruby - skip for now
- mini_tesseract OCR functionality should be preserved with pytesseract
- Tree structure for categories is critical - use custom implementation or library
- Maintain backward compatibility with existing MongoDB data

---

**END OF PRD**
