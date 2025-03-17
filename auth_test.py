import sys
import os
import logging

# Get the parent directory of testCase
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the authentication module
from auth import get_jwt_token

logging.basicConfig(level=logging.INFO)

def test_auth():
    """Test authentication and token retrieval."""
    token = get_jwt_token()
    if token:
        logging.info(f"✅ Authentication Successful! Token: {token[:10]}...")  # Mask full token
    else:
        logging.error("❌ Authentication Failed!")

if __name__ == "__main__":
    logging.info("🔍 Running Authentication Tests...\n")
    test_auth()
    logging.info("\n✅ All tests completed.")
