#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Демонстрационный скрипт с тестовыми данными для Web3Viz
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import sys

# Добавляем родительскую директорию в путь импорта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web3viz.visualizer import WalletVisualizer


def generate_mock_transactions(address, num_txs=50):
    """
    Генерирует тестовые данные транзакций для демонстрации
    
    Args:
        address (str): Ethereum-адрес
        num_txs (int): Количество транзакций
        
    Returns:
        pd.DataFrame: DataFrame с тестовыми транзакциями
    """
    # Генерируем случайные адреса
    addresses = [f"0x{i:040x}" for i in range(1, 11)]
    
    # Текущая дата
    now = datetime.now()
    
    # Список для хранения данных транзакций
    txs = []
    
    # Генерируем транзакции
    for i in range(num_txs):
        # Случайная дата в пределах последних 30 дней
        tx_date = now - timedelta(days=np.random.randint(0, 30), 
                                  hours=np.random.randint(0, 24),
                                  minutes=np.random.randint(0, 60))
        
        # Случайный адрес отправителя/получателя
        if np.random.random() < 0.5:
            # Входящая транзакция
            from_addr = np.random.choice(addresses)
            to_addr = address
        else:
            # Исходящая транзакция
            from_addr = address
            to_addr = np.random.choice(addresses)
            
        # Случайная сумма
        value = np.random.uniform(0.01, 5.0)
        
        # Добавляем транзакцию
        txs.append({
            'timeStamp': tx_date,
            'from': from_addr,
            'to': to_addr,
            'value': value,
            'hash': f"0x{np.random.randint(0, 2**64):064x}",
            'blockNumber': str(np.random.randint(10000000, 20000000)),
            'gas': str(21000),
            'gasPrice': str(np.random.randint(20, 100) * 10**9),
            'gasUsed': str(21000),
        })
    
    # Создаем DataFrame
    df = pd.DataFrame(txs)
    return df


def main():
    # Тестовый адрес
    address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    
    # Директория для сохранения результатов
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Инициализация визуализатора для адреса {address}")
    viz = WalletVisualizer(address)
    
    # Генерируем тестовые данные
    print("Генерация тестовых данных...")
    mock_transactions = generate_mock_transactions(address, num_txs=100)
    viz.transactions = mock_transactions
    print(f"Сгенерировано {len(mock_transactions)} тестовых транзакций")
    
    # Создаем имя файла на основе адреса и текущей даты
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    address_short = address[:10]
    
    # Строим график истории транзакций
    print("Построение графика истории транзакций...")
    history_path = os.path.join(output_dir, f"{address_short}_history_{timestamp}.png")
    viz.plot_transaction_history(save_path=history_path)
    print(f"График истории транзакций сохранен в {history_path}")
    
    # Строим график сети адресов
    print("Построение графика сети взаимодействий...")
    network_path = os.path.join(output_dir, f"{address_short}_network_{timestamp}.png")
    viz.plot_address_network(save_path=network_path)
    print(f"График сети взаимодействий сохранен в {network_path}")
    
    print("Визуализация завершена успешно!")
    print(f"Результаты сохранены в папке: {os.path.abspath(output_dir)}")


if __name__ == "__main__":
    main() 