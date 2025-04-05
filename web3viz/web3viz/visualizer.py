import requests
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from datetime import datetime
import os
import matplotlib.dates as mdates
import numpy as np


class WalletVisualizer:
    """
    Class for visualizing Ethereum wallet data
    """

    def __init__(self, address, api_key=None):
        """
        Initialize visualization object for a wallet
        
        Args:
            address (str): Ethereum wallet address
            api_key (str, optional): Etherscan API key
        """
        self.address = address.lower()
        self.api_key = api_key
        self.transactions = None
        self.base_url = "https://api.etherscan.io/api"
        
    def _validate_address(self):
        """
        Check the validity of an Ethereum address
        
        Returns:
            bool: True if address is valid, False otherwise
        """
        # Basic check for Ethereum address format
        return self.address.startswith('0x') and len(self.address) == 42
    
    def fetch_transactions(self):
        """
        Get transaction data through Etherscan API
        
        Returns:
            pandas.DataFrame: Transaction data
        """
        if not self._validate_address():
            raise ValueError(f"Invalid Ethereum address: {self.address}")
        
        # Parameters for requesting normal transactions
        params = {
            "module": "account",
            "action": "txlist",
            "address": self.address,
            "startblock": 0,
            "endblock": 99999999,
            "sort": "asc"
        }
        
        # Add API key if provided
        if self.api_key:
            params["apikey"] = self.api_key
            
        # Perform API request
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()
            
            if data["status"] != "1":
                raise Exception(f"Etherscan API error: {data['message']}")
                
            # Convert response to DataFrame
            transactions = pd.DataFrame(data["result"])
            
            # If no transactions
            if transactions.empty:
                return pd.DataFrame()
                
            # Convert data types
            transactions["timeStamp"] = pd.to_datetime(transactions["timeStamp"].astype(int), unit="s")
            transactions["value"] = transactions["value"].astype(float) / 1e18  # Convert Wei to ETH
            transactions["gasPrice"] = transactions["gasPrice"].astype(float) / 1e9  # Convert Wei to Gwei
            transactions["gas"] = transactions["gas"].astype(int)
            transactions["gasUsed"] = transactions["gasUsed"].astype(int)
            
            self.transactions = transactions
            return transactions
            
        except requests.RequestException as e:
            raise ConnectionError(f"Error connecting to Etherscan API: {str(e)}")
        except Exception as e:
            raise Exception(f"Error fetching transaction data: {str(e)}")
    
    def plot_transaction_history(self, save_path=None):
        """
        Plot transaction history over time
        
        Args:
            save_path (str, optional): Path to save the image
        """
        # Check if transactions are loaded
        if self.transactions is None or self.transactions.empty:
            self.fetch_transactions()
            
        if self.transactions.empty:
            raise ValueError(f"No transaction data for address {self.address}")
            
        # Group transactions by day and sum values
        daily_volumes = self.transactions.groupby(self.transactions['timeStamp'].dt.date)['value'].sum()
        daily_counts = self.transactions.groupby(self.transactions['timeStamp'].dt.date).size()
        
        # Create figure with two Y axes
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = ax1.twinx()
        
        # Plot transaction volume (in ETH)
        ax1.plot(daily_volumes.index, daily_volumes.values, 'b-', label='Volume (ETH)')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Transaction Volume (ETH)', color='b')
        ax1.tick_params(axis='y', labelcolor='b')
        
        # Format date axis
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
        
        # Plot transaction count
        ax2.bar(daily_counts.index, daily_counts.values, alpha=0.3, color='r', label='Count')
        ax2.set_ylabel('Transaction Count', color='r')
        ax2.tick_params(axis='y', labelcolor='r')
        
        # Add legend
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        # Chart title
        plt.title(f'Transaction History for {self.address[:10]}...{self.address[-8:]}')
        plt.grid(True, alpha=0.3)
        fig.tight_layout()
        
        # Rotate date labels for better readability
        plt.gcf().autofmt_xdate()
        
        # Save or show the chart
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            return save_path
        else:
            plt.show()
            return fig
    
    def plot_address_network(self, depth=1, save_path=None, max_addresses=50):
        """
        Plot the network of interactions with other addresses
        
        Args:
            depth (int, optional): Network depth (not used yet)
            save_path (str, optional): Path to save the image
            max_addresses (int, optional): Maximum number of addresses in visualization
        
        Returns:
            matplotlib.Figure or str: Chart or path to saved file
        """
        # Check if transactions are loaded
        if self.transactions is None or self.transactions.empty:
            self.fetch_transactions()
            
        if self.transactions.empty:
            raise ValueError(f"No transaction data for address {self.address}")
            
        # Create directed graph
        G = nx.DiGraph()
        
        # Add central node (our address)
        G.add_node(self.address, size=20, color='red', label=f"{self.address[:6]}...{self.address[-4:]}")
        
        # Get all unique addresses our wallet has interacted with
        from_addresses = set(self.transactions['from'].str.lower())
        to_addresses = set(self.transactions['to'].str.lower())
        all_addresses = (from_addresses | to_addresses) - {self.address.lower()}
        
        # Limit the number of nodes for graph readability
        if len(all_addresses) > max_addresses:
            # Find top addresses by transaction volume
            volume_by_address = {}
            
            # Sum outgoing transaction volumes by recipient addresses
            for _, tx in self.transactions[self.transactions['from'] == self.address].iterrows():
                to_addr = tx['to'].lower()
                value = float(tx['value'])
                volume_by_address[to_addr] = volume_by_address.get(to_addr, 0) + value
                
            # Sum incoming transaction volumes by sender addresses
            for _, tx in self.transactions[self.transactions['to'] == self.address].iterrows():
                from_addr = tx['from'].lower()
                value = float(tx['value'])
                volume_by_address[from_addr] = volume_by_address.get(from_addr, 0) + value
                
            # Sort addresses by transaction volume and take top_n
            top_addresses = sorted(volume_by_address.items(), key=lambda x: x[1], reverse=True)[:max_addresses]
            all_addresses = {addr for addr, _ in top_addresses}
        
        # Add nodes for all addresses
        for address in all_addresses:
            G.add_node(address, size=10, color='blue', label=f"{address[:6]}...{address[-4:]}")
        
        # Add edges for transactions
        for _, tx in self.transactions.iterrows():
            from_addr = tx['from'].lower()
            to_addr = tx['to'].lower()
            
            # Check that both addresses are in our graph (one might be filtered out)
            if from_addr in G.nodes and to_addr in G.nodes:
                # If edge already exists, increase its weight
                if G.has_edge(from_addr, to_addr):
                    G[from_addr][to_addr]['weight'] += float(tx['value'])
                    G[from_addr][to_addr]['count'] += 1
                else:
                    G.add_edge(from_addr, to_addr, weight=float(tx['value']), count=1, from_addr=from_addr, to_addr=to_addr)
        
        # Configure node sizes based on transaction count
        sizes = []
        colors = []
        labels = {}
        
        for node in G.nodes():
            node_data = G.nodes[node]
            if node.lower() == self.address.lower():
                sizes.append(2000)  # Main node is larger than others
                colors.append('red')
            else:
                # Node size is proportional to transaction count
                tx_count = sum(1 for u, v, data in G.edges(data=True) 
                               if u == node or v == node)
                sizes.append(500 + tx_count * 100)
                colors.append('skyblue')
            
            # Add labels with shortened addresses
            labels[node] = node_data.get('label', f"{node[:6]}...{node[-4:]}")
        
        # Configure edge weights based on transaction volume
        edge_weights = [np.log1p(data['weight']) * 0.5 for _, _, data in G.edges(data=True)]
        
        # Create figure
        plt.figure(figsize=(12, 12))
        
        # Define node layout
        pos = nx.spring_layout(G, k=0.3, iterations=50)
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_size=sizes, node_color=colors, alpha=0.8)
        
        # Draw edges with varying thickness based on weight
        nx.draw_networkx_edges(G, pos, width=edge_weights, alpha=0.6, arrows=True, 
                              arrowsize=15, arrowstyle='->', edge_color='gray')
        
        # Add node labels
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_family='sans-serif')
        
        # Title and chart settings
        plt.title(f'Interaction Network for {self.address[:10]}...{self.address[-8:]}')
        plt.axis('off')  # Disable axes
        
        # Save or show the chart
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            return save_path
        else:
            plt.show()
            return plt.gcf()
