"""
Integration tests for scripts
"""

import pytest
from unittest.mock import Mock, patch


class TestScripts:
    """Test scripts integration"""

    @pytest.mark.integration
    def test_run_parser_script(self):
        """Test run_parser script"""
        # Mock MongoDB connection and all dependencies
        with patch('mongoengine.connect') as mock_connect, \
             patch('spider.models.product_url.ProductUrl') as mock_product_url, \
             patch('spider.utils.optparse.SpiderOptions', {
                 'name': 'dangdang', 
                 'environment': 'test',
                 'downloader': 'normal',
                 'number': 100
             }) as mock_spider_options, \
             patch('spider.parser.dangdang_parser.DangdangParser') as mock_parser_class, \
             patch('spider.downloader.normal_downloader.NormalDownloader') as mock_downloader_class:
            
            # Mock the parser class to avoid actual parsing
            mock_parser_instance = Mock()
            mock_parser_instance.attributes.return_value = {'title': 'Test Product'}
            mock_parser_instance.belongs_to_categories.return_value = []
            mock_parser_class.return_value = mock_parser_instance
            
            # Mock the downloader class
            mock_downloader_instance = Mock()
            mock_downloader_class.return_value = mock_downloader_instance
            
            # Mock ProductUrl.from_kind to return empty list
            mock_product_url.from_kind.return_value.filter.return_value.limit.return_value = []
            
            # The script runs directly when imported, so we just test that it can be imported
            import scripts.run_parser
            assert scripts.run_parser is not None

    @pytest.mark.integration
    def test_run_digger_script(self):
        """Test run_digger script"""
        # Mock all dependencies for run_digger script
        with patch('mongoengine.connect') as mock_connect, \
             patch('spider.utils.optparse.SpiderOptions', {
                 'name': 'dangdang', 
                 'environment': 'test',
                 'downloader': 'normal',
                 'number': 100
             }) as mock_spider_options, \
             patch('spider.models.page.Page') as mock_page_class, \
             patch('spider.digger.dangdang_digger.DangdangDigger') as mock_digger_class:
            
            # Mock the Page class to avoid database access
            mock_page_instance = Mock()
            mock_page_instance.filter.return_value.limit.return_value = []
            mock_page_class.from_kind.return_value = mock_page_instance
            
            # Mock the digger class
            mock_digger_instance = Mock()
            mock_digger_instance.product_list.return_value = []
            mock_digger_class.return_value = mock_digger_instance
            
            # The script runs directly when imported, so we just test that it can be imported
            import scripts.run_digger
            assert scripts.run_digger is not None

    @pytest.mark.integration
    def test_run_fetcher_script(self):
        """Test run_fetcher script"""
        # Mock all dependencies for run_fetcher script
        with patch('mongoengine.connect') as mock_connect, \
             patch('spider.utils.optparse.SpiderOptions', {
                 'name': 'dangdang', 
                 'environment': 'test',
                 'downloader': 'normal',
                 'number': 100
             }) as mock_spider_options, \
             patch('spider.fetcher.dangdang_fetcher.DangdangFetcher') as mock_fetcher_class:
            
            # Mock the fetcher class
            mock_fetcher_instance = Mock()
            mock_fetcher_instance.category_list.return_value = []
            mock_fetcher_class.return_value = mock_fetcher_instance
            
            # The script runs directly when imported, so we just test that it can be imported
            import scripts.run_fetcher
            assert scripts.run_fetcher is not None

    @pytest.mark.integration
    def test_run_paginater_script(self):
        """Test run_paginater script"""
        # Mock all dependencies for run_paginater script
        with patch('mongoengine.connect') as mock_connect, \
             patch('spider.utils.optparse.SpiderOptions', {
                 'name': 'dangdang', 
                 'environment': 'test',
                 'downloader': 'normal',
                 'number': 100
             }) as mock_spider_options, \
             patch('spider.models.category.Category') as mock_category_class, \
             patch('spider.paginater.dangdang_paginater.DangdangPaginater') as mock_paginater_class:
            
            # Mock the Category class to avoid database access
            mock_category_class.from_kind.return_value = []
            
            # Mock the paginater class
            mock_paginater_instance = Mock()
            mock_paginater_instance.pagination_list.return_value = []
            mock_paginater_class.return_value = mock_paginater_instance
            
            # The script runs directly when imported, so we just test that it can be imported
            import scripts.run_paginater
            assert scripts.run_paginater is not None