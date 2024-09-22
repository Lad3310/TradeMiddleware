import pandas as pd
from utils import simulate_external_api_call
import logging
import asyncio

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_test_data(num_rows):
    return pd.DataFrame({
        'trade_id': range(1, num_rows + 1),
        'symbol': ['AAPL', 'GOOGL', 'MSFT', 'AMZN'] * (num_rows // 4 + 1),
        'quantity': [100] * num_rows,
        'price': [150.0] * num_rows
    })

def test_successful_scenario():
    logging.info("Testing successful scenario")
    test_data = create_test_data(50)
    result = simulate_external_api_call(test_data, max_retries=3, timeout=5, chunk_size=10, total_timeout=60)
    logging.info(f"Result: {result}")
    assert result['status'] == 'success', "Expected successful scenario"

def test_partial_failure_scenario():
    logging.info("Testing partial failure scenario")
    test_data = create_test_data(100)
    result = simulate_external_api_call(test_data, max_retries=2, timeout=2, chunk_size=20, total_timeout=30)
    logging.info(f"Result: {result}")
    assert result['status'] in ['partial_success', 'failure'], "Expected partial failure or failure"

def test_large_dataset_scenario():
    logging.info("Testing large dataset scenario")
    test_data = create_test_data(1000)
    result = simulate_external_api_call(test_data, max_retries=3, timeout=5, chunk_size=50, total_timeout=120)
    logging.info(f"Result: {result}")
    assert result['processed_rows'] > 0, "Expected some processed rows"

def test_timeout_scenario():
    logging.info("Testing timeout scenario")
    test_data = create_test_data(500)
    result = simulate_external_api_call(test_data, max_retries=2, timeout=1, chunk_size=10, total_timeout=5)
    logging.info(f"Result: {result}")
    assert result['status'] == 'failure', "Expected failure due to timeout"

if __name__ == "__main__":
    test_successful_scenario()
    test_partial_failure_scenario()
    test_large_dataset_scenario()
    test_timeout_scenario()
    logging.info("All tests completed")
