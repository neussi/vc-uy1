#!/bin/bash
# Server port as requested
PORT=6123

# Create and activate virtual environment
python3 -m venv venv-server
source venv-server/bin/activate

# Install dependencies
pip install -qqq -r server/requirements.txt

# Kill any previous instance on the port
fuser -k $PORT/tcp || true
pkill -f "gunicorn.*server.main:app" || true

# Start Gunicorn in the background
echo "Starting VC-UY1 Server on port $PORT..."
nohup python3 -m gunicorn -w 4 -k uvicorn.workers.UvicornWorker server.main:app --bind 0.0.0.0:$PORT --log-level debug > server.log 2>&1 &

sleep 5
if pgrep -f "gunicorn.*server.main:app" > /dev/null; then
    echo "Server started successfully and verified on port $PORT."
else
    echo "ERROR: Server failed to start."
    cat server.log
    exit 1
fi
