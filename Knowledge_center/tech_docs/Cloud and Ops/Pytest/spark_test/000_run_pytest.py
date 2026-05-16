# Run all tests
pytest

# Run specific file
pytest tests/test_customer.py

# Run specific class
pytest tests/test_customer.py::TestFilterByCountry

# Run specific test
pytest tests/test_customer.py::TestFilterByCountry::test_filter_usa_customers

# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term-missing

# Run only unit tests
pytest -m unit

# Skip slow tests
pytest -m "not slow"

# Run in parallel (pip install pytest-xdist)
pytest -n auto