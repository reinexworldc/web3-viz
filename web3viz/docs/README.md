# Web3Viz Documentation

## Overview

Web3Viz is a library for visualizing data from the Ethereum blockchain. It allows analyzing Ethereum address activity using charts and network visualizations.

## Installation

```bash
pip install web3viz
```

Or from source code:

```bash
git clone https://github.com/yourusername/web3viz.git
cd web3viz
pip install -e .
```

## Project Structure

```
web3viz/
├── docs/            # Documentation
├── examples/        # Usage examples
├── tests/           # Tests
├── web3viz/         # Library source code
│   ├── __init__.py  # Package initialization
│   └── visualizer.py # Main visualizer class
├── README.md        # General project description
└── setup.py         # Installation setup file
```

## Main Components

### WalletVisualizer

The main library class that provides functionality for:
- Fetching transactions for an address via Etherscan API
- Creating time-based transaction history charts
- Visualizing interaction networks with other addresses

### Usage Examples

#### Basic Example

```python
from web3viz import WalletVisualizer

# Initialize with wallet address
viz = WalletVisualizer("0x742d35Cc6634C0532925a3b844Bc454e4438f44e")

# Fetch transaction data
transactions = viz.fetch_transactions()

# Plot transaction history chart
viz.plot_transaction_history(save_path="history.png")

# Plot interaction network chart
viz.plot_address_network(save_path="network.png")
```

## Requirements

- Python 3.7+
- pandas
- matplotlib
- networkx
- requests 