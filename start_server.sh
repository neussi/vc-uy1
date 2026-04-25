#!/bin/bash
# Install dependencies
pip install -r requirements.txt

# Start the server on port 76123
gunicorn -w 4 -k uvicorn.workers.UvicornWorker server.main:app --bind 0.0.0.0:76123
