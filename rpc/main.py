import requests
import json
import time
import os

def post_json_rpc(url, method, params=[]):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching {method}: {response.status_code}")
        return None

def get_data(url, method):
    response = post_json_rpc(url, method)
    return response.get('result', {}).get('data') if response else None

def get_transactions_by_block_number(url, block_number):
    return post_json_rpc(url, "getTransactionsByBlockNumber", [block_number])

def format_transaction(tx):
    return (f"Hash: {tx['hash']}, Block: {tx['blockNumber']}, Timestamp: {tx['timestamp']}, "
            f"Confirmations: {tx['confirmations']}, From: {tx['from']}, To: {tx['to']}, "
            f"Value: {tx['value']}, Fee: {tx['fee']}, ExecutionResult: {tx.get('executionResult', 'N/A')}")

def main():
    url = os.getenv('RPC_URL', 'https://rpc-testnet.nimiqcloud.com')
    last_block_number = None
    last_block_time = time.time()

    while True:
        current_block_number = get_data(url, "getBlockNumber")

        if current_block_number and current_block_number != last_block_number:
            current_time = time.time()
            block_time_ms = (current_time - last_block_time) * 1000
            last_block_time = current_time
            last_block_number = current_block_number

            epoch_number = get_data(url, "getEpochNumber")
            batch_number = get_data(url, "getBatchNumber")
            transactions_data = get_transactions_by_block_number(url, current_block_number)
            transactions = transactions_data.get('result', {}).get('data', [])

            formatted_transactions = [format_transaction(tx) for tx in transactions]

            print(f"Block: {current_block_number}, Epoch: {epoch_number}, Batch: {batch_number}, BlockTime: {block_time_ms:.2f} ms, Transactions: {formatted_transactions}")
        else:
            print("Waiting for new block...", end="\r")

        time.sleep(0.1)  # Check for a new block every 0.5 seconds

if __name__ == "__main__":
    main()
