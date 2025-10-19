"""
Simple test to verify test infrastructure works
"""
import pytest


@pytest.mark.unit
def test_simple():
    """Simple test that always passes"""
    assert True


@pytest.mark.unit
def test_math():
    """Test basic math operations"""
    assert 2 + 2 == 4
    assert 3 * 3 == 9


@pytest.mark.unit
def test_string_operations():
    """Test string operations"""
    text = "Hello World"
    assert len(text) == 11
    assert text.upper() == "HELLO WORLD"
    assert text.lower() == "hello world"


@pytest.mark.integration
def test_integration_simple():
    """Simple integration test"""
    data = {"key": "value", "number": 42}
    assert data["key"] == "value"
    assert data["number"] == 42


@pytest.mark.performance
def test_performance_simple():
    """Simple performance test"""
    import time
    start = time.time()
    # Simulate some work
    sum(range(1000))
    end = time.time()
    assert end - start < 1.0  # Should complete in less than 1 second
