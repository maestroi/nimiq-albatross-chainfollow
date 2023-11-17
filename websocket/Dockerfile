# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the default environment variable for the WebSocket URL
ENV WEBSOCKET_URL="wss://rpc-testnet.nimiqcloud.com/ws"

# Run the script when the container launches
CMD ["python", "websocket.py"]
