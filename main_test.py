import logging
import time
import sys
import os

# Get the parent directory of the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from auth import get_jwt_token
from trading_logic import check_trade
from state_manager import TradeState

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_main_execution():
    """Test main script execution components."""
    try:
        access_token = get_jwt_token()
        if not access_token:
            logging.error("❌ Failed to obtain access token.")
            return
        
        state = TradeState()
        state.load_state()
        
        check_trade(state, access_token)  # Run one iteration
        logging.info("✅ Main script execution test passed.")
    except Exception as e:
        logging.error(f"❌ Main script execution test failed: {e}")

if __name__ == "__main__":
    logging.info("🔍 Running Main Script Tests...\n")
    time.sleep(1)
    test_main_execution()
    logging.info("\n✅ All tests completed.")
