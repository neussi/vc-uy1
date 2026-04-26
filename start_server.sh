#!/bin/bash
# Server port as requested
PORT=76123

# Install dependencies if not present
pip3 install -r server/requirements.txt

# Kill any previous instance on the port to avoid address-in-use errors
fuser -k $PORT/tcp || true

# Start Gunicorn in the background
LOG_FILE="/var/log/vc_uy1_gunicorn.log"
echo "Starting VC-UY1 Server on port $PORT..."
nohup gunicorn -w 4 -k uvicorn.workers.UvicornWorker server.main:app --bind 0.0.0.0:$PORT --access-logfile $LOG_FILE --error-logfile $LOG_FILE > server.log 2>&1 &

sleep 5
if pgrep -f "gunicorn.*server.main:app" > /dev/null; then
    echo "Server started successfully and verified."
else
    echo "ERROR: Server failed to start. Check $LOG_FILE for details."
    exit 1
fi
