#!/bin/bash
# Server port as requested
PORT=76123

# Install dependencies if not present
pip3 install -r server/requirements.txt

# Kill any previous instance on the port to avoid address-in-use errors
fuser -k $PORT/tcp || true

# Start Gunicorn in the background
# We assume we are in the project root
echo "Starting VC-UY1 Server on port $PORT..."
nohup gunicorn -w 4 -k uvicorn.workers.UvicornWorker server.main:app --bind 0.0.0.0:$PORT > server.log 2>&1 &

echo "Server started successfully."
