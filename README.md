# Python WebSocket Client for Nimiq Testnet

This project contains a Python script that connects to the Nimiq testnet WebSocket server to subscribe to new head blocks and retrieve transactions for each block.

## Features

- Connects to the Nimiq testnet WebSocket server.
- Subscribes to new head blocks and retrieves corresponding transactions.
- Displays information about each new block, including block number, epoch number, batch number, block time, and transactions.
- Runs inside a Docker container for easy deployment.

## Requirements

- Docker
- Docker Compose

## Setup and Running

### Building the Docker Container

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/maestroi/nimiq-albatross-chainfollow.git
cd nimiq-albatross-chainfollow
```
Build the Docker image using Docker Compose:

```bash
Copy code
docker-compose up --build
```

This command will build the Docker image based on the Dockerfile located in the websocket directory.

### Environment Variables
WEBSOCKET_URL: The WebSocket URL for connecting to the Nimiq testnet. Default is wss://rpc-testnet.nimiqcloud.com/ws.

You can set this variable in the docker-compose.yml file or pass it as an argument when running the Docker container.

### Running the Application
To start the application, use Docker Compose:

```bash
Copy code
docker-compose up
```
This will start the WebSocket client in a Docker container. The script will automatically connect to the Nimiq testnet and start processing blocks and transactions.

### Stopping the Application
To stop the application, use the following command:

```bash
Copy code
docker-compose down
```
