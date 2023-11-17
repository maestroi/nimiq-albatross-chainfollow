import asyncio
import websockets
import json
import os

async def get_transactions_by_block_number(url, block_number):
    try:
        async with websockets.connect(url) as websocket:
            payload = json.dumps({
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getTransactionsByBlockNumber",
                "params": [block_number]
            })
            await websocket.send(payload)
            response = await websocket.recv()
            return json.loads(response)
    except websockets.exceptions.WebSocketException as e:
        print(f"WebSocket error occurred: {e}")
        return {}

async def format_transaction(tx):
    return (f"Hash: {tx['hash']}, Block: {tx['blockNumber']}, Timestamp: {tx['timestamp']}, "
            f"Confirmations: {tx['confirmations']}, From: {tx['from']}, To: {tx['to']}, "
            f"Value: {tx['value']}, Fee: {tx['fee']}, ExecutionResult: {tx.get('executionResult', 'N/A')}")

async def main():
    uri = os.getenv('WEBSOCKET_URL', 'wss://rpc-testnet.nimiqcloud.com/ws')
    last_block_timestamp = None

    while True:
        try:
            async with websockets.connect(uri) as websocket:
                # Subscribe to new head blocks
                subscribe_payload = json.dumps({
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "subscribeForHeadBlock",
                    "params": [True]
                })
                await websocket.send(subscribe_payload)

                # Process incoming messages
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)

                    if 'method' in data and data['method'] == 'subscribeForHeadBlock':
                        block_data = data['params']['result']['data']
                        block_number = block_data['number']
                        epoch_number = block_data['epoch']
                        batch_number = block_data['batch']
                        block_timestamp = block_data['timestamp']

                        # Calculate block time in milliseconds
                        block_time_ms = None
                        if last_block_timestamp is not None:
                            block_time_ms = block_timestamp - last_block_timestamp
                        last_block_timestamp = block_timestamp

                        # Fetch transactions for this block
                        transactions_data = await get_transactions_by_block_number(uri, block_number)
                        transactions = transactions_data.get('result', {}).get('data', [])
                        formatted_transactions = [await format_transaction(tx) for tx in transactions]

                        # Print all relevant information together
                        block_time_info = f", BlockTime: {block_time_ms:.2f} ms" if block_time_ms is not None else ""
                        print(f"Block: {block_number}, Epoch: {epoch_number}, Batch: {batch_number}{block_time_info}, Transactions: {formatted_transactions}")
        
        except websockets.exceptions.WebSocketException as e:
            print(f"WebSocket error occurred: {e}")
            print("Attempting to reconnect...")
            await asyncio.sleep(1)  # Wait for 5 seconds before trying to reconnect

if __name__ == "__main__":
    asyncio.run(main())
