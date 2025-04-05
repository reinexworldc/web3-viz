#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the WalletVisualizer class
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

# Add parent directory to import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web3viz import WalletVisualizer


class TestWalletVisualizer(unittest.TestCase):
    """
    Tests for the WalletVisualizer class
    """
    
    def setUp(self):
        """
        Test setup
        """
        self.valid_address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
        self.invalid_address = "invalid_address"
        self.api_key = "DEMO_API_KEY"
    
    def test_validate_address(self):
        """
        Test address validation check
        """
        viz = WalletVisualizer(self.valid_address)
        self.assertTrue(viz._validate_address())
        
        viz = WalletVisualizer(self.invalid_address)
        self.assertFalse(viz._validate_address())
    
    @patch('web3viz.visualizer.requests.get')
    def test_fetch_transactions(self, mock_get):
        """
        Test transaction fetching
        """
        # Prepare request mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'status': '1',
            'message': 'OK',
            'result': [
                {
                    'blockNumber': '14000000',
                    'timeStamp': '1639000000',
                    'hash': '0x123',
                    'from': '0xabc',
                    'to': self.valid_address.lower(),
                    'value': '1000000000000000000',  # 1 ETH
                    'gas': '21000',
                    'gasPrice': '50000000000',
                    'gasUsed': '21000',
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Execute test
        viz = WalletVisualizer(self.valid_address, api_key=self.api_key)
        df = viz.fetch_transactions()
        
        # Assertions
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['value'], 1.0)  # Check Wei to ETH conversion
        
        # Verify API call with correct parameters
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], 'https://api.etherscan.io/api')
        self.assertEqual(kwargs['params']['address'], self.valid_address.lower())
        self.assertEqual(kwargs['params']['apikey'], self.api_key)
    
    @patch('web3viz.visualizer.requests.get')
    def test_fetch_transactions_error(self, mock_get):
        """
        Test error handling when fetching transactions
        """
        # Prepare error response mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'status': '0',
            'message': 'Error',
            'result': []
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Execute test
        viz = WalletVisualizer(self.valid_address)
        
        # Check exception raising
        with self.assertRaises(Exception):
            viz.fetch_transactions()
    
    @patch('web3viz.visualizer.plt.savefig')
    @patch('web3viz.visualizer.plt.subplots')
    @patch('web3viz.visualizer.plt.figure')
    @patch('web3viz.visualizer.plt.close')
    @patch('web3viz.visualizer.WalletVisualizer.fetch_transactions')
    def test_plot_transaction_history(self, mock_fetch, mock_close, mock_figure, mock_subplots, mock_savefig):
        """
        Test transaction history plotting
        """
        # Setup matplotlib mocks
        mock_fig = MagicMock()
        mock_ax1 = MagicMock()
        mock_ax2 = MagicMock()
        mock_ax1.twinx.return_value = mock_ax2
        mock_subplots.return_value = (mock_fig, mock_ax1)
        
        # Prepare mock transaction data
        mock_df = pd.DataFrame([
            {
                'timeStamp': pd.Timestamp('2021-01-01'),
                'value': 1.0,
                'from': '0xabc',
                'to': self.valid_address.lower(),
            },
            {
                'timeStamp': pd.Timestamp('2021-01-02'),
                'value': 2.0,
                'from': self.valid_address.lower(),
                'to': '0xdef',
            }
        ])
        mock_fetch.return_value = mock_df
        
        # Execute test
        viz = WalletVisualizer(self.valid_address)
        viz.transactions = mock_df  # Set transaction data
        result = viz.plot_transaction_history(save_path='test.png')
        
        # Assertions
        self.assertEqual(result, 'test.png')
        mock_savefig.assert_called_once()
    
    @patch('web3viz.visualizer.plt.savefig')
    @patch('web3viz.visualizer.plt.figure')
    @patch('web3viz.visualizer.plt.close')
    @patch('web3viz.visualizer.nx.spring_layout')
    @patch('web3viz.visualizer.nx.draw_networkx_nodes')
    @patch('web3viz.visualizer.nx.draw_networkx_edges')
    @patch('web3viz.visualizer.nx.draw_networkx_labels')
    @patch('web3viz.visualizer.WalletVisualizer.fetch_transactions')
    def test_plot_address_network(self, mock_fetch, mock_labels, mock_edges, mock_nodes, 
                                 mock_layout, mock_close, mock_figure, mock_savefig):
        """
        Test address network plotting
        """
        # Setup matplotlib and networkx mocks
        mock_layout.return_value = {}
        
        # Prepare mock transaction data
        mock_df = pd.DataFrame([
            {
                'timeStamp': pd.Timestamp('2021-01-01'),
                'value': 1.0,
                'from': '0xabc',
                'to': self.valid_address.lower(),
            },
            {
                'timeStamp': pd.Timestamp('2021-01-02'),
                'value': 2.0,
                'from': self.valid_address.lower(),
                'to': '0xdef',
            }
        ])
        mock_fetch.return_value = mock_df
        
        # Execute test
        viz = WalletVisualizer(self.valid_address)
        viz.transactions = mock_df  # Set transaction data
        result = viz.plot_address_network(save_path='test_network.png')
        
        # Assertions
        self.assertEqual(result, 'test_network.png')
        mock_savefig.assert_called_once()


if __name__ == '__main__':
    unittest.main() 