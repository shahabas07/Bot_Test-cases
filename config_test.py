import logging
import time
import sys
import os

# Get the parent directory of the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import config  # Ensure config.py is available

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_config_values():
    """Test config values are set correctly."""
    try:
        assert config.ATR_LENGTH > 0, "ATR_LENGTH should be greater than 0"
        assert config.FACTOR > 0, "FACTOR should be greater than 0"
        assert config.STOP_LOSS > 0, "STOP_LOSS should be greater than 0"
        assert config.TRADE_ALLOCATION > 0, "TRADE_ALLOCATION should be greater than 0"
        assert config.LOT_SIZE > 0, "LOT_SIZE should be greater than 0"
        assert config.COOLDOWN_PERIOD >= 0, "COOLDOWN_PERIOD should be non-negative"
        logging.info("✅ Config values test passed.")
    except AssertionError as e:
        logging.error(f"❌ Config values test failed: {e}")

if __name__ == "__main__":
    logging.info("🔍 Running Config Tests...\n")
    time.sleep(1)
    test_config_values()
    logging.info("\n✅ All tests completed.")
