# Web3Viz

Library for Ethereum blockchain data visualization.

## Features

- Fetching transaction data for Ethereum addresses via Etherscan API
- Plotting transaction history over time
- Visualizing interaction networks with other addresses
- Saving visualizations in PNG format

## Installation

```bash
pip install web3viz
```

## Usage

```python
from web3viz.visualizer import WalletVisualizer

# Initialize with wallet address
visualizer = WalletVisualizer("0x...")

# Plot transaction history
visualizer.plot_transaction_history()

# Plot interaction network
visualizer.plot_address_network()
```

## Requirements

- Python 3.7+
- pandas
- matplotlib
- requests
