# encoding: utf-8
"""
Utility functions for the Spider framework.
Mimics Ruby's Spider::Utils module.
"""

import re
import gzip
import io
from pathlib import Path
import yaml
from urllib.parse import parse_qs, urlencode
from mongoengine import connect


class Utils:
    """
    Utility class with various helper methods.
    Mimics Ruby's Spider::Utils module.
    """

    @staticmethod
    def valid_html(html):
        """
        Check if HTML is valid/complete.

        Args:
            html: HTML string

        Returns:
            bool: True if HTML appears complete
        """
        if not html:
            return False
        # Check if HTML ends with </html> tag (with optional comments/whitespace)
        pattern = r'</html>(<!--(.*?)-->|\s)*$'
        return re.search(pattern, html, re.MULTILINE | re.IGNORECASE) is not None

    @staticmethod
    def query2hash(query_str):
        """
        Convert query string to dictionary.

        Args:
            query_str: Query string like "a=1&b=2"

        Returns:
            dict: Parsed query parameters
        """
        result = {}
        for key, value in parse_qs(query_str).items():
            result[key] = value[0] if len(value) == 1 else value
        return result

    @staticmethod
    def hash2query(hash_dict):
        """
        Convert dictionary to query string.

        Args:
            hash_dict: Dictionary of parameters

        Returns:
            str: Query string
        """
        return urlencode(hash_dict)

    @staticmethod
    def decompress_gzip(data):
        """
        Decompress gzip data.

        Args:
            data: Gzip compressed bytes

        Returns:
            str: Decompressed string
        """
        if isinstance(data, str):
            data = data.encode('utf-8')

        with gzip.GzipFile(fileobj=io.BytesIO(data)) as gz:
            return gz.read().decode('utf-8')

    @staticmethod
    def load_models():
        """
        Load all model modules.
        Imports all Python files in the models directory.
        """
        models_dir = Path(__file__).parent.parent / 'models'
        model_files = sorted(models_dir.glob('*.py'), key=lambda f: len(str(f)))

        for model_file in model_files:
            if model_file.name.startswith('__'):
                continue
            module_name = model_file.stem
            print(f"Loading Model: {model_file.absolute()}")
            __import__(f'spider.models.{module_name}')

    @staticmethod
    def load_mongo(environment):
        """
        Load MongoDB connection based on environment.

        Args:
            environment: 'development' or 'production'
        """
        config_path = Path(__file__).parent.parent.parent / 'config' / 'mongoid.yml'

        with open(config_path, 'r') as f:
            settings = yaml.safe_load(f)

        env_settings = settings.get(environment, {})

        host = env_settings.get('host', 'localhost')
        database = env_settings.get('database', 'testapp_development')
        port = env_settings.get('port', 27017)
        username = env_settings.get('username')
        password = env_settings.get('password')

        # Connect to MongoDB
        if username and password:
            connect(database, host=host, port=port, username=username, password=password)
        else:
            connect(database, host=host, port=port)

        print(f"Connected to MongoDB: {host}:{port}/{database}")

    @staticmethod
    def load_redis(environment):
        """
        Load Redis connection based on environment.
        (Currently not fully implemented in Ruby version either)

        Args:
            environment: 'development' or 'production'
        """
        # TODO: Implement Redis connection if needed
        pass

    @staticmethod
    def load_fetcher():
        """Load fetcher module"""
        __import__('spider.fetcher')

    @staticmethod
    def load_parser():
        """Load parser module"""
        __import__('spider.parser')

    @staticmethod
    def load_digger():
        """Load digger module"""
        __import__('spider.digger')

    @staticmethod
    def load_paginater():
        """Load paginater module"""
        __import__('spider.paginater')

    @staticmethod
    def load_downloader():
        """Load downloader module"""
        __import__('spider.downloader')
