import logging
import time
import sys
import os
import pandas as pd
import unittest
from unittest.mock import patch, MagicMock

# Get the parent directory of the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import trading_logic  # Ensure trading_logic.py is available
from auth import get_jwt_token
from api_client import get_balance, get_historical_data
from state_manager import TradeState

# Configure logging
logging.basicConfig(level=logging.INFO)

class TestTradingLogic(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        self.state = TradeState()
        self.access_token = "mock_access_token"
        self.current_price = 22500  # Mock price for testing

    @patch('trading_logic.get_open_positions')
    @patch('trading_logic.place_order')
    def test_manage_positions(self, mock_place_order, mock_get_open_positions):
        """Test managing open positions."""
        # Mock open positions
        mock_get_open_positions.return_value = [
            {'symbol': 'NIFTY25MAR22500CE', 'entry_price': 22000, 'quantity': 50, 'direction': 'LONG'}
        ]

        # Mock place_order to simulate successful order placement
        mock_place_order.return_value = {'status': 'success'}

        # Call the function
        trading_logic.manage_positions(self.state, self.current_price, self.access_token)

        # Verify that place_order was called (stop loss triggered)
        mock_place_order.assert_called_once()

        # Verify that the position was removed from the state
        self.assertEqual(len(self.state.open_positions), 0)
        logging.info("✅ Position management test passed.")

    @patch('trading_logic.get_balance')
    @patch('trading_logic.get_historical_data')
    @patch('trading_logic.find_affordable_option')
    @patch('trading_logic.place_order')
    def test_check_trade(self, mock_place_order, mock_find_affordable_option, mock_get_historical_data, mock_get_balance):
        """Test executing trade logic."""
        # Mock balance
        mock_get_balance.return_value = 100000  # Mock balance of 100,000

        # Mock historical data
        mock_get_historical_data.return_value = [
            [1, 100, 102, 98, 101, 1000],  # Example candle data
            [2, 101, 103, 99, 102, 1500],
            [3, 102, 104, 100, 103, 2000]
        ]

        # Mock affordable option
        mock_find_affordable_option.return_value = {
            'symbol': 'NIFTY25MAR22500CE',
            'ltp': 150,
            'strike_price': 22500,
            'expiry': '25-Mar-2025'
        }

        # Mock place_order to simulate successful order placement
        mock_place_order.return_value = {'status': 'success'}

        # Call the function
        trading_logic.check_trade(self.state, self.access_token)

        # Verify that place_order was called (new trade entered)
        mock_place_order.assert_called_once()

        # Verify that the new position was added to the state
        self.assertEqual(len(self.state.open_positions), 1)
        logging.info("✅ Trade execution test passed.")

if __name__ == "__main__":
    logging.info("🔍 Running Trading Logic Tests...\n")
    unittest.main()