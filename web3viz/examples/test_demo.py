#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Demo script with test data for Web3Viz
"""

import os
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import sys

# Add parent directory to import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web3viz import WalletVisualizer


def generate_mock_transactions(address, num_txs=50):
    """
    Generate test transaction data for demonstration
    
    Args:
        address (str): Ethereum address
        num_txs (int): Number of transactions
        
    Returns:
        pd.DataFrame: DataFrame with test transactions
    """
    # Generate random addresses
    addresses = [f"0x{i:040x}" for i in range(1, 11)]
    
    # Current date
    now = datetime.now()
    
    # List for storing transaction data
    txs = []
    
    # Generate transactions
    for i in range(num_txs):
        # Random date within the last 30 days
        tx_date = now - timedelta(days=np.random.randint(0, 30), 
                                  hours=np.random.randint(0, 24),
                                  minutes=np.random.randint(0, 60))
        
        # Random sender/recipient address
        if np.random.random() < 0.5:
            # Incoming transaction
            from_addr = np.random.choice(addresses)
            to_addr = address
        else:
            # Outgoing transaction
            from_addr = address
            to_addr = np.random.choice(addresses)
            
        # Random amount
        value = np.random.uniform(0.01, 5.0)
        
        # Generate random hash
        tx_hash = '0x' + ''.join(random.choice('0123456789abcdef') for _ in range(64))
        
        # Add transaction
        txs.append({
            'timeStamp': tx_date,
            'from': from_addr,
            'to': to_addr,
            'value': value,
            'hash': tx_hash,
            'blockNumber': str(np.random.randint(10000000, 20000000)),
            'gas': str(21000),
            'gasPrice': str(np.random.randint(20, 100) * 10**9),
            'gasUsed': str(21000),
        })
    
    # Create DataFrame
    df = pd.DataFrame(txs)
    return df


def main():
    # Test address
    address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    
    # Directory for saving results
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Initializing visualizer for address {address}")
    viz = WalletVisualizer(address)
    
    # Generate test data
    print("Generating test data...")
    mock_transactions = generate_mock_transactions(address, num_txs=100)
    viz.transactions = mock_transactions
    print(f"Generated {len(mock_transactions)} test transactions")
    
    # Create filename based on address and current date
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    address_short = address[:10]
    
    # Plot transaction history
    print("Plotting transaction history...")
    history_path = os.path.join(output_dir, f"{address_short}_history_{timestamp}.png")
    viz.plot_transaction_history(save_path=history_path)
    print(f"Transaction history chart saved to {history_path}")
    
    # Plot address network
    print("Plotting interaction network...")
    network_path = os.path.join(output_dir, f"{address_short}_network_{timestamp}.png")
    viz.plot_address_network(save_path=network_path)
    print(f"Interaction network chart saved to {network_path}")
    
    print("Visualization completed successfully!")
    print(f"Results saved to folder: {os.path.abspath(output_dir)}")


if __name__ == "__main__":
    main() 