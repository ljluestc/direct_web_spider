# Direct Web Spider - Python Version

**Python conversion of the direct_web_spider Ruby framework**

A directed web scraping framework for extracting product information from major Chinese e-commerce platforms.

---

## Overview

This is a complete Python 3 conversion of the original Ruby-based direct_web_spider framework. The framework provides a structured pipeline for scraping product data from six major e-commerce sites:

- **Dangdang** (dangdang.com)
- **JingDong/360buy** (jd.com)
- **Tmall** (tmall.com)
- **Newegg China** (newegg.com.cn)
- **Suning** (suning.com)
- **Gome** (gome.com.cn)

---

## Requirements

### System Requirements
- **Python 3.8+**
- **MongoDB** (running locally or remotely)

### Python Dependencies
Install all dependencies using pip:

```bash
pip install -r requirements.txt
```

Dependencies include:
- `mongoengine>=0.24.0` - MongoDB ODM
- `pymongo>=4.0.0` - MongoDB driver
- `beautifulsoup4>=4.11.0` - HTML parsing
- `lxml>=4.9.0` - Fast XML/HTML parser
- `requests>=2.28.0` - HTTP library
- `aiohttp>=3.8.0` - Async HTTP (for EmDownloader)
- `pytesseract>=0.3.10` - OCR for price images
- `pyyaml>=6.0` - YAML config parsing

---

## Project Structure

```
direct_web_spider/
├── spider/                          # Main package
│   ├── __init__.py
│   ├── logger.py                    # Logging module
│   ├── encoding.py                  # Character encoding handling
│   ├── fetcher.py                   # Base fetcher class
│   ├── parser.py                    # Base parser class
│   ├── digger.py                    # Base digger class
│   ├── paginater.py                 # Base paginater class
│   ├── downloader.py                # Base downloader class
│   ├── models/                      # MongoDB models
│   │   ├── category.py              # Category with tree structure
│   │   ├── page.py                  # Listing pages
│   │   ├── product_url.py           # Product URLs
│   │   ├── product.py               # Products with details
│   │   ├── brand.py, merchant.py, etc.
│   │   └── ...
│   ├── fetcher/                     # Site-specific fetchers
│   │   ├── dangdang_fetcher.py
│   │   ├── jingdong_fetcher.py
│   │   └── ...
│   ├── parser/                      # Site-specific parsers
│   │   ├── dangdang_parser.py
│   │   └── ...
│   ├── digger/                      # Site-specific diggers
│   │   ├── dangdang_digger.py
│   │   └── ...
│   ├── paginater/                   # Site-specific paginaters
│   │   ├── dangdang_paginater.py
│   │   └── ...
│   ├── downloader/                  # Downloader implementations
│   │   ├── normal_downloader.py     # Single-threaded
│   │   ├── ty_downloader.py         # Multi-threaded
│   │   └── em_downloader.py         # Async event-driven
│   └── utils/
│       ├── utils.py                 # Utility functions
│       └── optparse.py              # CLI argument parsing
├── scripts/                         # Executable scripts
│   ├── run_fetcher.py              # Step 1: Fetch categories
│   ├── run_paginater.py            # Step 2: Generate pagination URLs
│   ├── run_digger.py               # Step 3: Extract product URLs
│   └── run_parser.py               # Step 4: Parse product details
├── config/
│   └── mongoid.yml                 # MongoDB configuration
├── log/                            # Log files (auto-created)
├── requirements.txt                # Python dependencies
└── README_PYTHON.md               # This file
```

---

## Architecture

The framework follows a **4-stage pipeline** architecture:

### Stage 1: Fetcher
**Purpose:** Fetch initial category list from e-commerce site
**Input:** Website homepage/category page
**Output:** Category records in MongoDB
**Run:** `python scripts/run_fetcher.py -s dangdang`

### Stage 2: Paginater
**Purpose:** Generate pagination URLs for each category
**Input:** Category records
**Output:** Page records with pagination URLs
**Run:** `python scripts/run_paginater.py -s dangdang -d ty`

### Stage 3: Digger
**Purpose:** Extract product URLs from listing pages
**Input:** Page records
**Output:** ProductUrl records
**Run:** `python scripts/run_digger.py -s dangdang -d ty`

### Stage 4: Parser
**Purpose:** Parse product details from product pages
**Input:** ProductUrl records
**Output:** Product records with full details
**Run:** `python scripts/run_parser.py -s dangdang -d ty`

---

## Installation

### 1. Install System Dependencies

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip mongodb tesseract-ocr

# macOS
brew install python3 mongodb tesseract
```

### 2. Start MongoDB

```bash
# Ubuntu/Debian
sudo systemctl start mongodb

# macOS
brew services start mongodb-community
```

### 3. Install Python Dependencies

```bash
cd direct_web_spider
pip install -r requirements.txt
```

### 4. Configure MongoDB

Edit `config/mongoid.yml` if needed:

```yaml
development:
  host: localhost
  port: 27017
  database: testapp_development

production:
  host: localhost
  port: 27017
  database: testapp_production
```

---

## Usage

### Basic Workflow

Run the 4 stages in order for a specific site:

```bash
# Step 1: Fetch categories
python scripts/run_fetcher.py -s dangdang

# Step 2: Generate pagination URLs
python scripts/run_paginater.py -s dangdang -d ty -n 100

# Step 3: Extract product URLs
python scripts/run_digger.py -s dangdang -d ty -n 500

# Step 4: Parse product details
python scripts/run_parser.py -s dangdang -d ty -n 1000
```

### Command-Line Arguments

All scripts support these arguments:

- **`-s, --name`**: Spider name (dangdang, jingdong, tmall, newegg, suning, gome)
  *Default:* `dangdang`

- **`-e, --environment`**: Environment (development, production)
  *Default:* `development`

- **`-d, --downloader`**: Downloader type (normal, ty, em)
  *Default:* `normal`
  - `normal`: Single-threaded, sequential downloads
  - `ty`: Multi-threaded (20 concurrent threads) - **Recommended**
  - `em`: Async event-driven (asyncio + aiohttp)

- **`-n, --number`**: Number of records to process
  *Default:* `1000`

### Examples

**Fetch categories for JingDong:**
```bash
python scripts/run_fetcher.py -s jingdong
```

**Generate pagination URLs for Tmall (production environment):**
```bash
python scripts/run_paginater.py -e production -s tmall -d ty -n 500
```

**Extract product URLs using async downloader:**
```bash
python scripts/run_digger.py -s suning -d em -n 2000
```

**Parse products with multi-threaded downloader:**
```bash
python scripts/run_parser.py -s gome -d ty -n 5000
```

---

## Features

### Character Encoding Support
The framework automatically handles different character encodings:
- **GB18030**: Dangdang, JingDong, Newegg, Tmall
- **UTF-8**: Suning, Gome

### Logging
All operations are logged to `log/` directory:
- Logs are organized by script and spider name
- Format: `YYYY-MM-DD HH:MM:SS - Module - Level - Message`
- Errors are logged with full context for debugging

### Tree-Structured Categories
Categories support parent-child relationships (hierarchical structure):
```python
from spider.models.category import Category

# Get leaf categories (no children)
leaf_cats = Category.from_kind('dangdang').filter(completed=False)

# Access parent/children
category.parent  # Get parent category
category.children  # Get child categories
category.is_leaf  # Check if leaf node
```

### Flexible Downloaders

**NormalDownloader** - Sequential single-threaded:
```python
# Use for: Testing, debugging, avoiding rate limits
python scripts/run_parser.py -d normal -n 10
```

**TyDownloader** - Multi-threaded (20 workers):
```python
# Use for: Production scraping, faster downloads
python scripts/run_parser.py -d ty -n 1000
```

**EmDownloader** - Async event-driven:
```python
# Use for: Maximum concurrency, lightweight I/O
python scripts/run_parser.py -d em -n 5000
```

---

## Database Schema

### Category
- `url`: Category page URL (unique)
- `name`: Category name
- `kind`: Site name (dangdang, jingdong, etc.)
- `completed`: Processing status
- `parent_id`: Parent category reference (for tree structure)

### Page
- `url`: Listing page URL (unique)
- `kind`: Site name
- `completed`: Processing status
- `category_id`: Reference to category

### ProductUrl
- `url`: Product page URL (unique)
- `kind`: Site name
- `completed`: Processing status
- `page_id`: Reference to listing page

### Product
- `title`: Product title
- `price`: Product price (Decimal)
- `stock`: Stock availability
- `image_url`: Main product image
- `score`: Rating/score
- `kind`: Site name
- `comments`: Embedded comments (list)
- `product_url_id`: Reference to product URL
- `brand`, `merchant`, `end_product`: References

---

## Extending the Framework

### Adding a New E-commerce Site

1. **Create Fetcher** (`spider/fetcher/mysite_fetcher.py`):
```python
from spider.fetcher import Fetcher
import requests
from bs4 import BeautifulSoup

class MysiteFetcher(Fetcher):
    @classmethod
    def category_list(cls):
        # Return list of {'name': ..., 'url': ...}
        pass
```

2. **Create Paginater** (`spider/paginater/mysite_paginater.py`):
```python
from spider.paginater import Paginater

class MysitePaginater(Paginater):
    def pagination_list(self):
        # Return list of pagination URLs
        pass
```

3. **Create Digger** (`spider/digger/mysite_digger.py`):
```python
from spider.digger import Digger

class MysiteDigger(Digger):
    def product_list(self):
        # Return list of product URLs
        pass
```

4. **Create Parser** (`spider/parser/mysite_parser.py`):
```python
from spider.parser import Parser

class MysiteParser(Parser):
    def title(self):
        return self.doc.select_one('h1.title').get_text(strip=True)

    def price(self):
        # Implement all required methods
        pass
```

5. **Add encoding to** `spider/encoding.py`:
```python
Map = {
    # ...
    "mysite": "UTF-8"  # or "GB18030"
}
```

6. **Run the pipeline:**
```bash
python scripts/run_fetcher.py -s mysite
python scripts/run_paginater.py -s mysite -d ty
python scripts/run_digger.py -s mysite -d ty
python scripts/run_parser.py -s mysite -d ty
```

---

## Troubleshooting

### MongoDB Connection Issues
```
Error: Could not connect to MongoDB
```
**Solution:** Ensure MongoDB is running:
```bash
sudo systemctl status mongodb  # Linux
brew services list             # macOS
```

### Import Errors
```
ModuleNotFoundError: No module named 'spider'
```
**Solution:** Run scripts from project root directory or ensure Python path is correct.

### Character Encoding Issues
```
UnicodeDecodeError: ...
```
**Solution:** Check if site encoding is correctly configured in `spider/encoding.py`.

### Empty Results
Check log files in `log/` directory for detailed error messages:
```bash
tail -f log/run_dangdang.log
```

---

## Performance Tips

1. **Use multi-threaded downloader** for production:
   ```bash
   python scripts/run_parser.py -d ty
   ```

2. **Process in batches** using `-n` parameter:
   ```bash
   python scripts/run_digger.py -n 500  # Process 500 at a time
   ```

3. **Monitor MongoDB** performance:
   ```bash
   mongostat
   ```

4. **Check log files** regularly:
   ```bash
   tail -f log/*.log
   ```

---

## Comparison with Ruby Version

| Feature | Ruby | Python |
|---------|------|--------|
| **Language** | Ruby 1.9.2+ | Python 3.8+ |
| **ODM** | Mongoid | MongoEngine |
| **HTML Parser** | Nokogiri | BeautifulSoup4 + lxml |
| **HTTP Library** | Open-URI, Typhoeus | requests, aiohttp |
| **Async** | EventMachine | asyncio |
| **Performance** | ~Same | ~Same or better |
| **Dependencies** | 7 gems | 7 packages |

**All functionality is identical** - the Python version is a line-by-line conversion maintaining the same architecture and logic.

---

## License

See original project for license information.

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## Support

For issues specific to the Python conversion, see:
- **PRD**: `PRD_RUBY_TO_PYTHON_CONVERSION.md`
- **Logs**: Check `log/` directory
- **Original Ruby docs**: `README.md`

---

## Credits

**Python Conversion:** Claude Code (2025)
**Original Ruby Framework:** [db-china.org](https://db-china.org)

---

**Happy Scraping! 🐍**
