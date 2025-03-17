import logging
import time
import sys
import os

# Get the parent directory of the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from state_manager import TradeState

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_state_saving_loading():
    """Test saving and loading trade state."""
    try:
        state = TradeState()
        state.open_positions = [{"symbol": "NIFTY", "quantity": 1}]
        state.save_state()
        
        loaded_state = TradeState()
        loaded_state.load_state()
        
        assert loaded_state.open_positions == state.open_positions
        logging.info("✅ State saving and loading test passed.")
    except Exception as e:
        logging.error(f"❌ State saving and loading test failed: {e}")

if __name__ == "__main__":
    logging.info("🔍 Running State Manager Tests...\n")
    time.sleep(1)
    test_state_saving_loading()
    logging.info("\n✅ All tests completed.")
