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
        with patch('scripts.run_parser.main') as mock_main:
            mock_main.return_value = 0
            result = mock_main()
            assert result == 0

    @pytest.mark.integration
    def test_run_downloader_script(self):
        """Test run_downloader script"""
        with patch('scripts.run_downloader.main') as mock_main:
            mock_main.return_value = 0
            result = mock_main()
            assert result == 0

    @pytest.mark.integration
    def test_run_fetcher_script(self):
        """Test run_fetcher script"""
        with patch('scripts.run_fetcher.main') as mock_main:
            mock_main.return_value = 0
            result = mock_main()
            assert result == 0

    @pytest.mark.integration
    def test_run_digger_script(self):
        """Test run_digger script"""
        with patch('scripts.run_digger.main') as mock_main:
            mock_main.return_value = 0
            result = mock_main()
            assert result == 0

    @pytest.mark.integration
    def test_run_paginater_script(self):
        """Test run_paginater script"""
        with patch('scripts.run_paginater.main') as mock_main:
            mock_main.return_value = 0
            result = mock_main()
            assert result == 0