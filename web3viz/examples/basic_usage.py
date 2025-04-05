#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example of using the Web3Viz library for visualizing
Ethereum address data.
"""

import os
import sys
import argparse
from datetime import datetime

# Add parent directory to import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web3viz import WalletVisualizer


def main():
    parser = argparse.ArgumentParser(description='Ethereum address data visualization')
    parser.add_argument('address', help='Ethereum address to analyze')
    parser.add_argument('--api-key', help='Etherscan API key (optional)')
    parser.add_argument('--output-dir', default='output', help='Directory for saving results')
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Create visualizer object
    print(f"Initializing visualizer for address {args.address}")
    viz = WalletVisualizer(args.address, api_key=args.api_key)
    
    # Get transaction data
    print("Fetching transaction data...")
    transactions = viz.fetch_transactions()
    print(f"Received {len(transactions)} transactions")
    
    # Create filename based on address and current date
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    address_short = args.address[:10]
    
    # Plot transaction history
    print("Plotting transaction history...")
    history_path = os.path.join(args.output_dir, f"{address_short}_history_{timestamp}.png")
    viz.plot_transaction_history(save_path=history_path)
    print(f"Transaction history chart saved to {history_path}")
    
    # Plot address network
    print("Plotting interaction network...")
    network_path = os.path.join(args.output_dir, f"{address_short}_network_{timestamp}.png")
    viz.plot_address_network(save_path=network_path)
    print(f"Interaction network chart saved to {network_path}")
    
    print("Visualization completed successfully!")


if __name__ == "__main__":
    main() 