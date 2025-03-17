import logging
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from notifications import send_sms

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_send_sms():
    """Test sending an SMS notification."""
    try:
        message = "Test message from trading bot."
        response = send_sms(message)

        if response:  # Now checking return value
            logging.info("✅ SMS notification test passed.")
        else:
            logging.error("❌ SMS notification test failed.")
    except Exception as e:
        logging.error(f"❌ SMS notification test failed: {e}")

if __name__ == "__main__":
    logging.info("🔍 Running Notifications Tests...\n")
    time.sleep(1)
    test_send_sms()
    logging.info("\n✅ All tests completed.")
