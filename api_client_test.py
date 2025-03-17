import logging
import time
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import PAPER_TRADING

# Import required modules
from auth import get_jwt_token
import api_client  # Ensure this contains all required functions

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_auth():
    """Test authentication and token retrieval."""
    token = get_jwt_token()
    if token:
        logging.info("✅ Authentication test passed.")
        return token
    logging.error("❌ Authentication test failed.")
    return None

def test_balance(token):
    """Test fetching account balance."""
    try:
        balance = api_client.get_balance(token)
        logging.info(f"✅ Balance fetched successfully: {balance}")
    except Exception as e:
        logging.error(f"❌ Failed to fetch balance: {e}")

def test_place_dummy_order(access_token):
    """Test placing a dummy order."""
    order_details = {
        "symbol": "NIFTY27MAR2522600PE",
        "price": 100,
        "quantity": 1,
        "is_exit": False,
    }

    try:
        response = api_client.place_order(
            symbol=order_details["symbol"],
            price=order_details["price"],
            quantity=order_details["quantity"],
            is_exit=order_details["is_exit"],
            access_token=access_token,
        )

        if response and response.get("status") == "success":
            logging.info(f"✅ Dummy Order Placement Test Passed: {response}")
        else:
            logging.error(f"❌ Dummy Order Placement Test Failed. Response: {response}")

    except Exception as e:
        logging.error(f"❌ Error in test_place_dummy_order: {e}")

def test_historical_data(token):
    """Test retrieving historical data for a sample stock (last 30 days)."""
    try:
        symboltoken = "99926000" 
        exchange = "NSE"
        interval = "THREE_MINUTE"

        data = api_client.get_historical_data(symboltoken, exchange, interval, token)

        if data and isinstance(data, list):
            logging.info(f"✅ Historical data fetched successfully: {data[:2]} ...")  # Show first 2 entries
        else:
            logging.error("❌ Historical data response is empty or invalid.")

    except Exception as e:
        logging.error(f"❌ Failed to fetch historical data: {e}")

def test_positions(token):
    """Test retrieving open positions."""
    try:
        positions = api_client.get_open_positions(token)
        logging.info(f"✅ Open positions fetched: {positions}")
    except Exception as e:
        logging.error(f"❌ Failed to fetch positions: {e}")

def test_find_affordable_option():
    """Test selecting the best affordable option based on NIFTY price and budget."""
    access_token = get_jwt_token()
    if not access_token:
        logging.error("❌ Authentication failed. Cannot proceed with option selection test.")
        return
    
    expiry = "27-Mar-2025"  # Example expiry date (Correct format)
    capital = 3000  # Test with 10,000 INR budget
    
    logging.info("🔍 Testing CALL (CE) option selection...")
    call_option = api_client.find_affordable_option(expiry, capital, "LONG")
    if call_option:
        logging.info(f"✅ CALL Option Selected: {call_option}")
    else:
        logging.warning("⚠️ No affordable CALL option found.")
    
    time.sleep(1)  # Small delay to avoid rate limit
    
    logging.info("🔍 Testing PUT (PE) option selection...")
    put_option = api_client.find_affordable_option(expiry, capital, "SHORT")
    if put_option:
        logging.info(f"✅ PUT Option Selected: {put_option}")
    else:
        logging.warning("⚠️ No affordable PUT option found.")
    
    logging.info("\n✅ Option selection test completed.")

def test_place_order():
    """Test placing a dummy order in paper trading mode."""
    logging.info("🔍 Running Dummy Order Placement Test...")

    order_details = {
        "symbol": "NIFTY27MAR2522600PE",
        "price": 200,
        "quantity": 1,
        "is_exit": False
    }

    response = api_client.place_order(**order_details)
    
    if PAPER_TRADING:
        # Check for the correct response structure in paper trading mode
        if response and response.get("paper_trade") == True:
            logging.info(f"✅ Paper trade successful: {response}")
        else:
            logging.error(f"❌ Paper trade failed. Response: {response}")
    else:
        # Check for the correct response structure in live trading mode
        if response and response.get("status") == "success":
            logging.info(f"✅ Live order placement successful: {response}")
        else:
            logging.error(f"❌ Live order placement failed. Response: {response}")

def test_save_and_load_paper_positions():
    """Test saving and loading paper positions."""
    position = {
        "symbol": "NIFTY27MAR2522600PE",
        "entry_price": 200,  # Use "entry_price" instead of "price"
        "quantity": 1,
        "type": "BUY",
        "timestamp": "2023-10-01T12:00:00"
    }

    # Save the position
    api_client.save_paper_position(position)
    logging.info("✅ Paper position saved.")

    # Load the positions
    positions = api_client.load_paper_positions()
    if positions:
        logging.info(f"✅ Paper positions loaded: {positions}")
    else:
        logging.error("❌ Failed to load paper positions.")

def test_handle_paper_trade():
    """Test the handle_paper_trade function."""
    symbol = "NIFTY27MAR2522600PE"
    price = 200
    quantity = 1
    is_exit = False

    response = api_client.handle_paper_trade(symbol, price, quantity, is_exit)
    if response and response.get("paper_trade") == True:
        logging.info(f"✅ Paper trade handled successfully: {response}")
    else:
        logging.error(f"❌ Paper trade handling failed. Response: {response}")

if __name__ == "__main__":
    logging.info("🔍 Running API Client Tests...\n")
    
    access_token = test_auth()
    
    if access_token:
        time.sleep(1)
        test_balance(access_token)
        time.sleep(1)
        test_place_dummy_order(access_token)
        time.sleep(1)
        test_historical_data(access_token)
        time.sleep(1)
        test_positions(access_token)
        time.sleep(1)
        test_find_affordable_option()
        time.sleep(1)
        test_place_order()
        time.sleep(1)
        test_save_and_load_paper_positions()
        time.sleep(1)
        test_handle_paper_trade()

    logging.info("\n✅ All tests completed.")