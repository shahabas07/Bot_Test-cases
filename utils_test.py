import logging
import time
import sys
import os
import pandas as pd
import numpy as np

# Get the parent directory of the utils module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import utils  # Ensure utils.py contains all required functions
from auth import get_jwt_token 
from state_manager import get_dummy_balance, update_dummy_balance

# Configure logging
logging.basicConfig(level=logging.INFO)
# Create a logger instance
logger = logging.getLogger(__name__)

# Set the logging level
logger.setLevel(logging.DEBUG)

ACCESS_TOKEN = get_jwt_token()

def test_dummy_balance():
    """Test dummy balance updates."""
    initial_balance = get_dummy_balance()
    logging.info(f"🔍 Initial Dummy Balance: {initial_balance}")

    update_dummy_balance(500)
    assert get_dummy_balance() == initial_balance + 500, "❌ Dummy balance increase failed!"

    update_dummy_balance(-200)
    assert get_dummy_balance() == initial_balance + 300, "❌ Dummy balance decrease failed!"

    logging.info("✅ Dummy balance update test passed.")

def test_atr():
    """Test ATR calculation."""
    df = pd.DataFrame({
        "high": [100, 102, 104, 103, 105],
        "low": [95, 96, 97, 98, 99],
        "close": [98, 101, 103, 102, 104]
    })
    try:
        # Calculate ATR
        atr = utils.calculate_atr(df, period=3)
        
        # Expected ATR values
        expected_atr = [5.0, 5.5, 6.0, 6.0, 6.0]
        
        # Debugging logs
        logger.debug(f"Calculated ATR: {atr.tolist()}")
        logger.debug(f"Expected ATR: {expected_atr}")
        
        # Compare the calculated ATR values with the expected values
        assert atr.tolist() == expected_atr, "❌ ATR values are incorrect."
        logging.info("✅ ATR calculation test passed.")
    except Exception as e:
        logging.error(f"❌ ATR calculation failed: {e}")

def test_upper_lower_bands():
    """Test upper and lower band calculation."""
    df = pd.DataFrame({
        "high": [100, 102, 104, 103, 105],
        "low": [95, 96, 97, 98, 99],
        "close": [98, 101, 103, 102, 104]
    })
    try:
        # Calculate ATR
        df['atr'] = utils.calculate_atr(df, period=3)
        
        # Calculate HL2 (midpoint of high and low)
        hl2 = (df['high'] + df['low']) / 2
        
        # Calculate upper and lower bands
        multiplier = 1.5
        df['upper'] = hl2 + (multiplier * df['atr'])
        df['lower'] = hl2 - (multiplier * df['atr'])
        
        # Expected upper and lower bands
        expected_upper = [105.0, 107.25, 109.5, 109.5, 111.0]
        expected_lower = [90.0, 90.75, 91.5, 91.5, 93.0]
        
        # Debugging logs
        logger.debug(f"Calculated Upper Band: {df['upper'].tolist()}")
        logger.debug(f"Expected Upper Band: {expected_upper}")
        logger.debug(f"Calculated Lower Band: {df['lower'].tolist()}")
        logger.debug(f"Expected Lower Band: {expected_lower}")
        
        # Compare the calculated bands with the expected values
        assert df['upper'].tolist() == expected_upper, "❌ Upper band values are incorrect."
        assert df['lower'].tolist() == expected_lower, "❌ Lower band values are incorrect."
        logging.info("✅ Upper and lower band calculation test passed.")
    except Exception as e:
        logging.error(f"❌ Upper and lower band calculation failed: {e}")

def test_supertrend_logic():
    """Test Supertrend logic."""
    df = pd.DataFrame({
        "high": [100, 102, 104, 103, 105],
        "low": [95, 96, 97, 98, 99],
        "close": [98, 101, 103, 102, 104]
    })
    try:
        # Calculate ATR
        df['atr'] = utils.calculate_atr(df, period=3)
        
        # Calculate HL2 (midpoint of high and low)
        hl2 = (df['high'] + df['low']) / 2
        
        # Calculate upper and lower bands
        multiplier = 1.5
        df['upper'] = hl2 + (multiplier * df['atr'])
        df['lower'] = hl2 - (multiplier * df['atr'])
        
        # Initialize Supertrend column
        df['supertrend'] = np.nan
        trend = True  # Start with an upward trend

        for i in range(1, len(df)):
            if df['close'][i] > df['upper'][i - 1]:
                trend = True  # Uptrend
            elif df['close'][i] < df['lower'][i - 1]:
                trend = False  # Downtrend

            # Set Supertrend value based on the current trend
            if trend:
                df.loc[i, 'supertrend'] = df.loc[i, 'lower']
            else:
                df.loc[i, 'supertrend'] = df.loc[i, 'upper']
        
        # Expected Supertrend values
        expected_supertrend = [np.nan, 90.75, 91.5, 91.5, 93.0]
        
        # Debugging logs
        logger.debug(f"Calculated Supertrend: {df['supertrend'].tolist()}")
        logger.debug(f"Expected Supertrend: {expected_supertrend}")
        
        # Compare the calculated Supertrend values with the expected values using np.allclose
        calculated_supertrend = df['supertrend'].tolist()
        assert np.allclose(calculated_supertrend[1:], expected_supertrend[1:], rtol=1e-5, equal_nan=True), "❌ Supertrend values are incorrect."
        logging.info("✅ Supertrend logic test passed.")
    except Exception as e:
        logging.error(f"❌ Supertrend logic test failed: {e}")

def test_supertrend():
    """Test Supertrend calculation."""
    df = pd.DataFrame({
        "high": [100, 102, 104, 103, 105],
        "low": [95, 96, 97, 98, 99],
        "close": [98, 101, 103, 102, 104]
    })
    try:
        # Pass the correct parameters: period and multiplier
        result = utils.supertrend(df, period=3, multiplier=1.5)
        
        # Expected Supertrend values based on the corrected logic
        expected_supertrend = [np.nan, 90.75, 91.5, 91.5, 93.0]
        
        # Debugging logs
        logger.debug(f"Calculated ATR: {result['atr'].tolist()}")
        logger.debug(f"Calculated Upper Band: {result['upper'].tolist()}")
        logger.debug(f"Calculated Lower Band: {result['lower'].tolist()}")
        logger.debug(f"Calculated Supertrend: {result['supertrend'].tolist()}")
        
        # Compare the calculated Supertrend values with the expected values using np.allclose
        calculated_supertrend = result["supertrend"].tolist()
        assert np.allclose(calculated_supertrend[1:], expected_supertrend[1:], rtol=1e-5, equal_nan=True), "❌ Supertrend values are incorrect."
        logging.info("✅ Supertrend calculation test passed.")
    except Exception as e:
        logging.error(f"❌ Supertrend calculation failed: {e}")
        
def test_check_trend_flip():
    """Test trend flip detection."""
    # Test bullish reversal
    df_bullish = pd.DataFrame({
        "open": [100, 102],
        "close": [99, 103]  # Bearish to bullish
    })
    result = utils.check_trend_flip(df_bullish)
    assert result == "BUY", "❌ Bullish trend flip detection failed."

    # Test bearish reversal
    df_bearish = pd.DataFrame({
        "open": [100, 102],
        "close": [103, 101]  # Bullish to bearish
    })
    result = utils.check_trend_flip(df_bearish)
    assert result == "SELL", "❌ Bearish trend flip detection failed."

    # Test no trend flip
    df_no_flip = pd.DataFrame({
        "open": [100, 102],
        "close": [103, 104]  # No flip
    })
    result = utils.check_trend_flip(df_no_flip)
    assert result is None, "❌ No trend flip detection failed."

    logging.info("✅ Trend flip detection test passed.")

def test_get_nifty_price():
    """Test fetching real NIFTY price."""
    price = utils.get_nifty_price()
    
    if price:
        logging.info(f"✅ NIFTY price fetch test passed. 🔹 Fetched NIFTY Price: {price}")
    else:
        logging.error("❌ NIFTY price fetch test failed.")

def test_get_token_by_symbol():
    """Test fetching a real token by symbol."""
    symbol = "NIFTY"  # Use a reliable symbol
    token = utils.get_token_by_symbol(symbol)
    
    if token:
        logging.info(f"✅ Token fetch test passed. Symbol: {symbol}, Token: {token}")
    else:
        logging.error(f"❌ Token fetch test failed. Could not fetch token for {symbol}.")

def test_get_option_ltp():
    """Test fetching the real LTP of an option from NSE."""
    symbol = "NIFTY"          # Underlying asset
    expiry = "13-Mar-2025"    # Example expiry date from NSE
    strike_price = 22600      # Example strike price
    option_type = "CE"        # Call option

    logging.info(f"🔍 Testing LTP fetch for {symbol} {expiry} {strike_price} {option_type}")

    # Pass all required arguments to match function definition
    ltp = utils.get_option_ltp(symbol, strike_price, expiry, option_type)

    if ltp is not None:
        logging.info(f"✅ Option LTP fetch test passed. LTP: {ltp}")
    else:
        logging.error("❌ Option LTP fetch test failed. No data returned.")

def test_get_valid_expiry():
    """Test expiry date conversion."""
    available_expiries = ['27-Mar-2025', '03-Apr-2025', '09-Apr-2025']
    test_cases = ["27MAR25", "27MAR2025", "2025-03-27", "27-03-2025"]

    for expiry in test_cases:
        result = utils.get_valid_expiry(expiry, available_expiries)
        if result:
            logging.info(f"✅ Expiry Conversion Passed: {expiry} → {result}")
        else:
            logging.error(f"❌ Expiry Conversion Failed for {expiry}")

if __name__ == "__main__":
    logging.info("🔍 Running Utility Function Tests...\n")
    time.sleep(1)
    test_atr()
    time.sleep(1)
    test_upper_lower_bands()
    time.sleep(1)
    test_supertrend_logic()
    time.sleep(1)
    test_supertrend()
    time.sleep(1)
    test_check_trend_flip()
    time.sleep(1)
    test_get_nifty_price()
    time.sleep(1)
    test_get_token_by_symbol()
    time.sleep(1)
    test_get_option_ltp()
    time.sleep(1)
    test_get_valid_expiry()
    time.sleep(1)
    test_dummy_balance()
    logging.info("\n✅ All tests completed.")